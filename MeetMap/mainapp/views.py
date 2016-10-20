from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.http import Http404
from django.template import loader
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from mainapp.models import UserProfile, Location, Event , Interest
from django.core import serializers

from .forms import LoginForm, RegisterForm, CreateEventForm

'''
Purpose : This view is for logging in.
Returns : LoginForm if the user is yet to login.
Alternate : Redirects to Map view if the login is successfuly
'''
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
                auth_login(request,user)
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

'''
Purpose : This view is for signup
Returns : Signup form
Alternate : None
'''
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
                            newUserProfile = UserProfile(user=newUser,username=username)
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
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    eventForm = CreateEventForm()

    data = {
        'event_form':eventForm
    }

    return render(request,'mainapp/map.html',data)

def get_events(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    current_user = UserProfile.objects.filter(user=request.user)
    #print("User: " + str(current_user.values()[0]))
    interests = Interest.objects.filter(userprofile=current_user)
    #print("Interests: " + str(interests.values()[0]))

    if interests: #if the user has interests, only render map with events of that interest
        interestArray = []
        for interest in interests:
            interestArray += [interest.id]
        #print("InterestArray: " + str(interestArray))

        events = serializers.serialize("json", Event.objects.filter(interests__in=interestArray),
                                       use_natural_foreign_keys=True, use_natural_primary_keys=True)
        print(events)
        return HttpResponse(events, content_type='application/json')
    else: # if the user has no interests, render all events
        events = serializers.serialize("json", Event.objects.all(),
                                       use_natural_foreign_keys=True, use_natural_primary_keys=True)
        return HttpResponse(events, content_type='application/json')

def mymeets(request):
    return render(request,'mainapp/mymeets.html')

'''
Purpose : This view is for creating events with POST.
Returns : JSON response indicating whether the save is successful or failed
Alternate : 404 error if the user tries to reach this view with a GET
'''
def create_event(request):
    saved = False
    message = "Error creating event"
    errors = None

    if request.method == 'POST':
        form = CreateEventForm(request.POST, request.FILES)

        if form.is_valid():
            street_number = form.cleaned_data['street_number']
            street_name = form.cleaned_data['street_name']
            suburb = form.cleaned_data['suburb']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']

            name = form.cleaned_data['name']
            from_time = form.cleaned_data['from_time']
            to_time = form.cleaned_data['to_time']
            description = form.cleaned_data['description']
            picture = form.cleaned_data['picture']
            is_private = form.cleaned_data['is_private']
            interests = form.cleaned_data['interests']

            location = Location(street_number=street_number,street_name=street_name,
                suburb=suburb,city=city,zipcode=zipcode,latitude=0,longitude=0)
            location.save()

            current_user = request.user.username
            profile = UserProfile.objects.get(username=current_user)

            meet = Event(name=name,from_time=from_time,to_time=to_time,
                description=description,is_private=is_private,
                location=location,creator=profile)
            meet.save()
            meet.interests = interests
            meet.save()

            saved = True
            message = "Event successfuly created !"
        else:
            saved = False
            message = "All fields required."
            errors = form.errors
    else:
        '''
        The user cannot visit this view from the browser. This view is only for
        saving events with a POST request
        '''
        raise Http404

    data = {
        'saved':saved,
        'message':message,
        'errors':errors,
    }

    return JsonResponse(data)
