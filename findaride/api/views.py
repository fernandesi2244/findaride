from django.shortcuts import render

from rest_framework import generics, status, views, viewsets
from rest_framework import permissions
from rest_framework.response import Response
from secrets import token_urlsafe
from django.contrib.auth import get_user_model
from datetime import timedelta, datetime

UserModel = get_user_model()

from .models import TripRequest, Trip, JoinRequest, Location
from .serializers import TripRequestSerializer, SimpleTripRequestSerializer, UserTripsSerializer

# TODO: see if any permissions need to be changed

# TODO: add appropriate views to users app based on table schema (e.g., trip ids for that user)
class TripRequestModelViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = TripRequest.objects.all()
    serializer_class = TripRequestSerializer

    # Define list here and create in serializer


class TripRequestListAPIView(generics.ListAPIView):
    serializer_class = SimpleTripRequestSerializer
    queryset = TripRequest.objects.all()


class TripRequestCreateAPIView(views.APIView):
    serializer_class = TripRequestSerializer

    def post(self, request):
        data = request.data
        departure_location, arrival_location = self.__getLocationObjects(data['departure_location'], data['arrival_location'])

        departure_time = datetime.strptime(data['departure_time'], '%y-%m-%d %H:%M:%S')

        user = UserModel.objects.get(pk=data['user'])

        trip_request = TripRequest.objects.create(
            user = user,
            departure_location = departure_location,
            arrival_location = arrival_location,
            departure_time = departure_time,
            num_luggage_bags = data['num_luggage_bags']
        )

         # logic for finding matching trips
        user_college = trip_request.user.college
        

        blacklisted_trips_id = user.blacklisted_trips.values('id')

        matching_trips = Trip.objects.filter(
            college=user_college,
            departure_location__postal_code=trip_request.departure_location.postal_code,
            arrival_location__postal_code=trip_request.arrival_location.postal_code,
            departure_time__gte=trip_request.departure_time,
            departure_time__lte=trip_request.departure_time + timedelta(minutes=20),
            num_luggage_bags__lte=5 - trip_request.num_luggage_bags,
            is_full=False,
        ).exclude(id__in=blacklisted_trips_id).order_by('departure_time', 'num_participants', 'num_luggage_bags')[:5]

        if len(matching_trips) == 0:
            # No trips to match to, so make a new trip for the user requesting a trip
            # TODO: How does atomicity work with django? For example, we want the following lines to either all occur or not occur at all.
            trip = Trip.objects.create(
                college=user_college,
                departure_location=trip_request.departure_location,
                arrival_location=trip_request.arrival_location,
                departure_time=trip_request.departure_time,
                num_luggage_bags=trip_request.num_luggage_bags,
                num_participants=1,
                is_full=False,
                num_join_requests=0
            )
            trip.participant_list.add(trip_request.user)
            trip.save()

            trip_request.delete()

            return Response(status=status.HTTP_200_OK)
        
        # Otherwise, we have matching trips, so we need to create a join request for each of them under a unified trip request
        for trip in matching_trips:
            join_request = JoinRequest.objects.create(
                num_participants_accepted=0,
                trip_details_changed=False
            )
            join_request.save()
            join_request.assign(trip, trip_request)

        return Response(status=status.HTTP_200_OK)
    
    def __getLocationObjects(self, departure_location, arrival_location):
        # See if location table contains any rows with the same departure address. If so, fetch that row. Otherwise, create a new row.
        matching_departure_locations = Location.objects.filter(postal_code=departure_location['postal_code'])
        if matching_departure_locations.exists():
            departure_location = matching_departure_locations[0]
        else:
            departure_location = Location.objects.create(
                address=departure_location['address'],
                postal_code=departure_location['postal_code'],
            )
            departure_location.save()
        
        # Do the same for the arrival location
        matching_arrival_locations = Location.objects.filter(postal_code=arrival_location['postal_code'])
        if matching_arrival_locations.exists():
            arrival_location = matching_arrival_locations[0]
        else:
            arrival_location = Location.objects.create(
                address=arrival_location['address'],
                postal_code=arrival_location['postal_code'],
            )
            arrival_location.save()
        
        return departure_location, arrival_location
    
class UserTripsDetailAPIView(generics.RetrieveAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserTripsSerializer
