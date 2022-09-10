from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from platy.models import Friends

from api.serializers import UserSerializer, FriendSerializer



@api_view(['GET', 'POST'])
def get_users_api_view(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return Response(serializer.data)


# @api_view(['GET', 'POST'])
# def get_friends_api_view(request, f):
#     friends = Friends.objects.all()
#     serializer = UserSerializer(friends, many=True)

#     return Response(serializer.data)

@api_view(['GET', 'POST'])
def friends_api_view(request):
    friends = Friends.objects.filter(is_accepted=True)\
        .filter(Q(req_sender_id=request.user.id) | Q(req_receiver_id=request.user.id))
    print(friends)

    serializer = FriendSerializer(friends, many=True)

    return Response(serializer.data)

@api_view(['GET', 'POST'])
def pending_friend_reqs_api_view(request):
    req_pending = Friends.objects.filter(req_sender_id=request.user.id).filter(is_accepted=False)
    print(req_pending)

    serializer = FriendSerializer(req_pending, many=True)

    return Response(serializer.data)

@api_view(['GET', 'POST'])
def received_friend_reqs_api_view(request):
    req_received = Friends.objects.filter(req_receiver_id=request.user.id).filter(is_accepted=False)
    print(req_received)

    serializer = FriendSerializer(req_received, many=True)

    return Response(serializer.data)


@api_view(['GET', 'POST'])
def send_friend_req_api_view(request, target):


    return Response()

@api_view(['GET', 'POST'])
def confirm_friend_req_api_view(request, sender_id):
    add_friend_target = Friends.objects.get(
        Q(req_sender_id=sender_id) &
        Q(req_receiver_id=request.user.id) &
        Q(is_accepted=False)
    )

    add_friend_target.is_accepted = True
    add_friend_target.save()

    # return Response(status=200, template_name='home')
    return redirect('home')

