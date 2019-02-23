from django.conf.urls import url
from main import views

app_name = "tagger"

urlpatterns = [
    url(r'^$', views.index, name='index'),
]