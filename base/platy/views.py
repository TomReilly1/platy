from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from platy.forms import SignUpForm



# Create your views here.

def landing_view(request):
    return render(request, 'landing.html')


@login_required(login_url='/accounts/login/')
def home_view(request):
    return render(request, 'home.html')


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

