from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home_view, name='home'),
    path('home/search/', views.search_view, name='search'),
    path('home/<slug:active_target>/', views.home_view, name='home'),
    path('home/add-friend/<str:sender>/<str:receiver>/', views.add_friend_view, name='add_friend'),
    path('error/', views.error_view, name='error'),
    path('', views.landing_view, name='landing'),
]

