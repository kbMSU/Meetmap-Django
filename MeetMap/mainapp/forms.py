from django import forms
from django.forms import ModelForm
from mainapp.models import Event

class LoginForm(forms.Form):
    username = forms.CharField(label='Enter Username: ')
    password = forms.CharField(label='Enter Password: ')

class RegisterForm(forms.Form):
    username = forms.CharField(label='Enter a Username: ')
    password1 = forms.CharField(label='Create a Password: ')
    password2 = forms.CharField(label='Confirm Password: ')
    email = forms.CharField(label='Enter your email address: ')

class CreateEventForm(forms.ModelForm):
    street_number = forms.IntegerField(label='Street Number')
    street_name = forms.CharField(label='Street Name')
    suburb = forms.CharField(label='Suburb')
    city = forms.CharField(label='City')
    zipcode = forms.IntegerField(label='ZipCode')
    latitude = forms.FloatField(label='Latitude')
    longitude = forms.FloatField(label='Longitude')

    class Meta:
        model = Event
        exclude = ['creator','location']
        labels = {
            'name' : 'What do you call the event ?',
            'from_time' : 'When does the event start ?',
            'to_time' : 'When does the event end ?',
            'description' : 'Tell us a bit about your event',
            'picture' : 'Show a picture about your event',
            'is_private' : 'Is your event private ?',
            'interests' : 'Tag your event for others to find'
        }
        initial = {
            'is_private' : False
        }

class GoingToEventForm(forms.Form):
    event_id = forms.IntegerField()
