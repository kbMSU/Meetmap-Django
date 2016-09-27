from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Enter Username: ')
    password = forms.CharField(label='Enter Password: ')

class RegisterForm(forms.Form):
    username = forms.CharField(label='Enter a Username: ')
    password1 = forms.CharField(label='Create a Password: ')
    password2 = forms.CharField(label='Confirm Password: ')
    email = forms.CharField(label = 'Enter your email address: ')
