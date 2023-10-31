from django.shortcuts import render

from rest_framework import generics, status, views, viewsets
from rest_framework import permissions
from rest_framework.response import Response
from secrets import token_urlsafe
from django.contrib.auth import get_user_model

from .models import TripRequest as TripRequestModel
from .serializers import TripRequestSerializer

# TODO: see if any permissions need to be changed

# TODO: add appropriate views to users app based on table schema (e.g., trip ids for that user)
class TripRequestModelViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = TripRequestModel.objects.all()
    serializer_class = TripRequestSerializer

    # Define list here and create in serializer
