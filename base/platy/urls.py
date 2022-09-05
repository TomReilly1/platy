from django.urls import path, include, render
from . import views


urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('', views.landing_view, name='landing'),
]

