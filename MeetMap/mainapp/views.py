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
from django.core import serializers

from .models import UserProfile, Location, Event , Interest

from .forms import LoginForm, RegisterForm, CreateEventForm, GoingToEventForm
from .forms import NotGoingToEventForm, DeleteEventForm, GetEventsForm
from .forms import ProfileForm, MyMeetsForm

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
Returns : Signup form if the user is yet to signup
Alternate : If signup is successful then the user can redirect to create profile page
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
            # Passwords must match
            if password1 == password2:
                # Password must have a minimum length
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

'''
Purpose : This view is to create a profile.
Returns : A ProfileForm if they are yet to complete their profile.
Alternate : If profile creation is successful user can redirect to map page.
'''
def createprofile(request):
    profileSuccess = False
    profileFailed = False
    descriptionMissing = False
    imageMissing = False
    invalidData = False

    profileForm = ProfileForm()

    if request.method == 'POST':
        profileForm = ProfileForm(request.POST)
        if profileForm.is_valid():
            description = profileForm.cleaned_data['description']
            picture = profileForm.cleaned_data['display_picture']

            try:
                profile = UserProfile.objects.get(user=request.user)
                if profileForm.data['description']:
                    profile.description = description
                    profile.save()
                if profileForm.data['display_picture']:
                    profile.display_picture = picture
                    profile.save()
            except:
                profileFailed = True
            else:
                profileSuccess = True
        else:
            if not profileForm.data['description']:
                descriptionMissing = True
            if not profileForm.data['display_picture']:
                imageMissing = True
            if not imageMissing and not descriptionMissing:
                invalidData = True

    data = {
        'form': profileForm,
        'profileSuccess': profileSuccess,
        'profileFailed': profileFailed,
        'descriptionMissing': descriptionMissing,
        'imageMissing': imageMissing,
        'invalidData': invalidData
    }

    return render(request, 'mainapp/createProfile.html', data)

'''
Purpose : This view is to view and update the profile
Returns : None
Alternate : Redirects to login if user is not authenticated
'''
def profile(request):
    if request.user.is_authenticated():
        return render(request, 'mainapp/profile.html')
    else:
        return HttpResponseRedirect('/login/')

