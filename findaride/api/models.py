from django.db import models
from django.apps import apps

class Location(models.Model):
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=5, default='00000')
    #latitude = models.FloatField()
    #longitude = models.FloatField()

    def __str__(self):
        return self.address

class Trip(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    num_participants = models.IntegerField()
    participant_list = models.ManyToManyField('users.CustomUser', related_name='trips') # can use user.trips.all() to get all trips for a user
    is_full = models.BooleanField()
    departure_location = models.ForeignKey(Location, on_delete=models.RESTRICT, related_name='+')
    arrival_location = models.ForeignKey(Location, on_delete=models.RESTRICT, related_name='+')
    departure_time = models.DateTimeField()
    num_luggage_bags = models.IntegerField()
    num_join_requests = models.IntegerField()
    join_requests = models.ManyToManyField('JoinRequest', related_name='trip_requested') # can use join_request.trip_requested.all() to get the trip that the join request is applying to
    blacklisted_users = models.ManyToManyField('users.CustomUser', related_name='blacklisted_trips') # can use user.blacklisted_trips.all() to get all trips a user is blacklisted from
    college = models.CharField(max_length=5)

    class Meta:
        ordering = ['created_on']
    
# created when a user submits the trip request form from the dashboard
class TripRequest(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='trip_requests')
    departure_location = models.ForeignKey(Location, on_delete=models.RESTRICT, related_name='+')
    arrival_location = models.ForeignKey(Location, on_delete=models.RESTRICT, related_name='+')
    departure_time = models.DateTimeField()
    num_luggage_bags = models.IntegerField()
    join_requests = models.ManyToManyField('JoinRequest', related_name='parent_trip_request') # can use join_request.parent_trip_request.all() to get the trip request that the join request is a part of

    class Meta:
        ordering = ['created_on']

# request to join a group, possible multiple JoinRequests for one TripRequest
class JoinRequest(models.Model):
    # has access to the trip it is requesting through 'trip_requested' related name on Trip
    # has access to the trip request it is a part of through 'parent_trip_request' related name on TripRequest
    # TODO: Use signals (Django) to delete this object when its associated trip or trip request is deleted
    # TODO: See any other relationships where this needs to be coded out
    num_participants_accepted = models.IntegerField() # members from specific trip being applied to that have accepted this applicant
    participants_that_accepted = models.ManyToManyField('users.CustomUser', related_name='+')
    trip_details_changed = models.BooleanField(default=False) # whether or not the trip details have changed since the request was made; relevant for notifying the user when they are confirming their acceptance

    def assign(self, trip, tripRequest):
        trip.num_join_requests += 1
        trip.join_requests.add(self)
        trip.save()

        tripRequest.join_requests.add(self)
        tripRequest.save()

        # TODO: send email notification (or by preferred notification method) to trip participants that a new join request has been made
    
    def accept(self, user):
        """
        Mark that the given existing trip user has accepted this join request. If all trip members have accepted,
        then send a confirmation request to the user that requested the trip.
        """
        self.participants_that_accepted.add(user)
        self.num_participants_accepted += 1
        self.save()

        if self.num_participants_accepted == self.trip_requested.num_participants:
            # send confirmation request to user that requested trip
            ConfirmationRequest.objects.create(
                join_request=self
            )

            # TODO: send email notification (or by preferred notification method) to user that informing them that all participants have accepted them

class ConfirmationRequest(models.Model):
    join_request = models.ForeignKey(JoinRequest, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']
    
    def accept(self):
        # add the user to the trip they accepted and clean up the database
        trip = self.join_request.trip_requested
        tripRequest = self.join_request.parent_trip_request
        user = tripRequest.user

        trip.num_participants += 1
        trip.participant_list.add(user)
        trip.departure_time = self.join_request.parent_trip_request.departure_time # since requested departure time had to have been <= group departure time
        trip.num_luggage_bags += self.join_request.parent_trip_request.num_luggage_bags
        trip.num_join_requests -= 1
        trip.join_requests.remove(self.join_request)
        trip.save()

        # remove all other join requests from the trip request
        for joinRequest in tripRequest.join_requests.all():
            joinRequest.delete()
        
        tripRequest.delete()

        self.delete()

        # send email to team indicating confirmation and new trip details
