from django.db import models
from django.apps import apps

class Location(models.Model):
    postal_code = models.IntegerField()
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

class Trip(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    num_participants = models.IntegerField()
    participant_list = models.ManyToManyField('users.CustomUser', related_name='trips') # can use user.trips.all() to get all trips for a user
    is_full = models.BooleanField()
    associated_college = models.CharField(max_length=255)
    departure_location = models.ForeignKey(Location, on_delete=models.RESTRICT, related_name='+')
    arrival_location = models.ForeignKey(Location, on_delete=models.RESTRICT, related_name='+')
    depature_time = models.DateTimeField()
    num_luggage_bags = models.IntegerField()
    num_trip_requests = models.IntegerField()
    trip_requests = models.ManyToManyField('SingleTripRequest', related_name='trip_requested') # can use single_trip_request.trip_requested.all() to get the trip that the single trip request is applying to
    blacklisted_users = models.ManyToManyField('users.CustomUser', related_name='blacklisted_trips') # can use user.blacklisted_trips.all() to get all trips a user is blacklisted from

    class Meta:
        ordering = ['created_on']
    
class MulipleTripRequest(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    departure_location = models.ForeignKey(Location, on_delete=models.RESTRICT, related_name='+')
    arrival_location = models.ForeignKey(Location, on_delete=models.RESTRICT, related_name='+')
    departure_time = models.DateTimeField()
    num_luggage_bags = models.IntegerField()
    trips_requested = models.ManyToManyField('SingleTripRequest', related_name='parent_trip_request') # can use single_trip_request.parent_trip_request.all() to get the multiple trip request that the single trip request is a part of

    class Meta:
        ordering = ['created_on']

class SingleTripRequest(models.Model):
    # has access to the trip it is requesting through 'trip_requested' related name on Trip
    # has access to the multiple trip request it is a part of through 'parent_trip_request' related name on MultipleTripRequest
    # TODO: Use signals (Django) to delete this object when its associated trip or multiple trip request is deleted
    # TODO: See any other relationships where this needs to be coded out
    num_members_accepted = models.IntegerField() # members from specific trip being applied to that have accepted this applicant
    trip_details_changed = models.BooleanField(default=False) # whether or not the trip details have changed since the request was made; relevant for notifying the user when they are confirming their acceptance

class ConfirmationRequest(models.Model):
    trip_request = models.ForeignKey(SingleTripRequest, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']
