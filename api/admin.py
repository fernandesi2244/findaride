from django.contrib import admin

from .models import TripRequest, Trip, Location, JoinRequest, ConfirmationRequest

admin.site.register(TripRequest)
admin.site.register(Trip)
admin.site.register(Location)
admin.site.register(JoinRequest)
admin.site.register(ConfirmationRequest)