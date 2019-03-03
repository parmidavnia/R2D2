from django.conf.urls import url
from django.urls import path
from scoring import views

app_name = "scoring"

urlpatterns = [
    url(r'^$', views.scoring, name='scoring'),
    url(r'^(?P<sentenceId>[0-9]*)/score$', views.score_sentence, name='score_sentence'),
    url(r'^add_scoring_sentence$', views.add_scoring_sentence, name='add_scoring_sentence'),

]