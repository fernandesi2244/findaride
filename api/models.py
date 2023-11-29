from django.db import models
from django.apps import apps
from django.utils.timezone import make_aware
from api.utils import send_confirm_email

import datetime

class Location(models.Model):
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=12, default='00000') # see https://www.quora.com/What-is-the-maximum-number-of-digits-in-a-zipcode-postal-code-for-a-place-in-this-universe
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
    num_join_requests = models.IntegerField()
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
            # delete associated stuff like TripUserDetails
            self.delete()
            return

        curr_utc_time = make_aware(datetime.datetime.utcnow())
        print(curr_utc_time)
        print(self.earliest_departure_time)

        # if the trip is less than 3 hours away, then don't change the trip timespan
        if curr_utc_time + datetime.timedelta(hours=3) > self.earliest_departure_time:
            return

        # get max min time and min max time of all users in trip to form new trip timespan
        self.earliest_departure_time = TripUserDetails.objects.filter(trip=self).aggregate(models.Max('earliest_departure_time'))['earliest_departure_time__max']
        self.latest_departure_time = TripUserDetails.objects.filter(trip=self).aggregate(models.Min('latest_departure_time'))['latest_departure_time__min']

        self.save()

class TripUserDetails(models.Model):
    trip = models.ForeignKey('Trip', related_name='user_timespans', on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUser', related_name='trip_timespans', on_delete=models.CASCADE)

    earliest_departure_time = models.DateTimeField()
    latest_departure_time = models.DateTimeField()

    num_luggage_bags = models.IntegerField()
    
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
    participants_that_accepted = models.ManyToManyField('users.CustomUser', related_name='+', blank=True)
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
            send_confirm_email(self.trip_request.user, self.trip)

            # Don't delete the join request yet, since we need to display its status to the trip group based on the associated confirmation request
            
            # TODO: send email notification (or by preferred notification method) to user that informing them that all participants have accepted them
    
    def reject(self):
        """
        Remove this join request from the trip, decrement the number of join requests for the trip, and
        add the user to the trip's blacklist.
        """
        trip = self.trip
        trip.num_join_requests -= 1
        trip.blacklisted_users.add(self.trip_request.user)
        trip.save()

        # If this was the last join request for the trip request, then create a new trip for the user
        num_confirmation_requests = ConfirmationRequest.objects.filter(join_request__trip_request_id=self.trip_request.id).count()
        if self.trip_request.join_requests.count() == 1 and num_confirmation_requests == 0:
            new_trip = Trip.objects.create(
                num_participants=1,
                departure_location=self.trip_request.departure_location,
                arrival_location=self.trip_request.arrival_location,
                earliest_departure_time=self.trip_request.earliest_departure_time,
                latest_departure_time=self.trip_request.latest_departure_time,
                num_luggage_bags=self.trip_request.num_luggage_bags,
                num_join_requests=0,
                college=self.trip_request.user.college,
                is_full=False
            )
            new_trip.participant_list.add(self.trip_request.user)
            TripUserDetails.objects.create(
                trip=new_trip,
                user=self.trip_request.user,
                earliest_departure_time=self.trip_request.earliest_departure_time,
                latest_departure_time=self.trip_request.latest_departure_time,
                num_luggage_bags=self.trip_request.num_luggage_bags
            )

            # delete the associated trip request
            self.trip_request.delete()
        
        # TODO: Down the line, we should ask if they want to have more requests sent out. If not or if there are no more possible
        # trips they can join, then we should create a new trip for them.

        self.delete()

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

        # update the trip's timespan to be the intersection of the trip's timespan and the user's timespan (max possible overlap)
        trip.earliest_departure_time = max(trip.earliest_departure_time, tripRequest.earliest_departure_time)
        trip.latest_departure_time = min(trip.latest_departure_time, tripRequest.latest_departure_time)
        trip.save()

        TripUserDetails.objects.create(
            trip=trip,
            user=user,
            earliest_departure_time=tripRequest.earliest_departure_time,
            latest_departure_time=tripRequest.latest_departure_time,
            num_luggage_bags=tripRequest.num_luggage_bags
        )

        # remove all join requests from the trip request
        for joinRequest in tripRequest.join_requests.all():
            joinRequest.delete()
        
        tripRequest.delete()

        self.delete()

        # send email to team indicating confirmation and new trip details

    def reject(self):
        tripRequest = self.join_request.trip_request
        user = tripRequest.user

        trip = self.join_request.trip
        trip.num_join_requests -= 1
        trip.blacklisted_users.add(user)
        trip.save()

        self.join_request.delete()

        self.delete()

        # if this was the last confirmation request for the trip request and there are no join requests, then create a new trip for the user
        num_confirmation_requests = ConfirmationRequest.objects.filter(join_request__trip_request_id=tripRequest.id).count()
        if tripRequest.join_requests.count() == 0 and num_confirmation_requests == 0:
            newTrip = Trip.objects.create(
                num_participants=1,
                departure_location=tripRequest.departure_location,
                arrival_location=tripRequest.arrival_location,
                earliest_departure_time=tripRequest.earliest_departure_time,
                latest_departure_time=tripRequest.latest_departure_time,
                num_luggage_bags=tripRequest.num_luggage_bags,
                num_join_requests=0,
                college=tripRequest.user.college,
                is_full=False
            )
            newTrip.participant_list.add(tripRequest.user)
            TripUserDetails.objects.create(
                trip=newTrip,
                user=user,
                earliest_departure_time=tripRequest.earliest_departure_time,
                latest_departure_time=tripRequest.latest_departure_time,
                num_luggage_bags=tripRequest.num_luggage_bags
            )

            # delete the associated trip request
            tripRequest.delete()

        # TODO: Down the line, we should ask if they want to have more requests sent out. If not or if there are no more possible
        # trips they can join, then we should create a new trip for them.
