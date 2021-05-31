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
    checkList = CheckList.objects.filter(userName = request.session['userName'])
    return render(request, 'checkList/index.html', {'checkLists' : checkList})
def make_check_list_page(request):
    return render(request, 'checkList/makeCheckList.html', {})

def make_check_list(request):
    data = json.loads(request.body)
    items = data['data']
    print(data['title'], data['data'])

    CheckList.objects.create(userName = request.session['userName'], checkListName = data['title'])

    for i in items:
        CheckListItems.objects.create(userName = request.session['userName'], checkListName = data['title'], itemName = i)

    return JsonResponse({
        'status' : 'success'
    }, json_dumps_params= {'ensure_ascii' : True})

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