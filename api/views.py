from django.shortcuts import render

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

from api.utils import send_join_email

from django.utils.timezone import make_aware

from rest_framework import generics, status, views, viewsets
from rest_framework import permissions
from rest_framework.response import Response
from secrets import token_urlsafe
from django.contrib.auth import get_user_model
from datetime import timedelta, datetime
from rest_framework.permissions import IsAuthenticated

UserModel = get_user_model()

from .models import TripRequest, Trip, JoinRequest, Location, ConfirmationRequest, TripUserDetails
from .serializers import TripRequestSerializer, SimpleTripRequestSerializer, UserTripsSerializer, SimpleConfirmationRequestSerializer, SimpleTripSerializer

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

class TripListAPIView(views.APIView):

    def get(self, request):
        user = request.user
        user_college = user.college
        blacklisted_trips_id = user.blacklisted_trips.values('id')
        user_trip_ids = user.trips.values('id')

        queryset = Trip.objects.filter(
            college=user_college,
            is_full=False,
        ).exclude(id__in=blacklisted_trips_id).exclude(id__in=user_trip_ids).order_by('num_participants', 'num_luggage_bags')
    
        earliest_departure_time = self.request.query_params.get("earliestDepartureTime", None)
        latest_departure_time = self.request.query_params.get("latestDepartureTime", None)
        num_luggage_bags = self.request.query_params.get("luggageCount", None)

        print(earliest_departure_time)
        departure_longitude = self.request.query_params.get("fromLong", None)
        departure_latitude = self.request.query_params.get("fromLat", None)
        arrival_longitude = self.request.query_params.get("toLong", None)
        arrival_latitude = self.request.query_params.get("toLat", None)

        if earliest_departure_time is not None:
            earliest_departure_time = datetime.strptime(earliest_departure_time, '%a, %d %b %Y %H:%M:%S %Z')
            earliest_departure_time = make_aware(earliest_departure_time)
            queryset = queryset.filter(earliest_departure_time__lte=earliest_departure_time)

        if latest_departure_time is not None:
            latest_departure_time = datetime.strptime(latest_departure_time, '%a, %d %b %Y %H:%M:%S %Z')
            latest_departure_time = make_aware(latest_departure_time)
            queryset = queryset.filter(latest_departure_time__gte=latest_departure_time)

        if num_luggage_bags is not None:
            queryset = queryset.filter(num_luggage_bags__lte=5 - int(num_luggage_bags))

        matching_trips = []

        if departure_latitude is not None and arrival_latitude is None:
            departure_latitude = float(departure_latitude)
            departure_longitude = float(departure_longitude)
            from_coord = (departure_latitude, departure_longitude)
            for trip in queryset:
                from_coord_2 = (trip.departure_location.latitude, trip.departure_location.longitude)
                if geodesic(from_coord, from_coord_2).miles < 1:
                    matching_trips.append(trip)
        elif departure_latitude is None and arrival_latitude is not None:
            arrival_latitude = float(arrival_latitude)
            arrival_longitude = float(arrival_longitude)
            to_coord = (arrival_latitude, arrival_longitude)
            for trip in queryset:
                from_coord_2 = (trip.departure_location.latitude, trip.departure_location.longitude)
                if geodesic(to_coord, to_coord_2).miles < 1:
                    matching_trips.append(trip)
        elif departure_latitude is not None and arrival_latitude is not None:
            arrival_latitude = float(arrival_latitude)
            arrival_longitude = float(arrival_longitude)
            departure_latitude = float(departure_latitude)
            departure_longitude = float(departure_longitude)
            from_coord = (departure_latitude, departure_longitude)
            to_coord = (arrival_latitude, arrival_longitude)
            for trip in queryset:
                from_coord_2 = (trip.departure_location.latitude, trip.departure_location.longitude)
                to_coord_2 = (trip.arrival_location.latitude, trip.arrival_location.longitude)
                if geodesic(from_coord, from_coord_2).miles < 1 and geodesic(to_coord, to_coord_2).miles < 1:
                    matching_trips.append(trip)
        else:
            matching_trips = queryset
    
        serializer = SimpleTripSerializer(matching_trips, many=True)
        return Response(serializer.data)

