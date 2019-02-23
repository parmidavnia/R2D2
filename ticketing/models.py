import datetime

from django.db import models
from mongoengine import *

from user.models import User


#class Ticket(models.Model):
class Ticket(models.Model):
    text = models.TextField(max_length=4096, null=False)
    # TODO refactor
    userId = models.ForeignKey(User, on_delete=CASCADE)
