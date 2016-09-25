from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate, login

from .forms import LoginForm

def login(request):
    # Keeps track of whether the login failed
    loginFailed = False
    # Keeps track of whether the username is missing
    usernameMissing = False
    # Keeps track of whether the password is missing
    passwordMissing = False
    # Keeps track of whether the fields are entered properly
    invalidData = False

    # We will be displaying a LoginForm on this page
    loginForm = LoginForm()

    # They can make either a POST or a GET request to this page
    if request.method == 'POST':
        # When the LoginForm is "submitted" by the HTML
        # it will make a POST request back to this same page.
        # The POST request will contain the filled out form.
        # Here we are getting that form
        loginForm = LoginForm(request.POST)
        # Django forms can check if everything is filled out
        # is_valid() will return False if ALL fields are not filled out
        # and none of the fields are empty spaces. Ex. "       "
        # If you need only some of the fields filled out then this method
        # is useless and you have to check each field manually.
        # I show you how to do that in the else part
        if loginForm.is_valid():
            # Get the username from the form
            username = loginForm.cleaned_data['username']
            # Get the password from the form
            password = loginForm.cleaned_data['password']
            # Ask Django to see if this user exists
            # If the user exists, this method will authenticate/login the user
            user = authenticate(username=username,password=password)
            # If the user does exist
            if user is not None:
                # Go to the main page
                return HttpResponseRedirect('/main/')
            # If the user does NOT exist
            else:
                # Tell the HTML that username/password is invalid
                loginFailed = True
        # If the form is not filled
        # Here we will check each field to see what is missing and
        # display the proper message
        else:
            # If username is missing
            if not loginForm.data['username']:
                # Mark username as missing
                usernameMissing = True
            # If password is missing
            if not loginForm.data['password']:
                # Mark password as missing
                passwordMissing = True
            # Maybe neither the username or password are missing but
            # the form is still considered invalid by Django
            # This can happen if for example one of the fields is just an
            # string of blank spaces. Ex. "      "
            # So we have to account for this
            if not usernameMissing and not passwordMissing:
                invalidData = True


    # This is the data that the HTML expects. It is just a JSON object
    # The HTML can use any of this data
    data = {
        # This LoginForm will either be the new one we created
        # at the start of the function
        # OR
        # the form that we got from the POST request that contains
        # the already filled out information
        'form':loginForm,
        # If loginFailed is true the HTML will display an
        # appropriat error
        'loginFailed':loginFailed,
        # If usernameMissing is true the HTML will display an
        # appropriat error
        'usernameMissing':usernameMissing,
        # If passwordMissing is true the HTML will display an
        # appropriat error
        'passwordMissing':passwordMissing,
        # If passwordMissing is true the HTML will display an
        # appropriat error
        'invalidData':invalidData
    }

    # The render method takes 3 parameters.
    # The request, the HTML to render, the JSON data to use in the page
    # The data field is optional
    return render(request, 'mainapp/login.html', data)

def signup(request):
    return render(request, 'mainapp/signup.html')

def main(request):
    return render(request, 'mainapp/main.html')
