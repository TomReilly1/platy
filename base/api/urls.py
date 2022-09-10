from django.urls import path
from . import views

urlpatterns = [
    path('get-users/', views.get_users_api_view, name='users_api'),
    path('friends/', views.friends_api_view, name='friends_api'),
    path('pending-friend-reqs/', views.pending_friend_reqs_api_view, name='pending_reqs_api'),
    path('received-friend-reqs/', views.received_friend_reqs_api_view, name='received_reqs_api'),
    path('confirm-friend/<int:sender_id>/', views.confirm_friend_req_api_view, name='confirm_friend_api'),
    path('send-friend-req/', views.send_friend_req_api_view, name='send_req_api'),
    # path('', views.),
]