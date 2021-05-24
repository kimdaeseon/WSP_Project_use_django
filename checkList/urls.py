from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('index', views.index, name='index'),
    path('graph', views.graph, name='graph'),
    path('api/v1/login', views.check_login, name='check_login'),
]
