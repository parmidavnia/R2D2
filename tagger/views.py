import json
from random import randint

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http.response import JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from tagger.models import Sentence, SentenceHistory
from user.models import User


def admin_authorization(request):
    auth_token = request.META.get('HTTP_AUTH', None)
    users = User.objects.filter(token=auth_token)
    if users is None or len(users) == 0:
        return JsonResponse({
            'result': 'ERR',
            'error': {
                'key': 'AUTHENTICATION_ERROR'
            }
        })

    user = users[0]

    if user['role'] != 'ADMIN':
        return JsonResponse({
            'result': 'ERR',
            'error': {
                'key': 'AUTHORIZATION_ERROR'
            }
        })
    return None


def add_sentence(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'GET':
        return render(request, 'tagger/add_sentence.html')
    elif request.method == 'POST':
        try:
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'پسوند فایل باید csv باشد')
                return render(request, "tagger/add_sentence.html", {
                    'error': 'پسوند فایل باید CSV باشد'
                })
            if csv_file.multiple_chunks():
                messages.error(request, "سایز فایل مورد نظر زیاد است (%.2f MB)." % (csv_file.size / (1000 * 1000),))
                return render(request, "tagger/add_sentence.html", {
                    'error': 'سایز فایل مورد نظر زیاد است.'
                })
            file_data = csv_file.read().decode("utf-8")

            lines = file_data.split("\n")
            # loop over the lines and save them in db. If error , store as string and then display
            for line in lines:
                print(line)
                fields = line.split(",")
                text = str(fields[0]).strip()
                if len(text) != 0:
                    s = Sentence(text=text)
                    s.save()

        except Exception as e:
            messages.error(request, "خطا در آپلود فایل: " + repr(e))
            return render(request, "tagger/add_sentence.html", {
                'error': 'خطا در آپلود فایل'
            })

        return render(request, "tagger/add_sentence.html", {
            'done': True
        })


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def sentence(request):
    if request.user.is_authenticated:
        user_sentence_history = SentenceHistory.objects.filter(userId=request.user.id)
        user_rated_sentences = [x.sentenceId for x in user_sentence_history]
    else:
        ip = get_client_ip(request)
        user_sentence_history = SentenceHistory.objects.filter(ip=ip)
        user_rated_sentences = [x.sentenceId for x in user_sentence_history]

    user_rated_sentences_ids = [x.id for x in user_rated_sentences]

    valid_sentences = Sentence.objects.exclude(id__in=user_rated_sentences_ids)
    count = len(valid_sentences)
    if count == 0:
        return render(request, 'tagger/sentence.html', {'all_rated': True})
    random_index = randint(0, count - 1)
    s = valid_sentences[random_index]

    if request.method == 'GET':
        return render(request, 'tagger/sentence.html', {'sentence': s})


def get_all_sentences(request, page, limit):
    if request.method == 'GET':
        if not request.user.is_superuser:
            raise PermissionDenied
        page = int(page)
        limit = int(limit)

        offset = (page - 1) * limit
        upper_bound = limit + offset

        sentences = Sentence.objects.all()[offset:upper_bound]

        previous_page = page - 1 if page > 1 else None
        next_page = page + 1 if len(sentences) > 0 else None

        return render(request, 'tagger/all_sentences.html', {
            'sentences': sentences,
            'next_limit': limit,
            'next_page': next_page,
            'previous_page': previous_page,
        })


def get_all_sentences_history(request, page, limit):
    if request.method == 'GET':
        if not request.user.is_superuser:
            raise HttpResponseForbidden()
        page = int(page)
        limit = int(limit)

        offset = (page - 1) * limit
        upper_bound = limit + offset

        histories = SentenceHistory.objects.all()[offset:upper_bound]

        previous_page = page - 1 if page > 1 else None
        next_page = page + 1 if len(histories) > 0 else None

        return render(request, 'tagger/all_sentences_history.html', {
            'histories': histories,
            'next_limit': limit,
            'next_page': next_page,
            'previous_page': previous_page,
        })


@csrf_exempt
def rate_sentence(request, sentenceId):
    if request.method == 'PUT':
        s = Sentence.objects.get(pk=sentenceId)
        body = json.loads(request.body.decode('utf-8'))
        polarity = body.get('polarity', None)
        if polarity is None:
            return JsonResponse({
                'result': 'ERR',
                'key': 'SCORE_IS_NONE'
            })

        ip = get_client_ip(request)
        u = None
        if request.user.is_authenticated:
            user = request.user
            userId = user.id
            u = User.objects.get(pk=userId)
            history = SentenceHistory.objects.filter(sentenceId=s, userId=u)
            if history is not None and len(history) > 0:
                return JsonResponse({
                    'result': 'ERR',
                    'key': 'YOU_RATED_THIS_BEFORE'
                })
            user.score += 1
            user.save()
        else:
            history = SentenceHistory.objects.filter(sentenceId=s, ip=ip)
            if history is not None and len(history) > 0:
                return JsonResponse({
                    'result': 'ERR',
                    'key': 'YOU_RATED_THIS_BEFORE'
                })

        avg = ((polarity * 0.2) + (s.polarityAvg * 0.8))
        s.polarityAvg = avg
        s.save()

        sentence_history = SentenceHistory(userId=u, sentenceId=s, polarity=polarity, ip=ip)
        sentence_history.save()
        return JsonResponse({
            'result': 'OK',
            'url': reverse('tagger:sentence')
        }, safe=False)

