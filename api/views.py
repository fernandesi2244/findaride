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
from django.db.models import F

UserModel = get_user_model()

from .models import TripRequest, Trip, JoinRequest, Location, TripUserDetails
from .serializers import TripRequestSerializer, SimpleTripRequestSerializer, UserTripsSerializer, SimpleTripSerializer

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

        curr_utc_time = make_aware(datetime.utcnow())

        queryset = Trip.objects.filter(
            college=user_college,
            is_full=False,
            # allow trips to be joined late but not too late (halfway through the defined range)
            earliest_departure_time__gt=curr_utc_time - (F('latest_departure_time') - F('earliest_departure_time')) / 2,
        ).exclude(id__in=blacklisted_trips_id).exclude(id__in=user_trip_ids).order_by('num_participants', 'num_luggage_bags')
    
        earliest_departure_time = self.request.query_params.get("earliestDepartureTime", None)
        latest_departure_time = self.request.query_params.get("latestDepartureTime", None)
        # num_luggage_bags = self.request.query_params.get("luggageCount", None)

        departure_longitude = self.request.query_params.get("fromLong", None)
        departure_latitude = self.request.query_params.get("fromLat", None)
        arrival_longitude = self.request.query_params.get("toLong", None)
        arrival_latitude = self.request.query_params.get("toLat", None)

        if earliest_departure_time is not None:
            latest_departure_time = datetime.strptime(latest_departure_time, '%a, %d %b %Y %H:%M:%S %Z')
            latest_departure_time = make_aware(latest_departure_time)
            queryset = queryset.filter(earliest_departure_time__lte=latest_departure_time)

        if latest_departure_time is not None:
            earliest_departure_time = datetime.strptime(earliest_departure_time, '%a, %d %b %Y %H:%M:%S %Z')
            earliest_departure_time = make_aware(earliest_departure_time)
            queryset = queryset.filter(latest_departure_time__gte=earliest_departure_time)

        # if num_luggage_bags is not None:
        #     queryset = queryset.filter(num_luggage_bags__lte=5 - int(num_luggage_bags))

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
                to_coord_2 = (trip.arrival_location.latitude, trip.arrival_location.longitude)
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


class JoinRequestAPIView(views.APIView):
    def post(self, request, pk):
        action = self.request.query_params.get("action", None)
        try:
            join_request = JoinRequest.objects.get(pk=pk)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})
        # TODO: Do all the logic for preventing users from typing random stuff in the URL
        if action == "accept":
            join_request.accept(self.request.user)
        elif action == "reject":
            join_request.reject()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Invalid action."})
        return Response(status=status.HTTP_200_OK)

class JoinSelectedTripsAPIView(views.APIView):
    def post(self, request):
        selected_trip_ids = request.data['selected_trip_ids']
        if selected_trip_ids is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "No trips selected."})
        user = request.user
        trip_request = TripRequest.objects.create(
            user = user,
            departure_location = Location.objects.get(pk=1),
            arrival_location = Location.objects.get(pk=1),
            earliest_departure_time = datetime.utcnow(),
            latest_departure_time = datetime.utcnow(),
            num_luggage_bags = -1,
            comment = 'TODO: FIX THIS!'
        )
        trip_request.save()
        request_made = False
        for trip_id in selected_trip_ids:
            try:
                trip = Trip.objects.get(pk=trip_id)
            except Exception as e:
                continue
            request_made = True
            join_request = JoinRequest.objects.create(
                num_participants_accepted=0,
                trip_details_changed=False,
                trip_request=trip_request,
                trip=trip
            )
            join_request.save()
            send_join_email(trip.participant_list, trip)
        
        if not request_made:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "The requested trips do not exist."})
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

        if data['num_luggage_bags'] < 0: # or data['num_luggage_bags'] > TripRequestAPIView.INDIVIDUAL_BAG_LIMIT: 
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

        pre_matching_trips = Trip.objects.filter(
            college=user_college,
            earliest_departure_time__lte=trip_request.latest_departure_time,
            latest_departure_time__gte=trip_request.earliest_departure_time,
            # num_luggage_bags__lte=5 - trip_request.num_luggage_bags,
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
            trip.save()

            send_join_email(trip.participant_list, trip)

        return Response({'message': 'Trip request created'}, status=status.HTTP_200_OK)
    
    def __getLocationObjects(self, departure_location, arrival_location):
        # See if location table contains any rows with the same departure address. If so, fetch that row. Otherwise, create a new row.
        matching_departure_locations = Location.objects.filter(latitude=departure_location['latitude']).filter(longitude=departure_location['longitude'])

        geolocator = Nominatim(user_agent="findaride")
        if matching_departure_locations.exists():
            departure_location = matching_departure_locations[0]
        else:
            location = geolocator.reverse((departure_location['latitude'], departure_location['longitude']), addressdetails=True)
            departure_location = Location.objects.create(
                address = departure_location['address'],
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
                latitude = arrival_location['latitude'],
                longitude = arrival_location['longitude'],
            )
            arrival_location.save()
        
        return departure_location, arrival_location

    def delete(self, request, pk):
        # TODO: Atomicize this
        try:
            tripRequest = TripRequest.objects.get(pk=pk)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})
        try:
            joinRequests = tripRequest.join_requests.all()
            for joinRequest in joinRequests:
                joinRequest.delete()
            tripRequest.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})
    
class UserTripsDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserModel.objects.all()
    serializer_class = UserTripsSerializer

    def get(self, request):
        when = self.request.query_params.get("when", None)
        if when is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "No time span provided."})
        elif when == "past" or when == "upcoming":
            user = self.request.user
            associated_trips = user.trips.all()
            associated_trip_requests = user.trip_requests.all()

            utcnow = datetime.utcnow()

            if when == "past":
                associated_trips = associated_trips.filter(latest_departure_time__lt=utcnow)
                associated_trip_requests = associated_trip_requests.filter(latest_departure_time__lt=utcnow)
            elif when == "upcoming":
                associated_trips = associated_trips.filter(latest_departure_time__gte=utcnow)
                associated_trip_requests = associated_trip_requests.filter(latest_departure_time__gte=utcnow)

            return Response(status=status.HTTP_200_OK, data={
                "trips": SimpleTripSerializer(associated_trips, many=True).data,
                "trip_requests": SimpleTripRequestSerializer(associated_trip_requests, many=True).data,
                "id": user.id,
            })

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
        elif action == "toggleIsFullSetting":
            trip.toggle_is_full_setting()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Invalid action."})
