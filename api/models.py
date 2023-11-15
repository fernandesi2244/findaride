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
    blacklisted_users = models.ManyToManyField('users.CustomUser', related_name='blacklisted_trips', null=True, blank=True) # can use user.blacklisted_trips.all() to get all trips a user is blacklisted from
    college = models.CharField(max_length=5)

    class Meta:
        ordering = ['created_on']
    
# created when a user submits the trip request form from the dashboard
class TripRequest(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='trip_requests')
    departure_location = models.ForeignKey(Location, on_delete=models.RESTRICT, related_name='+')
    arrival_location = models.ForeignKey(Location, on_delete=models.RESTRICT, related_name='+')
    earliest_departure_time = models.DateTimeField()
    latest_departure_time = models.DateTimeField()
    num_luggage_bags = models.IntegerField()
    comment = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['created_on']

# request to join a group, possible multiple JoinRequests for one TripRequest
class JoinRequest(models.Model):
    # TODO: Use signals (Django) to delete this object when its associated trip or trip request is deleted
    # TODO: See any other relationships where this needs to be coded out
    num_participants_accepted = models.IntegerField(default=0) # members from specific trip being applied to that have accepted this applicant
    participants_that_accepted = models.ManyToManyField('users.CustomUser', related_name='+')
    trip_details_changed = models.BooleanField(default=False) # whether or not the trip details have changed since the request was made; relevant for notifying the user when they are confirming their acceptance
    trip_request = models.ForeignKey('TripRequest', related_name='join_requests', null=True, blank=True, on_delete=models.CASCADE) 
    trip = models.ForeignKey('Trip', related_name='join_requests', null=True, blank=True, on_delete=models.CASCADE) 
    
    def accept(self, user):
        """
        Mark that the given existing trip user has accepted this join request. If all trip members have accepted,
        then send a confirmation request to the user that requested the trip.
        """
        if user in self.participants_that_accepted.all():
            return
        
        self.participants_that_accepted.add(user)
        self.num_participants_accepted += 1
        self.save()

        # if new member joins before other member is accepted, how do we deal with pending join requests?
        # if all trip members previously accepted -> good to go
        # if not all trip members previously accepted -> need to have new member accept request as well
        if self.num_participants_accepted == self.trip.num_participants:
            # note that user a and b may both be sent a confirmation request around the same time

            # make sure that there is not already a confirmation request for this join request (user a gets in and accepts user b before b accepts their confirmation request)
            if ConfirmationRequest.objects.filter(join_request=self).exists():
                return

            # odd-ball case where user b is already in group but a hasn't refreshed their page yet and tries to accept user b's join request
            if self.trip.participant_list.filter(pk=self.trip_request.user.pk).exists():
                return

            # send confirmation request to user that requested trip
            ConfirmationRequest.objects.create(
                join_request=self
            )

            # Don't delete the join request yet, since we need to display its status to the trip group based on the associated confirmation request

            # TODO: send email notification (or by preferred notification method) to user that informing them that all participants have accepted them

class ConfirmationRequest(models.Model):
    join_request = models.OneToOneField(JoinRequest, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']
    
    def accept(self):
        # add the user to the trip they accepted and clean up the database
        trip = self.join_request.trip
        tripRequest = self.join_request.trip_request
        user = tripRequest.user

        trip.num_participants += 1
        trip.participant_list.add(user)
        trip.num_luggage_bags += self.join_request.trip_request.num_luggage_bags
        trip.num_join_requests -= 1
        trip.save()

        # remove all join requests from the trip request
        for joinRequest in tripRequest.join_requests.all():
            joinRequest.delete()
        
        tripRequest.delete()

        self.delete()

        # send email to team indicating confirmation and new trip details

    def reject(self):
        # remove the user from the trip request and clean up the database
        tripRequest = self.join_request.trip_request
        user = tripRequest.user

        trip = self.join_request.trip
        trip.num_join_requests -= 1
        trip.blacklisted_users.add(user)
        trip.save()

        self.join_request.delete()

        self.delete()
