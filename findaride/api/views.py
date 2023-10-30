from django.shortcuts import render

from rest_framework import generics, status, views, viewsets
from rest_framework import permissions
from .serializers import LoginSerializer, SignUpSerializer
from rest_framework.response import Response
from secrets import token_urlsafe
from django.contrib.auth import get_user_model

from .models import Trip as TripModel

# TODO: see if any permissions need to be changed

# TODO: add appropriate views to users app based on table schema (e.g., trip ids for that user)
class TripRequestModelViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = TripModel.objects.all()
    # serializer_class = randomOne # TODO: finish

    # Define list here and create in serializer
