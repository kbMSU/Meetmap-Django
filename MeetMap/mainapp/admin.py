from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserProfile, Interest, Location, Event

admin.site.register(UserProfile)
admin.site.register(Interest)
admin.site.register(Location)
admin.site.register(Event)
