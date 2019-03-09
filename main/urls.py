from django.conf.urls import url
from main import views

app_name = "main"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^scoring_detail$', views.scoring_detail, name='scoring_detail'),
    url(r'^sentimental_detail$', views.sentimental_detail, name='sentimental_detail'),
]