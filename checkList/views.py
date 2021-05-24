from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

def login(request):
    return render(request, 'checkList/login.html', {})
def graph(request):
    return render(request, 'checkList/graph.html', {})
def index(request):
    return render(request, 'checkList/index.html', {})
def check_login(request):
    return JsonResponse({
        'message' : 'test',
        'array' : ['test', 'array']
    }, json_dumps_params = {'ensure_ascii' : True})