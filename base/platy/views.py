import requests
import json

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.db.models import Q
from django.contrib.auth.models import User
# from django.contrib.postgres import search

from platy.models import Friends
from platy.forms import SearchForm, SignUpForm


# Create your views here.
@require_GET
def landing_view(request):
    return render(request, 'landing.html')


@login_required(login_url='/accounts/login/')
@require_GET
def home_view(request):
    # print(requests.get('http://localhost:8000/api/get-users').text)
    print(request.user.id)

    req_pending = Friends.objects.filter(req_sender_id=request.user.id).filter(is_accepted=False)
    req_received = Friends.objects.filter(req_receiver_id=request.user.id).filter(is_accepted=False)
    friends = Friends.objects.filter(is_accepted=True)\
        .filter(Q(req_sender_id=request.user.id) | Q(req_receiver_id=request.user.id))
    
    print(req_pending)
    print(req_received)
    # print(req_pending[0].req_receiver.username)
    # print(req_received[0].req_sender.username)
    print(friends)

    # pending_req_list = list(req_pending)
    pending_req_list = list(map(lambda obj: obj.req_receiver.username, req_pending))
    print(pending_req_list)
    received_req_list = list(req_received)
    # received_req_list = list(map(lambda obj: obj.req_sender.username, req_received))
    # print(received_req_list)
    friends_list = []
    for f in friends:
        # print(f.req_receiver)
        if f.req_receiver == request.user:
            friends_list.append(f.req_sender)
        elif f.req_sender == request.user:
            friends_list.append(f.req_receiver)
        else:
            raise 'CUSTOM ERROR: Unkown error in creating friends list'
    # friends_list = list(map(lambda obj: obj.username, friends))
    print(friends_list)


    return render(request, 'home.html', {
        'friends': friends_list,
        'pending': pending_req_list,
        'received': received_req_list
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





@require_GET
def error_view(request):
    return render(request, 'error.html')



