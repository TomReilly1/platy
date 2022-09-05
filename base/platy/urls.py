from django.urls import path, include, render
from . import views


urlpatterns = [
    path('/home', views.home_view, name='home')
]

