from django.conf.urls import url
from django.urls import path
from tagger import views

app_name = "tagger"

urlpatterns = [
    url(r'^$', views.sentence, name='sentence'),
    url(r'^add$', views.add_sentence, name='add_sentence'),
    url(r'^(?P<sentenceId>[0-9]*)/rate$', views.rate_sentence, name='rate_sentence'),
    url(r'^history/(?P<page>[0-9]*)/(?P<limit>[0-9]*)$', views.get_all_sentences_history, name='get_all_sentences_history'),
    url(r'^(?P<page>[0-9]*)/(?P<limit>[0-9]*)$', views.get_all_sentences, name='get_all_sentences'),
    url(r'^scoring$', views.scoring, name='scoring'),
    url(r'^(?P<sentenceId>[0-9]*)/score$', views.score_sentence, name='score_sentence'),
    url(r'^add_scoring_sentence$', views.add_scoring_sentence, name='add_scoring_sentence'),

]