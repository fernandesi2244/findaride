from django.urls import include, path
from .views import TripRequestModelViewSet, TripRequestAPIView, TripRequestListAPIView, UserTripsDetailAPIView, JoinRequestAPIView, TripAPIView, TripListAPIView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'trip-request', TripRequestModelViewSet)

urlpatterns = [
    path("user-trips/<int:pk>/", UserTripsDetailAPIView.as_view(), name="user-trips"),
    path("join-requests/<int:pk>/", JoinRequestAPIView.as_view(), name="join-request"),
    path("trip-request/", TripRequestAPIView.as_view(), name="trip-request"),
    path("trip-request-list/", TripRequestListAPIView.as_view(), name="trip-request-list"),
    path("delete-trip-request/<int:pk>/", TripRequestAPIView.as_view(), name="delete-trip-request"),
    path("trip/<int:pk>/", TripAPIView.as_view(), name="trip"),
    path("trip/", TripListAPIView.as_view(), name="trip-list"),
]

urlpatterns += router.urls
