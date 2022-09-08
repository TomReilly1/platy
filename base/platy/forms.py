from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, help_text='Enter a username with a max length of 20 characters. Letters, digits and @/./+/-/_ only.')
    email = forms.EmailField(max_length=50, help_text='Enter a valid email address.')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, help_text='Your password must contain at least 8 characters and cannot be entirely numeric. Your password should not be similar to personal information or be a commonly used password.')
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, help_text='Enter the same password as above for verification.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=30)

