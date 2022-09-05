from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required




# Create your views here.
@login_required(login_url='/accounts/login/')
def home_view(request):
    return render(request, 'home.html')

