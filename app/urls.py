from django.urls import path
from app import views

urlpatterns = [
    path('', views.home),
    path('login', views.login),
    path('register', views.register),
    path('login_process', views.login_process),
    path('register_process', views.register_process),
]