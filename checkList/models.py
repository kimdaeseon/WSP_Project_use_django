from django.db import models
from django.conf import settings
from django.utils import timezone
class User(models.Model):
    name = models.CharField(max_length=100)
    userId = models.CharField(max_length=100)
    userPassword = models.CharField(max_length=100)

class CheckList(models.Model):
    userName = models.CharField(max_length=100)
    checkListName = models.CharField(max_length=100)

class CheckListItems(models.Model):
    checkListName = models.CharField(max_length=100)
    userName = models.CharField(max_length=100)
    itemName = models.CharField(max_length=100)

class CheckListData(models.Model):
    userName = models.CharField(max_length=100)
    checkListName = models.CharField(max_length=100)
    itemName = models.CharField(max_length=100)
    dateData = models.DateTimeField(default=timezone.now)
# Create your models here.


