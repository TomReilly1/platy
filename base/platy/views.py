from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth.models import User
# from django.contrib.postgres import search

from platy.forms import SearchForm, SignUpForm


# Create your views here.
@require_GET
def landing_view(request):
    return render(request, 'landing.html')


@login_required(login_url='/accounts/login/')
@require_GET
def home_view(request):
    return render(request, 'home.html')

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
            search_request = User.objects.filter(username__startswith=search_str)[:5]
            
            user_list = list(map(lambda obj: {'name':obj.username}, search_request))

            return render(request, 'search.html', {'form': form, 'userlist': user_list})
    # GET Method
    else:
        form = SearchForm()
        return render(request, 'search.html', {'form': form, 'userlist': [{'name':''}]})

    return render(request, 'search.html', {'form': form})

