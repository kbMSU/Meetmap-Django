from django.db import models
from django.contrib.auth.models import User

class Interest(models.Model):
    interest_name = models.CharField(max_length=100)

    def __str__(self):
        return self.interest_name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_picture = models.ImageField()
    description = models.CharField(max_length=500)
    interests = models.ManyToManyField(Interest, blank=True)
    whitelist = models.ManyToManyField('self', blank=True)
    blacklist = models.ManyToManyField('self', blank=True)
    events = models.ManyToManyField('Event', blank=True)

    def __str__(self):
        return self.user.username

# This class helps with serialization of foreign keys
# Makes foreign key return values rather than an integer
class LocationManager(models.Manager):
    def get_by_natural_key(self, latitude, longitude, street_number, street_name, suburb,
                           city, zipcode):
        return self.get(latitude = latitude,
                        longitude = longitude,
                        street_number = street_number,
                        street_name = street_name,
                        suburb = suburb,
                        city = city,
                        zipcode = zipcode)
class Location(models.Model):
    objects = LocationManager()

    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    street_number = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100)
    suburb = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.IntegerField()

    def natural_key(self):
        return(self.latitude, self.longitude, self.street_number, self.street_name, self.suburb,
               self.city, self.zipcode)


    def __str__(self):
        return self.street_number + " " + \
               self.street_name + ", " + \
               self.suburb + ", " + \
               self.city + " " + \
               str(self.zipcode)

class Event(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    time = models.DateTimeField()
    duration = models.DurationField()
    description = models.CharField(max_length=500)
    picture = models.ImageField(null=True)
    is_private = models.BooleanField()
    interests = models.ManyToManyField(Interest)
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " | Creator: " + self.creator.user.username
