from django.contrib import admin
from .models import User, CheckList, CheckListData, CheckListItems

admin.site.register(User)
admin.site.register(CheckList)
admin.site.register(CheckListItems)
admin.site.register(CheckListData)

# Register your models here.
