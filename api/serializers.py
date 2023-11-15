from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from users.serializers import SimpleUserSerializer
from django.contrib.auth.password_validation import validate_password

from datetime import timedelta
import datetime

from .models import TripRequest, Trip, JoinRequest, Location, ConfirmationRequest

UserModel = get_user_model()

class TripSerializer(serializers.ModelSerializer):
    arrival_location = serializers.StringRelatedField()
    departure_location = serializers.StringRelatedField()
    class Meta:
        model = Trip
        fields = '__all__'

class JoinRequestTripSerializer(serializers.ModelSerializer):
    trip = TripSerializer()

    class Meta:
        model = JoinRequest
        fields = '__all__'
        fields = ('num_participants_accepted', 'trip_details_changed', 'participants_that_accepted', 'trip', 'id')


class SimpleConfirmationRequestSerializer(serializers.ModelSerializer):
    join_request = JoinRequestTripSerializer()
    class Meta:
        model = ConfirmationRequest
        fields = '__all__'

class TripRequestSerializer(serializers.ModelSerializer):
    arrival_location = serializers.StringRelatedField()
    departure_location = serializers.StringRelatedField()
    user = SimpleUserSerializer()
    join_requests = JoinRequestTripSerializer(many=True)

    confirmation_requests = serializers.SerializerMethodField('get_confirmation_requests')
    
    def get_confirmation_requests(self, obj):
        confirmation_requests = ConfirmationRequest.objects.filter(join_request__trip_request_id=obj.id)
        serializer = SimpleConfirmationRequestSerializer(confirmation_requests, many=True)
        return serializer.data
    
    class Meta:
        model = TripRequest
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class SimpleTripRequestSerializer(serializers.ModelSerializer):
    arrival_location = serializers.StringRelatedField()
    departure_location = serializers.StringRelatedField()
    user = SimpleUserSerializer()
    class Meta:
        model = TripRequest
        fields = '__all__'

class JoinRequestSerializer(serializers.ModelSerializer):
    trip_request = SimpleTripRequestSerializer()
    class Meta:
        model = JoinRequest
        fields = '__all__'
        fields = ('id', 'num_participants_accepted', 'trip_details_changed', 'participants_that_accepted', 'trip_request')


class SimpleTripSerializer(serializers.ModelSerializer):
    arrival_location = serializers.StringRelatedField()
    departure_location = serializers.StringRelatedField()
    participant_list = SimpleUserSerializer(many=True)
    join_requests = JoinRequestSerializer(many=True)

    class Meta:
        model = Trip
        fields = '__all__'


class UserTripsSerializer(serializers.ModelSerializer):
    trip_requests = TripRequestSerializer(many=True)
    trips = SimpleTripSerializer(many=True)
    class Meta:
        model = UserModel
        fields = ('trip_requests', 'trips')
