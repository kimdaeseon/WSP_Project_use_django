from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import User, CheckList, CheckListItems, CheckListData
from datetime import datetime
from django.utils import timezone


# Create your views here.

def login(request):
    return render(request, 'checkList/login.html', {})
def graph(request):
    user = User.objects.get(name = request.session['userName'], userId =  request.session['userId'])
    checkList = CheckList.objects.filter(user=user)
    return render(request, 'checkList/graph.html', {'checkLists' : checkList})
def index(request):
    user = User.objects.get(name = request.session['userName'], userId =  request.session['userId'])
    checkList = CheckList.objects.filter(user=user)
    return render(request, 'checkList/index.html', {'checkLists' : checkList})
def make_check_list_page(request):
    return render(request, 'checkList/makeCheckList.html', {})

def make_check_list(request):
    data = json.loads(request.body)
    items = data['data']
    user = User.objects.get(name = request.session['userName'], userId =  request.session['userId'])
    try:
        CheckList.objects.create(user = user, checkListName = data['title'])
        checkList = CheckList.objects.get(user = user, checkListName = data['title'])
        for i in items:
            CheckListItems.objects.create(checkList = checkList, itemName = i)

        return JsonResponse({
            'status' : 'true'
        }, json_dumps_params= {'ensure_ascii' : True})
    except:
        try:
            checkList = CheckList.objects.get(user = user, checkListName = data['title'])
            checkList.delete()
            return JsonResponse({
                'status' : 'false'
            }, json_dumps_params= {'ensure_ascii' : True})
        except:
            return JsonResponse({
                'status' : 'false'
            }, json_dumps_params= {'ensure_ascii' : True})


def check_login(request):
    data = json.loads(request.body)
    userId = data['userId']
    userPassword = data['userPassword']
    try:
        user = User.objects.get(userId = userId, userPassword = userPassword)
        request.session['userName'] = user.name
        request.session['userId'] = user.userId
        return JsonResponse({
            'loginstatus' : 'true'
        }, json_dumps_params = {'ensure_ascii' : True})
    except:
        return JsonResponse({
            'loginstatus' : 'false'
        }, json_dumps_params = {'ensure_ascii' : True})

def calcDiffer(differ):
    year = datetime.today().year
    month = datetime.today().month
    day = datetime.today().day
    monthData = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    targetYear = -1
    targetMonth = -1
    targetDay = -1

    if day - differ < 1 :
        if month - 1 < 1:
            targetYear = year-1
            targetMonth = 12
            targetDay = monthData[month-1] + (day - differ)
        else:
            targetYear = year
            targetMonth = month - 1
            targetDay = monthData[month-1] + (day - differ)
    else:
        targetYear = year
        targetMonth = month 
        targetDay = day - differ
    
    return targetYear, targetMonth, targetDay

def check_list(request, checkListName):

    year = datetime.today().year
    month = datetime.today().month
    day = datetime.today().day

    temp = []
    savedItems = []

    user = User.objects.get(name = request.session['userName'], userId =  request.session['userId'])
    checkList = CheckList.objects.get(user = user, checkListName = checkListName)
    checkListItem = CheckListItems.objects.filter(checkList = checkList)
    for i in checkListItem:
        temp = CheckListData.objects.filter(checkListItem = i, dateData__gt = timezone.datetime(year, month, day), dateData__lte = timezone.datetime.now())
        for j in temp:
            savedItems.append(j)
    for i in checkListItem:
        i.isChecked = False
        for j in savedItems:
            if i.itemName == j.checkListItem.itemName:
                i.isChecked = True

    return render(request, 'checkList/checkList.html', {'checkListItems' : checkListItem, 'checkListName' : checkListName})

def save_check_list(request):
    data = json.loads(request.body)
    checkListName = data['checkListName']
    items = data['itemList']
    user = User.objects.get(name = request.session['userName'], userId = request.session['userId'])
    checkList = CheckList.objects.get(user=user, checkListName = checkListName)
    for item in items:
        checkListItem = CheckListItems.objects.get(checkList=checkList, itemName = item)
        CheckListData.objects.create(checkListItem = checkListItem, dateData = timezone.datetime.now())
    
    return JsonResponse({
            'status' : 'true'
        }, json_dumps_params = {'ensure_ascii' : True})
    
def delete_check_list_page(request):
    user = User.objects.get(name = request.session['userName'], userId = request.session['userId'])
    checkList = CheckList.objects.filter(user = user)
    return render(request, 'checkList/index.html', {'deleteMode' : True, 'checkLists' : checkList})
    
def delete_check_list(request):
    data = json.loads(request.body)
    checkListName = data['checkListName']
    user = User.objects.get(name = request.session['userName'], userId = request.session['userId'])
    for name in checkListName:
        CheckList.objects.filter(user=user, checkListName = name).delete()
    
    return JsonResponse({
            'status' : 'true'
        }, json_dumps_params = {'ensure_ascii' : True})




def graph_data(request):
    data = json.loads(request.body)
    checkListName = data['checkListName']
    newData = []
    temp = []
    tempItemName = []
    count = 0
    user = User.objects.get(name = request.session['userName'], userId = request.session['userId'])
    for name in checkListName:
        checkList = CheckList.objects.get(user=user, checkListName = name)
        newData.append([])
        for i in range(0, 7):
            targetYear, targetMonth, targetDay = calcDiffer(i)
            targetPrevYear, targetPrevMonth, targetPrevDay = calcDiffer(i - 1)
            if i == 0:
                array = CheckListData.objects.filter(checkListItem__checkList = checkList, dateData__gt = timezone.datetime(targetYear, targetMonth, targetDay), dateData__lte = timezone.now())
                for i in array:
                    tempItemName.append(i.checkListItem.itemName)
                temp.append({
                    "date" : str(targetYear) + "." + str(targetMonth) + "." + str(targetDay) + ".",
                    "value" : len(array),
                    'items' : tempItemName[:]
                }) 
            else:
                array = CheckListData.objects.filter(checkListItem__checkList = checkList, dateData__gt = timezone.datetime(targetYear, targetMonth, targetDay), dateData__lte = timezone.datetime(targetPrevYear, targetPrevMonth, targetPrevDay))
                for i in array:
                    tempItemName.append(i.checkListItem.itemName)
                temp.append({
                    "date" : str(targetYear) + "." + str(targetMonth) + "." + str(targetDay) + ".",
                    "value" : len(array),
                    'items' : tempItemName[:]
                }) 
            tempItemName = []
        newData[count] = {
            'name' : name,
            'data' : temp[:]
        }
        count = count + 1
        temp = []
        
    return JsonResponse({
            'status' : 'true',
            'newData' : newData
        }, json_dumps_params = {'ensure_ascii' : True})

def registerPage(request):
    return render(request, 'checkList/register.html', {})

def register(request):
    data = json.loads(request.body)
    userId = data['userId']
    userPassword = data['userPassword']
    name = data['userName']
    try:
        User.objects.create(name = name, userId = userId, userPassword= userPassword)
        return JsonResponse({
            'status' : 'true',
        }, json_dumps_params = {'ensure_ascii' : True})
    except:
        return JsonResponse({
            'status' : 'false',
        }, json_dumps_params = {'ensure_ascii' : True})

