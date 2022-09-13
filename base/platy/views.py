import requests
import json

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.db.models import Q
from django.contrib.auth.models import User
# from django.contrib.postgres import search

from platy.models import DirectMessages, Friends
from platy.forms import SearchForm, SignUpForm


# Create your views here.
@require_GET
def landing_view(request):
    return render(request, 'landing.html')


@login_required(login_url='/accounts/login/')
@require_GET
def home_view(request, active_target=None):
    # print(requests.get('http://localhost:8000/api/get-users').text)

    req_pending = Friends.objects.filter(req_sender_id=request.user.id).filter(is_accepted=False)
    req_received = Friends.objects.filter(req_receiver_id=request.user.id).filter(is_accepted=False)
    friends = Friends.objects.filter(is_accepted=True)\
        .filter(Q(req_sender_id=request.user.id) | Q(req_receiver_id=request.user.id))

    pending_req_list = list(req_pending)
    print(pending_req_list)
    
    received_req_list = list(req_received)
    print(received_req_list)
    
    # friends_list = []
    # for f in friends:
    #     if f.req_receiver == request.user:
    #         friends_list.append(f.req_sender)
    #     elif f.req_sender == request.user:
    #         friends_list.append(f.req_receiver)
    #     else:
    #         raise 'CUSTOM ERROR: Unkown error in creating friends list'

    friends_list = friends
    print(friends_list)


    


    if active_target:
        l_sender_user = User.objects.get(username=request.user)
        l_target_user = User.objects.get(username=active_target)
        
        stored_messages = DirectMessages.objects.filter(
            (Q(msg_sender_id=l_sender_user.id) & Q(msg_receiver_id=l_target_user.id)) | 
            (Q(msg_sender_id=l_target_user.id) & Q(msg_receiver_id=l_sender_user.id))
        )
    else:
        stored_messages = None


    return render(request, 'home.html', {
        'friends': friends_list,
        'pending': pending_req_list,
        'received': received_req_list,
        'active_target': active_target,
        'stored_messages': stored_messages
    })




@require_http_methods(['GET', 'POST'])
def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'signup.html', {'form': form})

@login_required(login_url='/accounts/login/')
@require_http_methods(['GET', 'POST'])
def search_view(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        
        if form.is_valid():            
            search_str = form.cleaned_data.get('search_query')
            search_request = User.objects.filter(username__istartswith=search_str)[:5]
            friends = Friends.objects.all()

                        
            user_list = []

            for obj in search_request:
                user_obj = {'name': obj.username, 'has_requested': False, 'are_friends': False}
                print(user_obj)
                for pair in friends:
                    if request.user.id == pair.req_sender_id and obj.id == pair.req_receiver_id:
                        user_obj['has_requested'] = True
                        
                        if pair.is_accepted:
                            user_obj['are_friends'] = True
                        
                        break

                user_list.append(user_obj)                        
                print(user_list)
            # user_list = list(map(lambda obj: {'name':obj.username}, search_request))


            return render(request, 'search.html', {'form': form, 'userlist': user_list})
    # GET Method
    else:
        form = SearchForm()
        return render(request, 'search.html', {'form': form, 'userlist': [{'name':''}]})

    return render(request, 'search.html', {'form': form})


@login_required(login_url='/accounts/login/')
@require_POST
def add_friend_view(request, sender, receiver):
    try:
        print(sender)
        print(receiver)

        sender_user = User.objects.get(username=sender)
        receiver_user = User.objects.get(username=receiver)

        print('got users')
        
        print(sender_user)
        print(receiver_user)
        
        friend_request = Friends(req_sender=sender_user, req_receiver=receiver_user, is_accepted=False)
        friend_request.save()

        print('made it')

        return render(request, 'add_friend.html', {'target': receiver})
    except:
        return redirect('error')


@login_required(login_url='/accounts/login/')
@require_http_methods(['GET', 'POST'])
def chat_view(request):




    return render(request, 'chat.html')


@require_GET
def error_view(request):
    return render(request, 'error.html')



