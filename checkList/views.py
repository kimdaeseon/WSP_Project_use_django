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
    checkList = CheckList.objects.filter(userName = request.session['userName'])
    return render(request, 'checkList/graph.html', {'checkLists' : checkList})
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
    
    checkListItems = CheckListItems.objects.filter(checkListName = checkListName, userName = request.session['userName'])
    savedItems = CheckListData.objects.filter(userName = request.session['userName'], checkListName = checkListName, dateData__gt = timezone.datetime(year, month, day), dateData__lte = timezone.datetime.now())
    for i in checkListItems:
        i.isChecked = False
        for j in savedItems:
            print(i.itemName, j.itemName)
            if i.itemName == j.itemName:
                i.isChecked = True

    return render(request, 'checkList/checkList.html', {'checkListItems' : checkListItems, 'checkListName' : checkListName})

def save_check_list(request):
    data = json.loads(request.body)
    checkListName = data['checkListName']
    items = data['itemList']
    print(items)
    for item in items:
        print(items)
        CheckListData.objects.create(userName = request.session['userName'], checkListName = checkListName, itemName = item)
    
    return JsonResponse({
            'status' : 'true'
        }, json_dumps_params = {'ensure_ascii' : True})
    
def delete_check_list_page(request):
    checkList = CheckList.objects.filter(userName = request.session['userName'])
    return render(request, 'checkList/index.html', {'deleteMode' : True, 'checkLists' : checkList})
    
def delete_check_list(request):
    data = json.loads(request.body)
    checkListName = data['checkListName']
    print(checkListName)
    for name in checkListName:
        print(name)
        print( CheckList.objects.filter(userName = request.session['userName'], checkListName = name))
        CheckList.objects.filter(userName = request.session['userName'], checkListName = name).delete()
        print( CheckList.objects.filter(userName = request.session['userName'], checkListName = name))

        print( CheckListItems.objects.filter(userName = request.session['userName'], checkListName = name))
        CheckListItems.objects.filter(userName = request.session['userName'], checkListName = name).delete()
        print( CheckListItems.objects.filter(userName = request.session['userName'], checkListName = name))

        print( CheckListData.objects.filter(userName = request.session['userName'], checkListName = name))
        CheckListData.objects.filter(userName = request.session['userName'], checkListName = name).delete()
        print( CheckListData.objects.filter(userName = request.session['userName'], checkListName = name))
    
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
    for name in checkListName:
        newData.append([])
        for i in range(0, 7):
            targetYear, targetMonth, targetDay = calcDiffer(i)
            targetPrevYear, targetPrevMonth, targetPrevDay = calcDiffer(i - 1)
            if i == 0:
                print(request.session['userName'], name)
                array = CheckListData.objects.filter(userName = request.session['userName'], checkListName = name, dateData__gt = timezone.datetime(targetYear, targetMonth, targetDay), dateData__lte = timezone.now())
                for i in array:
                    tempItemName.append(i.itemName)
                temp.append({
                    "date" : str(targetYear) + "." + str(targetMonth) + "." + str(targetDay) + ".",
                    "value" : len(CheckListData.objects.filter(userName = request.session['userName'], checkListName = name, dateData__gt = timezone.datetime(targetYear, targetMonth, targetDay), dateData__lte = timezone.now())),
                    'items' : tempItemName[:]
                }) 
            else:
                print(request.session['userName'], name)
                array = CheckListData.objects.filter(userName = request.session['userName'], checkListName = name, dateData__gt = timezone.datetime(targetYear, targetMonth, targetDay), dateData__lte = timezone.datetime(targetPrevYear, targetPrevMonth, targetPrevDay))
                for i in array:
                    tempItemName.append(i.itemName)
                temp.append({
                    "date" : str(targetYear) + "." + str(targetMonth) + "." + str(targetDay) + ".",
                    "value" : len(CheckListData.objects.filter(userName = request.session['userName'], checkListName = name, dateData__gt = timezone.datetime(targetYear, targetMonth, targetDay), dateData__lte = timezone.datetime(targetPrevYear, targetPrevMonth, targetPrevDay))),
                    'items' : tempItemName[:]
                }) 
            tempItemName = []
        newData[count] = {
            'name' : name,
            'data' : temp[:]
        }
        count = count + 1
        temp = []
        
    print(newData)
    return JsonResponse({
            'status' : 'true',
            'newData' : newData
        }, json_dumps_params = {'ensure_ascii' : True})

def test(request):


    CheckListData.objects.create(userName = "daeseon", checkListName = "test", itemName = "testItem", dateData = timezone.datetime(2021, 6, 17))

    return JsonResponse({
            'status' : 'false'
        }, json_dumps_params = {'ensure_ascii' : True})