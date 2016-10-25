from django.db import models
from django.contrib.auth.models import User


class InterestManager(models.Manager):
    def get_by_natural_key(self, interest_name):
        return self.get(interest_name=interest_name)


class Interest(models.Model):
    objects = InterestManager()

    interest_name = models.CharField(max_length=100)

    def natural_key(self):
        return self.interest_name

    def __str__(self):
        return self.interest_name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_picture = models.ImageField()
    description = models.CharField(max_length=500)
    interests = models.ManyToManyField('Interest', blank=True)
    whitelist = models.ManyToManyField('self', blank=True)
    blacklist = models.ManyToManyField('self', blank=True)
    events = models.ManyToManyField('Event', blank=True)

    def __str__(self):
        return self.user.username


class Location(models.Model):
    street_number = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100)
    suburb = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    def __str__(self):
        return self.street_number + " " + \
               self.street_name + ", " + \
               self.suburb + ", " + \
               self.city + " " + \
               str(self.zipcode)

class EventManager(models.Manager):
    def get_by_natural_key(self, interest_name):
        return self.get(interest_name=interest_name)

class Event(models.Model):
    objects = EventManager()

    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    time = models.DateTimeField()
    duration = models.DurationField()
    description = models.CharField(max_length=500)
    picture = models.ImageField(null=True)
    is_private = models.BooleanField()
    interests = models.ManyToManyField(Interest)
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def natural_key(self):
        return self.name

    def __str__(self):
        return self.name + " | Creator: " + self.creator.user.username
