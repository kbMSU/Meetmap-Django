from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Enter Username: ')
    password = forms.CharField(label='Enter Password: ')
