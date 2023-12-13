from django.urls import include, path
from .views import JoinSelectedTripsAPIView, TripRequestAPIView, TripRequestListAPIView, UserTripsDetailAPIView, JoinRequestAPIView, TripAPIView, TripListAPIView
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path("user-trips/", UserTripsDetailAPIView.as_view(), name="user-trips"),
    path("join-requests/<int:pk>/", JoinRequestAPIView.as_view(), name="join-request"),
    path("join-selected-trips/", JoinSelectedTripsAPIView.as_view(), name="join-selected-trips"),
    path("trip/", TripAPIView.as_view(), name="create-trip"),
    path("trip-request-list/", TripRequestListAPIView.as_view(), name="trip-request-list"),
    path("delete-trip-request/<int:pk>/", TripRequestAPIView.as_view(), name="delete-trip-request"),
    path("trip/<int:pk>/", TripAPIView.as_view(), name="trip"),
    path("trip-list/", TripListAPIView.as_view(), name="trip-list"),
]

urlpatterns += router.urls
