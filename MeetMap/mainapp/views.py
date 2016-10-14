from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from mainapp.models import UserProfile

from .forms import LoginForm, RegisterForm, CreateEventForm

def login(request):
    loginFailed = False
    usernameMissing = False
    passwordMissing = False
    invalidData = False

    loginForm = LoginForm()

    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                return HttpResponseRedirect('/map/')
            else:
                loginFailed = True
        else:
            if not loginForm.data['username']:
                usernameMissing = True
            if not loginForm.data['password']:
                passwordMissing = True
            if not usernameMissing and not passwordMissing:
                invalidData = True

    data = {
        'form':loginForm,
        'loginFailed':loginFailed,
        'usernameMissing':usernameMissing,
        'passwordMissing':passwordMissing,
        'invalidData':invalidData
    }

    return render(request, 'mainapp/login.html', data)

def signup(request):
    registerSuccess = False
    registerFailed = False
    usernameMissing = False
    usernameExists = False
    passwordMissing = False
    emailMissing = False
    passwordsDontMatch = False
    passwordTooShort = False
    invalidData = False

    registerForm = RegisterForm()

    if request.method == 'POST':
        registerForm = RegisterForm(request.POST)
        if registerForm.is_valid():
            username = registerForm.cleaned_data['username']
            password1 = registerForm.cleaned_data['password1']
            password2 = registerForm.cleaned_data['password2']
            email = registerForm.cleaned_data['email']
            if password1 == password2:
                if len(password1) > 5:
                    if not User.objects.filter(username=username).exists():
                        try:
                            newUser = User.objects.create_user(username, email, password1)
                            newUser.save()
                            newUserProfile = UserProfile(user=newUser)
                            newUserProfile.save()
                        except:
                            registerFailed = True
                        else:
                            registerSuccess = True
                            authenticate(username=username,password=password1)
                    else:
                        usernameExists = True
                else:
                    passwordTooShort = True
            else:
                passwordsDontMatch = True
        else:
            if not registerForm.data['username']:
                usernameMissing = True
            if not registerForm.data['password1']:
                passwordMissing = True
            if not registerForm.data['email']:
                emailMissing = True
            if not usernameMissing and not passwordMissing and not emailMissing:
                invalidData = True

    data = {
        'form':registerForm,
        'registerSuccess':registerSuccess,
        'registerFailed':registerFailed,
        'usernameMissing':usernameMissing,
        'usernameExists':usernameExists,
        'passwordMissing':passwordMissing,
        'emailMissing':emailMissing,
        'passwordsDontMatch':passwordsDontMatch,
        'passwordTooShort': passwordTooShort,
        'invalidData':invalidData
    }

    return render(request, 'mainapp/signup.html', data)

def createprofile(request):
    return render(request,'mainapp/createProfile.html')

def profile(request):
    return render(request,'mainapp/profile.html')

def map(request):
    eventForm = CreateEventForm()

    data = {
        'event_form':eventForm
    }

    return render(request,'mainapp/map.html',data)

def mymeets(request):
    return render(request,'mainapp/mymeets.html')

def create_event(request):
    success = False
    message = "Only POST request allowed on this URL"

    data = {
        'success':success,
        'message':message
    }
    return HttpResponse(
        data,
        content_type="application/json"
    )

    '''
    if request.method == 'POST':
        success = True
        message = "Event successfuly created !"

    data = {
        'success':success,
        'message':message
    }

    return HttpResponse(
        data,
        content_type="application/json"
    )
    '''
