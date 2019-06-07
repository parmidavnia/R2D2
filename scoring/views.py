from django.shortcuts import render
import json
from random import randint

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http.response import JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from scoring.models import ScoringSentence, ScoringSentenceHistory, ScoringDataset
from user.models import User

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def add_scoring_sentence(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'GET':
        return render(request, 'scoring/add_scoring_sentence.html')
    elif request.method == 'POST':
        try:
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'پسوند فایل باید csv باشد')
                return render(request, "scoring/add_scoring_sentence.html", {
                    'error': 'پسوند فایل باید CSV باشد'
                })
            if csv_file.multiple_chunks():
                messages.error(request, "سایز فایل مورد نظر زیاد است (%.2f MB)." % (csv_file.size / (1000 * 1000),))
                return render(request, "scoring/add_scoring_sentence.html", {
                    'error': 'سایز فایل مورد نظر زیاد است.'
                })

            dataset = ScoringDataset(name=csv_file.name)
            dataset.save()
            file_data = csv_file.read().decode("utf-8")
            lines = file_data.split("\n")
            line_no = -1
            for line in lines:
                line_no += 1
                print(line)
                fields = line.split(",")
                if line_no == 0:
                    continue
                number = fields[0]
                mr = str(fields[1])
                text = str(fields[2]).strip()
                if len(text) != 0:
                    s = ScoringSentence(number=number, text=text, mr=mr, dataset=dataset)
                    s.save()

        except Exception as e:
            messages.error(request, "خطا در آپلود فایل: " + repr(e))
            return render(request, "scoring/add_scoring_sentence.html", {
                'error': 'خطا در آپلود فایل'
            })

        return render(request, "scoring/add_scoring_sentence.html", {
            'done': True
        })


def scoring(request):
    if request.user.is_authenticated:
        user_sentence_history = ScoringSentenceHistory.objects.filter(userId=request.user.id)
        user_rated_sentences = [x.sentenceId for x in user_sentence_history]
    else:
        ip = get_client_ip(request)
        user_sentence_history = ScoringSentenceHistory.objects.filter(ip=ip)
        user_rated_sentences = [x.sentenceId for x in user_sentence_history]

    user_rated_sentences_ids = [x.id for x in user_rated_sentences]

    valid_sentences = ScoringSentence.objects.exclude(id__in=user_rated_sentences_ids)
    count = len(valid_sentences)
    if count == 0:
        return render(request, 'scoring/scoring.html', {'all_rated': True})
    random_index = randint(0, count - 1)
    s = valid_sentences[random_index]

    if request.method == 'GET':
        return render(request, 'scoring/scoring.html', {'sentence': s})


@csrf_exempt
def score_sentence(request, sentenceId):
    if request.method == 'PUT':
        s = ScoringSentence.objects.get(pk=sentenceId)
        body = json.loads(request.body.decode('utf-8'))
        inform = body.get('inform', None)
        natural = body.get('natural', None)
        quality = body.get('quality', None)
        if inform is None:
            return JsonResponse({
                'result': 'ERR',
                'key': 'INFORMATIVENESS_IS_NONE'
            })
        if natural is None:
            return JsonResponse({
                'result': 'ERR',
                'key': 'NATURALNESS_IS_NONE'
            })
        if quality is None:
            return JsonResponse({
                'result': 'ERR',
                'key': 'QUALITY_IS_NONE'
            })
        ip = get_client_ip(request)
        u = None
        if request.user.is_authenticated:
            user = request.user
            userId = user.id
            u = User.objects.get(pk=userId)
            history = ScoringSentenceHistory.objects.filter(sentenceId=s, userId=u)
            if history is not None and len(history) > 0:
                return JsonResponse({
                    'result': 'ERR',
                    'key': 'YOU_RATED_THIS_BEFORE'
                })
            user.score += 1
            user.save()
        else:
            history = ScoringSentenceHistory.objects.filter(sentenceId=s, ip=ip)
            if history is not None and len(history) > 0:
                return JsonResponse({
                    'result': 'ERR',
                    'key': 'YOU_RATED_THIS_BEFORE'
                })

        informativeness_avg = inform * 0.2 + s.informativeness_avg * 0.8
        naturalness_avg = natural * 0.2 + s.naturalness_avg * 0.8
        quality_avg = quality * 0.2 + s.quality_avg * 0.8
        s.informativeness_avg = informativeness_avg
        s.naturalness_avg = naturalness_avg
        s.quality_avg = quality_avg
        s.save()
        dataset = s.dataset
        dataset.informativeness_avg = 0.8*dataset.informativeness_avg + 0.2*inform
        dataset.naturalness_avg = 0.8 * dataset.naturalness_avg + 0.2 * natural
        dataset.quality_avg = 0.8 * dataset.quality_avg + 0.2 * quality
        dataset.save()

        sentence_history = ScoringSentenceHistory(userId=u, sentenceId=s, informativeness=inform,
                                           naturalness=natural, quality=quality, ip=ip)
        sentence_history.save()
        return JsonResponse({
            'result': 'OK',
            'url': reverse('scoring:scoring')
        }, safe=False)