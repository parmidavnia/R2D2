import datetime


from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.CharField(max_length=1024)
    registrationDate = models.DateTimeField(auto_now=True)
    score = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='static/site-media/photos/profiles/', blank=True, null=True,
                               default='static/site-media/photos/profiles/matthew.png')