class ConfirmationRequestAPIView(views.APIView):
    def get(self, request):
        user = self.request.user
        confirmation_requests = ConfirmationRequest.objects.filter(join_request__trip_request__user=user)
        serializer = SimpleConfirmationRequestSerializer(confirmation_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        action = self.request.query_params.get("action", None)
        confirmation_request = ConfirmationRequest.objects.get(pk=pk)
        # TODO: Do all the logic for preventing users from typing random stuff in the URL
        if action == "accept":
            confirmation_request.accept()
        elif action == "reject":
            confirmation_request.reject()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Invalid action."})
        return Response(status=status.HTTP_200_OK)

class JoinRequestAPIView(views.APIView):
    def post(self, request, pk):
        action = self.request.query_params.get("action", None)
        join_request = JoinRequest.objects.get(pk=pk)
        # TODO: Do all the logic for preventing users from typing random stuff in the URL
        if action == "accept":
            join_request.accept(self.request.user)
        elif action == "reject":
            join_request.reject()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Invalid action."})
        return Response(status=status.HTTP_200_OK)

class TripRequestAPIView(views.APIView):
    serializer_class = TripRequestSerializer

    INDIVIDUAL_BAG_LIMIT = 5 # TODO: change if we mess with bag filtering

    def getRequestDataValidationResults(self, data):
        validation_results = {}
        # If the departure time is not after the current time, raise a ValidationError

        earliest_departure_time_parsed = datetime.strptime(data['earliest_departure_time'], '%a, %d %b %Y %H:%M:%S %Z')
        latest_departure_time_parsed = datetime.strptime(data['latest_departure_time'], '%a, %d %b %Y %H:%M:%S %Z')

        if earliest_departure_time_parsed <= datetime.utcnow():
            validation_results['earliest_departure_time'] = 'Departure time must be after the current time.'
        
        if latest_departure_time_parsed <= datetime.utcnow():
            validation_results['latest_departure_time'] = 'Departure time must be after the current time.'
        
        if earliest_departure_time_parsed > latest_departure_time_parsed:
            validation_results['earliest_departure_time'] = 'Earliest departure time must be before latest departure time.'

        # TODO: depending on what we do for stale requests later, we might impose a max limit on the departure_time

        if data['num_luggage_bags'] < 0 or data['num_luggage_bags'] > TripRequestAPIView.INDIVIDUAL_BAG_LIMIT: 
            validation_results['num_luggage_bags'] = f'Number of luggage bags must be between 0 and {TripRequestAPIView.INDIVIDUAL_BAG_LIMIT}.'

        return validation_results

    def post(self, request):
        data = request.data

        validation_results = self.getRequestDataValidationResults(data)

        if len(validation_results) > 0:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": validation_results})

        user = UserModel.objects.get(pk=data['user'])

        # if the user already has 2 pending trip requests, raise an error indicating that they cannot make any more requests at this time
        if TripRequest.objects.filter(user=user).filter(latest_departure_time__gte=datetime.utcnow()).count() >= 2:
            # return 400 Response indicating why the request failed
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "You cannot make more than 2 pending trip requests at a time."})

        try:
            departure_location, arrival_location = self.__getLocationObjects(data['departure_location'], data['arrival_location'])
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "One of the provided locations is currently not supported. Please see the following error: " + str(e)})

        earliest_departure_time = datetime.strptime(data['earliest_departure_time'], '%a, %d %b %Y %H:%M:%S %Z')
        latest_departure_time = datetime.strptime(data['latest_departure_time'], '%a, %d %b %Y %H:%M:%S %Z')

        earliest_departure_time = make_aware(earliest_departure_time)
        latest_departure_time = make_aware(latest_departure_time)

        trip_request = TripRequest.objects.create(
            user = user,
            departure_location = departure_location,
            arrival_location = arrival_location,
            earliest_departure_time = earliest_departure_time,
            latest_departure_time = latest_departure_time,
            num_luggage_bags = data['num_luggage_bags'],
            comment = data['comment']
        )

         # logic for finding matching trips
        user_college = trip_request.user.college
        blacklisted_trips_id = user.blacklisted_trips.values('id')
        user_trip_ids = user.trips.values('id')

        # Once we get lats/lons, update this. For now, just match on postal code.
        pre_matching_trips = Trip.objects.filter(
            college=user_college,
            earliest_departure_time__lte=trip_request.latest_departure_time,
            latest_departure_time__gte=trip_request.earliest_departure_time,
            num_luggage_bags__lte=5 - trip_request.num_luggage_bags,
            is_full=False,
        ).exclude(id__in=blacklisted_trips_id).exclude(id__in=user_trip_ids).order_by('num_participants', 'num_luggage_bags')[:5]

        matching_trips = []
        from_coord = (departure_location.latitude, departure_location.longitude)
        to_coord = (arrival_location.latitude, arrival_location.longitude)
        for trip in pre_matching_trips:
            from_coord_2 = (trip.departure_location.latitude, trip.departure_location.longitude)
            to_coord_2 = (trip.arrival_location.latitude, trip.arrival_location.longitude)
            if geodesic(from_coord, from_coord_2).miles < 1 and geodesic(to_coord, to_coord_2).miles < 1:
                matching_trips.append(trip)

        if len(matching_trips) == 0:
            # No trips to match to, so make a new trip for the user requesting a trip
            # TODO: How does atomicity work with django? For example, we want the following lines to either all occur or not occur at all.
            trip = Trip.objects.create(
                college=user_college,
                departure_location=trip_request.departure_location,
                arrival_location=trip_request.arrival_location,
                earliest_departure_time=trip_request.earliest_departure_time,
                latest_departure_time=trip_request.latest_departure_time,
                num_luggage_bags=trip_request.num_luggage_bags,
                num_participants=1,
                is_full=False,
                num_join_requests=0
            )
            trip.participant_list.add(trip_request.user)
            trip.save()

            TripUserDetails.objects.create(
                user=user,
                trip=trip,
                earliest_departure_time=trip_request.earliest_departure_time,
                latest_departure_time=trip_request.latest_departure_time,
                num_luggage_bags=trip_request.num_luggage_bags,
            )

            trip_request.delete()

            return Response({'message': 'Trip created'}, status=status.HTTP_200_OK)
        
        # Otherwise, we have matching trips, so we need to create a join request for each of them under a unified trip request
        for trip in matching_trips:
            join_request = JoinRequest.objects.create(
                num_participants_accepted=0,
                trip_details_changed=False,
                trip_request=trip_request,
                trip=trip
            )
            join_request.save()
            trip.num_join_requests += 1
            trip.save()

            send_join_email(trip.participant_list, user)

        return Response({'message': 'Trip request created'}, status=status.HTTP_200_OK)
    
    def __getLocationObjects(self, departure_location, arrival_location):
        # See if location table contains any rows with the same departure address. If so, fetch that row. Otherwise, create a new row.
        matching_departure_locations = Location.objects.filter(latitude=departure_location['latitude']).filter(longitude=departure_location['longitude'])

        geolocator = Nominatim(user_agent="findaride")
        if matching_departure_locations.exists():
            departure_location = matching_departure_locations[0]
        else:
            location = geolocator.reverse((departure_location['latitude'], departure_location['longitude']), addressdetails=True)
            #location = geolocator.geocode({"postalcode": departure_location['postal_code']})
            departure_location = Location.objects.create(
                address = departure_location['address'],
                postal_code = location.raw['address']['postcode'],
                latitude = departure_location['latitude'],
                longitude = departure_location['longitude'],
            )
            departure_location.save()
        
        # Do the same for the arrival location
        matching_arrival_locations = Location.objects.filter(latitude=arrival_location['latitude']).filter(longitude=arrival_location['longitude'])
        if matching_arrival_locations.exists():
            arrival_location = matching_arrival_locations[0]
        else:
            location = geolocator.reverse((arrival_location['latitude'], arrival_location['longitude']), addressdetails=True)
            arrival_location = Location.objects.create(
                address = arrival_location['address'],
                postal_code = location.raw['address']['postcode'],
                latitude = arrival_location['latitude'],
                longitude = arrival_location['longitude'],
            )
            arrival_location.save()
        
        return departure_location, arrival_location

    def delete(self, request, pk):
        # TODO: Atomicize this
        tripRequest = TripRequest.objects.get(pk=pk)
        try:
            joinRequests = tripRequest.join_requests.all()
            for joinRequest in joinRequests:
                associatedTrip = joinRequest.trip
                associatedTrip.num_join_requests -= 1
                associatedTrip.save()
                joinRequest.delete()
            tripRequest.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})
    
class UserTripsDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserModel.objects.all()
    serializer_class = UserTripsSerializer

class TripAPIView(views.APIView):
    serializer_class = SimpleTripSerializer

    def patch(self, request, pk):
        action = self.request.query_params.get("action", None)
        if action is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "No action provided."})

        trip = Trip.objects.get(pk=pk)

        if action == "removeUser":
            trip.remove_user(self.request.user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Invalid action."})
