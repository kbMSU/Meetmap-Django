from django.db import models
from django.contrib.auth.models import User

class Interest(models.Model):
    interest_name = models.CharField(max_length=100)

    def __str__(self):
        return self.interest_name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100,default="")
    display_picture = models.ImageField(null=True,upload_to = 'profile_pic_folder/')
    description = models.CharField(max_length=500,default="",null=True)
    interests = models.ManyToManyField(Interest)
    whitelist = models.ManyToManyField('self')
    blacklist = models.ManyToManyField('self')
    events = models.ManyToManyField('Event')

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
        return ""+self.street_number+" "+self.street_name

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
        return self.name
