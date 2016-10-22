from django.db import models
from django.contrib.auth.models import User

# This class helps with serialization of foreign keys
# Makes foreign key return values rather than an Integer (Primary Key)
class InterestManager(models.Manager):
    def get_by_natural_key(self, interest_name):
        return self.get(interest_name=interest_name)

class Interest(models.Model):
    objects = InterestManager()

    interest_name = models.CharField(max_length=100)

    def natural_key(self):
        return(self.interest_name)

    def __str__(self):
        return self.interest_name

class UserProfileManager(models.Manager):
    def get_by_natural_key(self, username):
        return self.get(username=username)

class UserProfile(models.Model):
    objects = UserProfileManager()

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100,default="")
    display_picture = models.ImageField(null=True,upload_to = 'profile_pic_folder/')
    description = models.CharField(max_length=500,default="",null=True)
    interests = models.ManyToManyField(Interest)
    whitelist = models.ManyToManyField('self')
    blacklist = models.ManyToManyField('self')
    events = models.ManyToManyField('Event')

    def natural_key(self):
        return(self.username)

    def __str__(self):
        return self.user.username

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
    from_time = models.DateTimeField()
    to_time = models.DateTimeField()
    description = models.CharField(max_length=500,default="")
    picture = models.ImageField(null=True,upload_to = 'event_pic_folder/')
    is_private = models.BooleanField(default=False)
    interests = models.ManyToManyField(Interest)
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " | Creator: " + self.creator.user.username
