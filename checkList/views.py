from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import User, CheckList, CheckListItems, CheckListData

# Create your views here.

def login(request):
    return render(request, 'checkList/login.html', {})
def graph(request):
    return render(request, 'checkList/graph.html', {})
def index(request):
    return render(request, 'checkList/index.html', {})


def check_login(request):
    data = json.loads(request.body)
    userId = data['userId']
    userPassword = data['userPassword']
    isUser = User.objects.filter(userId = userId, userPassword = userPassword)
    print(isUser)
    if not isUser:
        print("login failed")
        return JsonResponse({
            'loginstatus' : 'false'
        }, json_dumps_params = {'ensure_ascii' : True})
    else:
        print(isUser[0].name)
        request.session['userName'] = isUser[0].name
        return JsonResponse({
            'loginstatus' : 'true'
        }, json_dumps_params = {'ensure_ascii' : True})