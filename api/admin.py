from django.contrib import admin

from .models import TripRequest, Trip, Location, JoinRequest, TripUserDetails

admin.site.register(TripRequest)
admin.site.register(Trip)
admin.site.register(Location)
admin.site.register(JoinRequest)
admin.site.register(TripUserDetails)
