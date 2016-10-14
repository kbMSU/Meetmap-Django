from django.db import models
from django.contrib.auth.models import User

class Interest(models.Model):
    interest_name = models.CharField(max_length=100)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_picture = models.ImageField()
    description = models.CharField(max_length=500)
    interests = models.ManyToManyField(Interest)
    whitelist = models.ManyToManyField('self')
    blacklist = models.ManyToManyField('self')
    events = models.ManyToManyField('Event')

class Location(models.Model):
    street_number = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100)
    suburb = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

class Event(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    from_time = models.DateTimeField()
    to_time = models.DateTimeField(null=True)
    description = models.CharField(max_length=500)
    picture = models.ImageField(null=True)
    is_private = models.BooleanField()
    interests = models.ManyToManyField(Interest)
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