'''
Purpose : This view is to see the map
Returns : CreateEventForm to create a new event by clicking on the map
Alternate : Redirects to login if user is not authenticated
'''
def map(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    eventForm = CreateEventForm()

    data = {
        'event_form':eventForm,
    }

    return render(request,'mainapp/map.html',data)

'''
Purpose : This view is to see their meets
Returns : A list of their meets
Alternate : Redirects to login if user is not authenticated
'''
def mymeets(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    current_user = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = MyMeetsForm(request.POST)
        form.is_valid()
        action_type = form.cleaned_data['action_type']
        meet_id = form.cleaned_data['event_id']
        meet = Event.objects.get(pk=meet_id)
        if action_type == "delete":
            meet.delete()
        else:
            current_user.events.remove(meet)
            current_user.save()

    joined_events = Event.objects.filter(
                                userprofile=current_user
                                ).exclude(
                                creator=current_user
                                )
    created_events = Event.objects.filter(creator=current_user)

    data = {
        'joined':joined_events,
        'created':created_events
    }

    return render(request, 'mainapp/mymeets.html', data)

'''
REST Endpoints start here
'''

'''
Purpose : Get the details required by the map page
'''
@api_view(['GET'])
def get_user_details(request):
    success = False

    try:
        current_user = UserProfile.objects.get(user=request.user)

        # Get all of the events of this user, minus the ones they created
        events = Event.objects.filter(
                            userprofile=current_user
                            )
        events_json = serializers.serialize("json", events, use_natural_foreign_keys=True,
                                            use_natural_primary_keys=True)

        # Get the users interests
        interests = Interest.objects.filter(userprofile=current_user)
        interests_json = serializers.serialize("json", interests,
                                                use_natural_foreign_keys=True,
                                                use_natural_primary_keys=True)

        # Get ALL interests
        all_interests = Interest.objects.all()
        all_interests_json = serializers.serialize("json", all_interests,
                                                    use_natural_foreign_keys=True,
                                                    use_natural_primary_keys=True)

        success = True
    except:
        success = False

    response = {
        'username':current_user.username,
        'events':events_json,
        'interests':interests_json,
        'all_interests':all_interests_json
    }

    if success:
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

'''
Purpose : User creates an event.
'''
@api_view(['POST'])
def create_event(request):
    saved = False
    message = "Error creating event"
    errors = None
    meet = None
    meet_json = None

    form = CreateEventForm(request.POST, request.FILES)
    if form.is_valid():
        street_number = form.cleaned_data['street_number']
        street_name = form.cleaned_data['street_name']
        suburb = form.cleaned_data['suburb']
        city = form.cleaned_data['city']
        zipcode = form.cleaned_data['zipcode']
        latitude = form.cleaned_data['latitude']
        longitude = form.cleaned_data['longitude']

        name = form.cleaned_data['name']
        from_time = form.cleaned_data['from_time']
        to_time = form.cleaned_data['to_time']
        description = form.cleaned_data['description']
        picture = form.cleaned_data['picture']
        is_private = form.cleaned_data['is_private']
        interests = form.cleaned_data['interests']

        location = Location(street_number=street_number,street_name=street_name,
            suburb=suburb,city=city,zipcode=zipcode,latitude=latitude,
            longitude=longitude)
        location.save()

        current_user = request.user.username
        profile = UserProfile.objects.get(username=current_user)

        meet = Event(name=name,from_time=from_time,to_time=to_time,
            description=description,is_private=is_private,
            location=location,creator=profile,picture=picture)
        meet.save()
        meet.interests = interests
        meet.save()
        profile.events.add(meet)
        profile.save()

        saved = True
        message = "Event successfuly created !"

        meet_json = serializers.serialize("json", [meet],
                                            use_natural_foreign_keys=True,
                                            use_natural_primary_keys=True)
    else:
        saved = False
        message = "All fields required."
        errors = form.errors

    data = {
        'saved':saved,
        'message':message,
        'errors':errors,
        'meet':meet_json
    }

    if saved:
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

'''
Purpose : User RSVP to an event.
'''
@api_view(['POST'])
def going_to_event(request):
    success = True
    message = 'You are now going to the event !'

    try:
        form = GoingToEventForm(request.POST)
        form.is_valid()
        meet_id = form.cleaned_data['event_id']
        meet = Event.objects.get(pk=meet_id)

        current_user = UserProfile.objects.get(user=request.user)
        current_user.events.add(meet)
        current_user.save()
    except:
        success = False
        message = "Error RSVP'ing to the event"

    data = {
        'success':success,
        'message':message
    }

    if success:
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

'''
Purpose : User is no longer going to an event.
'''
@api_view(['POST'])
def not_going_to_event(request):
    success = True
    message = 'You are no longer going to the event !'

    try:
        form = NotGoingToEventForm(request.POST)
        form.is_valid()
        meet_id = form.cleaned_data['event_id']
        meet = Event.objects.get(pk=meet_id)

        current_user = UserProfile.objects.get(user=request.user)
        current_user.events.remove(meet)
        current_user.save()
    except:
        success = False
        message = "Error leaving the event"

    data = {
        'success':success,
        'message':message
    }

    if success:
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

'''
Purpose : User deletes an event.
'''
@api_view(['POST'])
def delete_event(request):
    success = True
    message = 'The event has been deleted !'

    try:
        form = NotGoingToEventForm(request.POST)
        print(form)
        form.is_valid()
        meet_id = form.cleaned_data['event_id']
        meet = Event.objects.get(pk=meet_id)
        meet.delete()
    except:
        success = False
        message = "Error deleting the event"

    data = {
        'success':success,
        'message':message
    }

    if success:
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

'''
Purpose : Get events corresponding to a list of interests. To show on the map.
'''
@api_view(['POST'])
def get_events(request):
    success = False

    try:
        form = GetEventsForm(request.POST)
        form.is_valid()
        selected_interests = form.cleaned_data['interests']
        interests = Interest.objects.filter(interest_name__in=selected_interests)

        events = Event.objects.filter(interests__in=interests)
        events_json = serializers.serialize("json", events,
                                            use_natural_foreign_keys=True,
                                            use_natural_primary_keys=True)
        success = True
    except:
        success = False

    data = {
        'events':events_json
    }

    if success:
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

def get_profile(request):
    print("here")
    if request.user.is_authenticated():
        print("whatduotpfsjfsjdlkjfdsa")
        my_profile = serializers.serialize("json", UserProfile.objects.filter(user=request.user),
                                                   use_natural_foreign_keys=True, use_natural_primary_keys=True)
        #print(my_profile)
        #print(serialized_profile)

        return HttpResponse(my_profile, content_type='application/json')
    else:
        return HttpResponseRedirect('/login/')
