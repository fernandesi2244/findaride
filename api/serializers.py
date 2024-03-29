from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.serializers import SimpleUserSerializer

from .models import TripRequest, Trip, JoinRequest, Location, TripUserDetails

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


class TripRequestSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    join_requests = JoinRequestTripSerializer(many=True)
    
    class Meta:
        model = TripRequest
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class SimpleTripRequestSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    join_requests = JoinRequestTripSerializer(many=True)
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

    num_pending_requests = serializers.SerializerMethodField()

    def get_num_pending_requests(self, obj):
        return obj.join_requests.count()

    class Meta:
        model = Trip
        fields = '__all__'

class SimpleUserTripSerializer(serializers.ModelSerializer):
    arrival_location = serializers.StringRelatedField()
    departure_location = serializers.StringRelatedField()
    participant_list = SimpleUserSerializer(many=True)
    join_requests = JoinRequestSerializer(many=True)
    trip_nickname = serializers.SerializerMethodField()

    def get_trip_nickname(self, obj):
        user = self.context['request'].user
        if user in obj.participant_list.all():
            return TripUserDetails.objects.get(trip=obj, user=user).trip_nickname
        return "Rideshare trip"

    class Meta:
        model = Trip
        fields = '__all__'


class UserTripsSerializer(serializers.ModelSerializer):
    trip_requests = TripRequestSerializer(many=True)
    trips = SimpleTripSerializer(many=True)
    class Meta:
        model = UserModel
        fields = ('trip_requests', 'trips', 'id')
