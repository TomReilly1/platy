from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, help_text='Required. Max length of 20 characters. Letters, digits and @/./+/-/_ only.')
    email = forms.EmailField(max_length=50, help_text='Required. Please enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
