from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('index', views.index, name='index'),
    path('graph', views.graph, name='graph'),
    path('api/v1/login', views.check_login, name='check_login'),
    path('makeCheckList', views.make_check_list_page, name='make_check_list_page'),
    path('api/v1/makeCheckList', views.make_check_list, name='make_check_list')
]
