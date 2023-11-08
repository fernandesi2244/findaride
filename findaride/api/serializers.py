from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from datetime import timedelta
import datetime

from .models import TripRequest, Trip, JoinRequest, Location, ConfirmationRequest

UserModel = get_user_model()

class SimpleTripSerializer(serializers.ModelSerializer):
    arrival_location = serializers.StringRelatedField()
    departure_location = serializers.StringRelatedField()

    class Meta:
        model = Trip
        fields = '__all__'


class SimpleTripRequestSerializer(serializers.ModelSerializer):
    arrival_location = serializers.StringRelatedField()
    departure_location = serializers.StringRelatedField()
    class Meta:
        model = TripRequest
        fields = '__all__'


class TripRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripRequest
        fields = '__all__'

    def validate(self, attrs):
        # If the departure time is not after the current time, raise a ValidationError
        if attrs['departure_time'] <= datetime.now():
            raise serializers.ValidationError({"departure_time": "Departure time must be after the current time."})

        # TODO: depending on what we do for stale requests later, we might impose a max limit on the departure_time

        if attrs['num_luggage_bags'] < 0 or attrs['num_luggage_bags'] > 5: # TODO: change if we mess with bag filtering
            raise serializers.ValidationError({"num_luggage_bags": "Number of luggage bags must be between 0 and 5."})

        return attrs

    def create(self, validated_data):
        # if the user already has 2 pending trip requests, raise an error indicating that they cannot make any more requests at this time
        if TripRequest.objects.filter(user=self.context['request'].user).count() >= 2:
            raise serializers.ValidationError("You cannot make more than 2 pending trip requests at a time.")

        departureLocation, arrivalLocation = TripRequestSerializer.__getLocationObjects(validated_data['departure_location'], validated_data['arrival_location'])

        tripRequest = TripRequest.objects.create(
            user = self.context['request'].user,
            departure_location = departureLocation,
            arrival_location = arrivalLocation,
            departure_time = validated_data['departure_time'],
            num_luggage_bags = validated_data['num_luggage_bags']
        )

        # logic for finding matching trips
        userCollege = tripRequest.user.college
        matchingTrips = Trip.objects.filter(
            college=userCollege,
            departure_location__postal_code=tripRequest.departure_location.postal_code,
            arrival_location__postal_code=tripRequest.arrival_location.postal_code,
            departure_time_ge=tripRequest.departure_time,
            departure_time_le=tripRequest.departure_time + timedelta(minutes=20),
            num_luggage_bags_le=5 - tripRequest.num_luggage_bags,
            is_full=False,
        ).exclude(blacklisted_users__contains=tripRequest.user).order_by('departure_time', 'num_participants', 'num_luggage_bags')[:5]

        if len(matchingTrips) == 0:
            # No trips to match to, so make a new trip for the user requesting a trip
            # TODO: How does atomicity work with django? For example, we want the following lines to either all occur or not occur at all.
            trip = Trip.objects.create(
                college=userCollege,
                departure_location=tripRequest.departure_location,
                arrival_location=tripRequest.arrival_location,
                departure_time=tripRequest.departure_time,
                num_luggage_bags=tripRequest.num_luggage_bags,
                num_participants=1,
                is_full=False,
                num_join_requests=0
            )
            trip.participant_list.add(tripRequest.user)
            trip.save()

            tripRequest.delete()

            return None
        
        # Otherwise, we have matching trips, so we need to create a join request for each of them under a unified trip request
        for trip in matchingTrips:
            joinRequest = JoinRequest.objects.create(
                num_participants_accepted=0,
                trip_details_changed=False
            )
            joinRequest.save()

            joinRequest.assign(trip, tripRequest)

        return tripRequest

    def __getLocationObjects(departureLocation, arrivalLocation):
        # See if location table contains any rows with the same departure address. If so, fetch that row. Otherwise, create a new row.
        matchingDepartureLocations = Location.objects.filter(address=departureLocation['address'])
        if matchingDepartureLocations.exists():
            departureLocation = matchingDepartureLocations[0]
        else:
            departureLocation = Location.objects.create(
                address=departureLocation['address'],
                latitude=departureLocation['latitude'],
                longitude=departureLocation['longitude']
            )
            departureLocation.save()
        
        # Do the same for the arrival location
        matchingArrivalLocations = Location.objects.filter(address=arrivalLocation['address'])
        if matchingArrivalLocations.exists():
            arrivalLocation = matchingArrivalLocations[0]
        else:
            arrivalLocation = Location.objects.create(
                address=arrivalLocation['address'],
                latitude=arrivalLocation['latitude'],
                longitude=arrivalLocation['longitude']
            )
            arrivalLocation.save()
        
        return departureLocation, arrivalLocation

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'

class JoinRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinRequest
        fields = '__all__'

class ConfirmationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmationRequest
        fields = '__all__'

class UserTripsSerializer(serializers.ModelSerializer):
    trip_requests = SimpleTripRequestSerializer(many=True)
    trips = SimpleTripSerializer(many=True)
    class Meta:
        model = UserModel
        fields = ('trip_requests', 'trips')