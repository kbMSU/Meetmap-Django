from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate, login

from .forms import LoginForm

def login(request):
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect('/main/')
            else:
                return HttpResponseRedirect('/signup/')
    else:
        loginForm = LoginForm()

    return render(request, 'mainapp/login.html', {'form':loginForm})

def signup(request):
    template = loader.get_template('mainapp/signup.html')
    return HttpResponse(template.render(request))

def main(request):
    template = loader.get_template('mainapp/main.html')
    return HttpResponse(template.render(request))
