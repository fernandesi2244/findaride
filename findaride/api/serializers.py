from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from datetime import timedelta
import datetime

from .models import TripRequest, Trip, JoinRequest

UserModel = get_user_model()

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

        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # TODO: should we validate the locations here and add them to the database if they don't exist?

        return attrs

    def create(self, validated_data):
        # TODO: if location(s) don't exist in database, create it

        tripRequest = TripRequest.objects.create(
            user = self.context['request'].user,
            departure_location = validated_data['departure_location'],
            arrival_location = validated_data['arrival_location'],
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

            return None # TODO: IS THIS RIGHT??
        
        # Otherwise, we have matching trips, so we need to create a join request for each of them under a unified trip request
        for trip in matchingTrips:
            joinRequest = JoinRequest.objects.create(
                num_participants_accepted=0,
                trip_details_changed=False
            )
            joinRequest.save()

            joinRequest.assign(trip, tripRequest)

        return tripRequest

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label="Email",
        # This will be used when the DRF browsable API is enabled
        trim_whitespace=False,
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take email and password from request
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong email or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "email" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs