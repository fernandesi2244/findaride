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
        departureLocation, arrivalLocation = self.__getLocationObjects(data['departure_location'], data['arrival_location'])

        departure_time = datetime.strptime(data['departure_time'], '%y-%m-%d %H:%M:%S')

        user = UserModel.objects.get(pk=data['user'])

        tripRequest = TripRequest.objects.create(
            user = user,
            departure_location = departureLocation,
            arrival_location = arrivalLocation,
            departure_time = departure_time,
            num_luggage_bags = data['num_luggage_bags']
        )


        return Response(status=status.HTTP_200_OK)
    
    def __getLocationObjects(self, departureLocation, arrivalLocation):
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

        {"departure_time":"test","num_luggage_bags":0,"user":1,"departure_location":{"address":"JFK Terminal 1, Queens, NY, USA","longitude":-73.7890953,"latitude":40.6433188},"arrival_location":{"address":"Princeton Jct., Wallace Circle, Princeton Junction, NJ, USA","longitude":-74.6238302,"latitude":40.3163592}}
    
class UserTripsDetailAPIView(generics.RetrieveAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserTripsSerializer
