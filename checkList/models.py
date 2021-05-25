from django.db import models
from django.conf import settings
from django.utils import timezone
class User(models.Model):
    name = models.CharField(max_length=100)
    userId = models.CharField(max_length=100)
    userPassword = models.CharField(max_length=100)


# Create your models here.
