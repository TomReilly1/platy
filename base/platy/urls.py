from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home_view, name='home'),
    path('home/search/', views.search_view, name='search'),
    path('', views.landing_view, name='landing'),
]

