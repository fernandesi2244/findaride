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
from .serializers import TripRequestSerializer, SimpleTripRequestSerializer, UserTripsSerializer, SimpleTripSerializer, SimpleUserTripSerializer

# TODO: see if any permissions need to be changed

class TripListAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    # gets the filtered list of trips in the search widget
    def get(self, request):
        user = request.user
        user_college = user.college
        blacklisted_trips_id = user.blacklisted_trips.values('id')
        user_trip_ids = user.trips.values('id')
        trips_requested = [joinRequest.trip.id for tripRequest in TripRequest.objects.filter(user=user) for joinRequest in tripRequest.join_requests.all()]

        curr_utc_time = make_aware(datetime.utcnow())

        queryset = Trip.objects.filter(
            college=user_college,
            is_full=False,
            # allow trips to be joined late but not too late (halfway through the defined range)
            earliest_departure_time__gt=curr_utc_time - (F('latest_departure_time') - F('earliest_departure_time')) / 2,
        ).exclude(id__in=blacklisted_trips_id).exclude(id__in=user_trip_ids).exclude(id__in=trips_requested).order_by('num_participants', 'num_luggage_bags')

        earliest_departure_time = self.request.query_params.get("earliestDepartureTime", None)
        latest_departure_time = self.request.query_params.get("latestDepartureTime", None)
        # num_luggage_bags = self.request.query_params.get("luggageCount", None)

        departure_longitude = self.request.query_params.get("fromLong", None)
        departure_latitude = self.request.query_params.get("fromLat", None)
        arrival_longitude = self.request.query_params.get("toLong", None)
        arrival_latitude = self.request.query_params.get("toLat", None)

        if latest_departure_time is not None:
            latest_departure_time = datetime.strptime(latest_departure_time, '%a, %d %b %Y %H:%M:%S %Z')
            latest_departure_time = make_aware(latest_departure_time)
            queryset = queryset.filter(earliest_departure_time__lte=latest_departure_time)

        if earliest_departure_time is not None:
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
            matching_trips = queryset[:]
    
        serializer = SimpleTripSerializer(matching_trips, many=True)
        return Response(status=status.HTTP_200_OK, data={
            "trips": serializer.data,
        })

class JoinRequestAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        action = self.request.query_params.get("action", None)
        try:
            join_request = JoinRequest.objects.get(pk=pk)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})
        
        # Verify that the user is in the trip that the join request is for
        user = self.request.user
        if user not in join_request.trip.participant_list.all():
            return Response(status=status.HTTP_403_FORBIDDEN, data={"error": "Not authorized."})

        if action == "accept":
            join_request.accept(user)
        elif action == "reject":
            join_request.reject()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Invalid action."})
        return Response(status=status.HTTP_200_OK)

class JoinSelectedTripsAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        selected_trip_ids = request.data['selected_trip_ids']
        if selected_trip_ids is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "No trips selected."})
        user = request.user

        # validate request data
        if request.data['luggageCount'] < 0: # or data['num_luggage_bags'] > TripRequestAPIView.INDIVIDUAL_BAG_LIMIT: 
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": f"Number of luggage bags must be greater than 0."})
        if (len(request.data['nickname']) > TripUserDetails.MAX_NICKNAME_LENGTH):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": f"Nickname too long. Stay under {TripUserDetails.MAX_NICKNAME_LENGTH} characters."})

        trip_request = TripRequest.objects.create(
            user = user,
            trip_nickname = request.data['nickname'],
            num_luggage_bags = request.data['luggageCount'],
            comment = request.data['comment']
        )
        trip_request.save()
        request_made = False
        for trip_id in selected_trip_ids:
            try:
                trip = Trip.objects.get(pk=trip_id)
            except Exception as e:
                continue

            # check if the user CAN join the trip
            if trip.college != user.college:
                continue
            if trip.is_full:
                continue
            if trip.earliest_departure_time <= make_aware(datetime.utcnow()) - (trip.latest_departure_time - trip.earliest_departure_time) / 2:
                continue
            if trip.blacklisted_users.filter(id=user.id).exists():
                continue
            if trip.participant_list.filter(id=user.id).exists():
                continue
            if JoinRequest.objects.filter(trip_request__user=user).filter(trip=trip).exists():
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
            trip_request.delete()
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "The requested trips do not exist or are unavailable to join."})
        return Response(status=status.HTTP_200_OK)

class TripRequestAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    serializer_class = TripRequestSerializer

    def delete(self, request, pk):
        # TODO: Atomicize this
        try:
            tripRequest = TripRequest.objects.get(pk=pk)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})
        
        # check authorization
        user = request.user
        if user != tripRequest.user:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"error": "Not authorized."})

        try:
            joinRequests = tripRequest.join_requests.all()
            for joinRequest in joinRequests:
                joinRequest.delete()
            tripRequest.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})
    
class UserTripsDetailAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    queryset = UserModel.objects.all()

    def get(self, request):
        when = self.request.query_params.get("when", None)
        if when is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "No time span provided."})
        elif when == "past" or when == "upcoming" or when == "all":
            user = self.request.user
            associated_trips = user.trips.all()
            associated_trip_requests = user.trip_requests.all()

            utcnow = datetime.utcnow()

            if when == "past":
                associated_trips = associated_trips.filter(latest_departure_time__lt=utcnow)
            elif when == "upcoming":
                associated_trips = associated_trips.filter(latest_departure_time__gte=utcnow)

            return Response(status=status.HTTP_200_OK, data={
                "trips": SimpleUserTripSerializer(associated_trips, many=True, context={'request': request}).data,
                "trip_requests": SimpleTripRequestSerializer(associated_trip_requests, many=True).data,
            })

class TripAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    serializer_class = SimpleTripSerializer

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

        if (len(data['trip_nickname']) > TripUserDetails.MAX_NICKNAME_LENGTH):
            validation_results['trip_nickname'] = f'Nickname too long. Stay under {TripUserDetails.MAX_NICKNAME_LENGTH} characters.'

        return validation_results

    def post(self, request):
        data = request.data

        validation_results = self.getRequestDataValidationResults(data)

        if len(validation_results) > 0:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": validation_results})

        user = self.request.user

        try:
            departure_location, arrival_location = self.__getLocationObjects(data['departure_location'], data['arrival_location'])
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "One of the provided locations is currently not supported. Please see the following error: " + str(e)})

        earliest_departure_time = datetime.strptime(data['earliest_departure_time'], '%a, %d %b %Y %H:%M:%S %Z')
        latest_departure_time = datetime.strptime(data['latest_departure_time'], '%a, %d %b %Y %H:%M:%S %Z')

        earliest_departure_time = make_aware(earliest_departure_time)
        latest_departure_time = make_aware(latest_departure_time)

        # TODO: How does atomicity work with django? For example, we want the following lines to either all occur or not occur at all.
        trip = Trip.objects.create(
            college=user.college,
            departure_location=departure_location,
            arrival_location=arrival_location,
            earliest_departure_time=earliest_departure_time,
            latest_departure_time=latest_departure_time,
            num_luggage_bags=data['num_luggage_bags'],
            num_participants=1,
            is_full=False,
        )
        trip.participant_list.add(user)
        trip.save()

        TripUserDetails.objects.create(
            user=user,
            trip=trip,
            num_luggage_bags=data['num_luggage_bags'],
            trip_nickname=data['trip_nickname'],
        )

        return Response({'message': 'Trip created'}, status=status.HTTP_200_OK)

    def __getLocationObjects(self, departure_location, arrival_location):
        # See if location table contains any rows with the same departure address. If so, fetch that row. Otherwise, create a new row.
        matching_departure_locations = Location.objects.filter(latitude=departure_location['latitude']).filter(longitude=departure_location['longitude'])

        geolocator = Nominatim(user_agent="findaride")
        if matching_departure_locations.exists():
            departure_location = matching_departure_locations[0]
        else:
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
            arrival_location = Location.objects.create(
                address = arrival_location['address'],
                latitude = arrival_location['latitude'],
                longitude = arrival_location['longitude'],
            )
            arrival_location.save()
        
        return departure_location, arrival_location

    def patch(self, request, pk):
        action = self.request.query_params.get("action", None)
        if action is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "No action provided."})

        trip = Trip.objects.get(pk=pk)

        # check authorization
        user = request.user
        if user not in trip.participant_list.all():
            return Response(status=status.HTTP_403_FORBIDDEN, data={"error": "Not authorized."})

        if action == "removeUser":
            trip.remove_user(self.request.user)
            return Response(status=status.HTTP_200_OK)
        elif action == "toggleIsFullSetting":
            trip.toggle_is_full_setting()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Invalid action."})
