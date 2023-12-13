from django.db import models
from django.utils.timezone import make_aware
from api.utils import send_trip_joined_email, send_member_left_email, send_absolute_rejection_email
from geopy.distance import geodesic

import datetime

class Location(models.Model):
    address = models.CharField(max_length=255)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    def __str__(self):
        return self.address

class Trip(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    num_participants = models.IntegerField()
    participant_list = models.ManyToManyField('users.CustomUser', related_name='trips', blank=True) # can use user.trips.all() to get all trips for a user
    is_full = models.BooleanField()
    departure_location = models.ForeignKey(Location, on_delete=models.RESTRICT, related_name='+')
    arrival_location = models.ForeignKey(Location, on_delete=models.RESTRICT, related_name='+')
    earliest_departure_time = models.DateTimeField()
    latest_departure_time = models.DateTimeField()
    num_luggage_bags = models.IntegerField()
    blacklisted_users = models.ManyToManyField('users.CustomUser', related_name='blacklisted_trips', blank=True) # can use user.blacklisted_trips.all() to get all trips a user is blacklisted from
    college = models.CharField(max_length=5)

    class Meta:
        ordering = ['created_on']

    def remove_user(self, user):
        """
        Remove the given user from the trip, and if the trip is now empty, delete it.
        """
        self.participant_list.remove(user)
        self.num_participants -= 1
        self.blacklisted_users.add(user)
        
        corresponding_trip_user_details = TripUserDetails.objects.get(trip=self, user=user)
        self.num_luggage_bags -= corresponding_trip_user_details.num_luggage_bags
        corresponding_trip_user_details.delete()

        self.save()

        if self.num_participants == 0:
            # delete all join requests to this trip
            for join_request in self.join_requests.all():
                if joinRequest.trip_request.join_requests.count() == 1:
                    send_absolute_rejection_email(joinRequest.trip_request.user)
                    joinRequest.trip_request.delete()
                join_request.delete()
            self.delete()
            return

        send_member_left_email(self.participant_list, self)

        # mark all join requests to this trip as trip details changed
        for joinRequest in self.join_requests.all():
            joinRequest.trip_details_changed = True
            joinRequest.save()

        self.save()
    
    def toggle_is_full_setting(self):
        self.is_full = not self.is_full
        self.save()

        if self.is_full:
            # clear all join requests to this trip
            for joinRequest in self.join_requests.all():
                # if the trip request associated with this join request has no more join requests, then delete it
                if joinRequest.trip_request.join_requests.count() == 1:
                    send_absolute_rejection_email(joinRequest.trip_request.user)
                    joinRequest.trip_request.delete()
                joinRequest.delete()

                self.save()

class TripUserDetails(models.Model):
    trip = models.ForeignKey('Trip', related_name='trip_user_details', on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUser', related_name='trip_user_details', on_delete=models.CASCADE)
    num_luggage_bags = models.IntegerField()
    trip_nickname = models.CharField(max_length=255, blank=True)

# created when a user submits the trip request form from the dashboard
class TripRequest(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='trip_requests')
    trip_nickname = models.CharField(max_length=255, blank=True)
    num_luggage_bags = models.IntegerField()
    comment = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['created_on']

# request to join a group, possible multiple JoinRequests for one TripRequest
class JoinRequest(models.Model):
    # TODO: Use signals (Django) to delete this object when its associated trip or trip request is deleted
    # TODO: See any other relationships where this needs to be coded out
    num_participants_accepted = models.IntegerField(default=0) # members from specific trip being applied to that have accepted this applicant
    participants_that_accepted = models.ManyToManyField('users.CustomUser', related_name='+', blank=True)
    trip_details_changed = models.BooleanField(default=False) # whether or not the trip details have changed since the request was made; relevant for notifying the user when they are looking at their join requests
    trip_request = models.ForeignKey('TripRequest', related_name='join_requests', null=True, blank=True, on_delete=models.CASCADE) 
    trip = models.ForeignKey('Trip', related_name='join_requests', null=True, blank=True, on_delete=models.CASCADE)
    
    def accept(self, user):
        """
        Mark that the given existing trip user has accepted this join request. If all trip members have accepted,
        then add the user to the trip.
        """
        if user in self.participants_that_accepted.all():
            return
        
        # make sure that the associated trip request still exists
        if not self.trip_request:
            return

        if self.trip.is_full:
            if self.trip_request.join_requests.count() == 1:
                send_absolute_rejection_email(self.trip_request.user)
                self.trip_request.delete()
        
            # TODO: Down the line, we should ask if they want to have more requests sent out. If not or if there are no more possible
            # trips they can join, then we should create a new trip for them.

            self.delete()
            return
        
        self.participants_that_accepted.add(user)
        self.num_participants_accepted += 1
        self.save()

        # if new member joins before other member is accepted, how do we deal with pending join requests?
        # if all trip members previously accepted -> good to go
        # if not all trip members previously accepted -> need to have new member accept request as well
        if self.num_participants_accepted == self.trip.num_participants:
            # odd-ball case where user b is already in group but a hasn't refreshed their page yet and tries to accept user b's join request - this shouldn't be possible assuming appropriate measures taken at frontend
            if self.trip.participant_list.filter(pk=self.trip_request.user.pk).exists():
                return

            # add the user to the trip they accepted and clean up the database
            trip = self.trip
            tripRequest = self.trip_request
            user = tripRequest.user

            trip.num_participants += 1
            trip.participant_list.add(user)
            trip.num_luggage_bags += tripRequest.num_luggage_bags

            trip.save()

            TripUserDetails.objects.create(
                trip=trip,
                user=user,
                num_luggage_bags=tripRequest.num_luggage_bags,
                trip_nickname=tripRequest.trip_nickname
            )

            # remove all join requests from the trip request
            for joinRequest in tripRequest.join_requests.all():
                joinRequest.delete()
            
            tripRequest.delete()

            self.delete()

            # send email to team indicating new team along with details
            send_trip_joined_email(user, trip.participant_list)

            # mark all other join requests to this trip as trip details changed
            for joinRequest in trip.join_requests.all():
                joinRequest.trip_details_changed = True
                joinRequest.save()
    
    def reject(self):
        """
        Remove this join request from the trip, decrement the number of join requests for the trip, and
        add the user to the trip's blacklist.
        """
        trip = self.trip
        trip.blacklisted_users.add(self.trip_request.user)
        trip.save()

        # If this was the last join request for the trip request, then delete the trip request
        if self.trip_request.join_requests.count() == 1:
            send_absolute_rejection_email(self.trip_request.user)
            self.trip_request.delete()
        
        # TODO: Down the line, we should ask if they want to have more requests sent out. If not or if there are no more possible
        # trips they can join, then we should create a new trip for them.

        self.delete()

@staticmethod
def create_new_trip(trip_request):
    new_trip = Trip.objects.create(
        num_participants=1,
        departure_location=trip_request.departure_location,
        arrival_location=trip_request.arrival_location,
        earliest_departure_time=trip_request.earliest_departure_time,
        latest_departure_time=trip_request.latest_departure_time,
        num_luggage_bags=trip_request.num_luggage_bags,
        college=trip_request.user.college,
        is_full=False
    )
    new_trip.participant_list.add(trip_request.user)
    TripUserDetails.objects.create(
        trip=new_trip,
        user=trip_request.user,
        num_luggage_bags=trip_request.num_luggage_bags,
        trip_nickname=trip_request.trip_nickname
    )

    return new_trip