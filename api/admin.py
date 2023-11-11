from django.contrib import admin

from .models import TripRequest, Trip, Location

admin.site.register(TripRequest)
admin.site.register(Trip)
admin.site.register(Location)