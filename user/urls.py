from django.conf.urls import url

from django.urls import path

from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from user import views

app_name = "user"

urlpatterns = [
    url(r'^register$', views.register, name='register'),
    url(r'^login$', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    url(r'^logout', views.user_logout, name='logout'),
    # url(r'^(?P<userId>[a-z0-9]*)/edit_profile$', views.edit_profile, name='edit_profile'),
    path('profile/me/', views.profile, name="profile")
]
