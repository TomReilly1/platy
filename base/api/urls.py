from django.urls import path
from . import views

urlpatterns = [
    path('get-users/', views.get_users_api_view),
]