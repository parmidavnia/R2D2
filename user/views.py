import json

from django.contrib.auth import login, logout
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from tagger.models import SentenceHistory, Sentence
from scoring.models import ScoringSentenceHistory, ScoringSentence
from .models import User
from .forms import UserForm, UserRegisterForm


class MyProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User

    form_class = UserForm
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        return self.request.user


def authorization_and_get_user(request, userId):
    auth_token = request.META.get('HTTP_AUTH', None)
    users = User.objects.filter(token=auth_token)
    if users is None or len(users) == 0:
        return JsonResponse({
            'result': 'ERR',
            'error': {
                'key': 'AUTHENTICATION_ERROR'
            }
        }), None

    user = users[0]

    if user['role'] != 'ADMIN' and str(user['id']) != userId:
        return JsonResponse({
            'result': 'ERR',
            'error': {
                'key': 'AUTHORIZATION_ERROR'
            }
        }), user

    return None, user


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data.get('username')).exists():
                return render(request, 'users/register.html', {
                    'register': False,
                    'register_form': form,
                    'error': 'نام کاربری تکراری است'
                })
            user = User(
                username=form.cleaned_data.get('username'),
                first_name=form.cleaned_data.get('firstname'),
                last_name=form.cleaned_data.get('lastname'),
                email=form.cleaned_data.get('email'),
            )

            user.set_password(form.cleaned_data.get('password'))

            user.save()

            login(request, user)
            return render(request, 'users/register.html',
                          {'register': True, 'register_form': form})
        else:
            return render(request, 'users/register.html',
                          {'register': False, 'register_form': form})
    else:
        return render(request, 'users/register.html',
                      {register: False, 'register_form': UserRegisterForm()})


def user_logout(request):
    logout(request)
    return redirect('user:login')


def show_sentence_history(request, userId):
    # TODO only admin can see
    if request.method == 'GET':
        authorization_error, user = authorization_and_get_user(request, userId)
        if authorization_error is not None:
            return authorization_error

        sentence_histories = SentenceHistory.objects.filter(userId=userId)
        return JsonResponse({
            'result': 'OK',
            'data': {
                'sentence_histories': json.loads(sentence_histories.to_json())
            }
        })


def profile(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            ratings = SentenceHistory.objects.filter(userId=request.user)
            scores = ScoringSentenceHistory.objects.filter(userId=request.user)
            sentence_histories = None
            sentences = None
            scoring_sentence_histories = None
            scoring_sentences = None
            if request.user.is_superuser:
                sentence_histories = SentenceHistory.objects.all().order_by('-id')[:12]
                sentences = Sentence.objects.all().order_by('-id')[:12]

                scoring_sentence_histories = ScoringSentenceHistory.objects.all().order_by('-id')[:12]
                scoring_sentences = ScoringSentence.objects.all().order_by('-id')[:12]

            return render(request, 'users/profile.html', {
                'user': request.user,
                'ratings': ratings,
                'scores' : scores,
                'sentence_histories': sentence_histories,
                'sentences': sentences,
                'scoring_sentence_histories': scoring_sentence_histories,
                'scoring_sentences': scoring_sentences,
            })