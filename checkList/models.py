from django.db import models
from django.conf import settings
from django.utils import timezone
class User(models.Model):
    name = models.CharField(max_length=100)
    userId = models.CharField(max_length=100, primary_key = True)
    userPassword = models.CharField(max_length=100)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'userId', 'userPassword'], name="unique_user")
        ]

class CheckList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    checkListName = models.CharField(max_length=100)

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['user', 'checkListName'], name="unique_checkList")
    ]

class CheckListItems(models.Model):
    checkList = models.ForeignKey(CheckList, on_delete=models.CASCADE)
    itemName = models.CharField(max_length=100)

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['checkList', 'itemName'], name="unique_checkListItems")
    ]

class CheckListData(models.Model):
    checkListItem =  models.ForeignKey(CheckListItems, on_delete=models.CASCADE)
    dateData = models.DateTimeField(default=timezone.datetime.now())

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['checkListItem', 'dateData'], name="unique_checkListData")
    ]
# Create your models here.


