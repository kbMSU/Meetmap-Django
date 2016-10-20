from django import forms
from .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(label='Enter Username: ')
    password = forms.CharField(label='Enter Password: ')

class RegisterForm(forms.Form):
    username = forms.CharField(label='Enter a Username: ')
    password1 = forms.CharField(label='Create a Password: ')
    password2 = forms.CharField(label='Confirm Password: ')
    email = forms.CharField(label = 'Enter your email address: ')

class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('description', 'display_picture',)