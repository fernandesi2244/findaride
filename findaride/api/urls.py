from django.urls import include, path
from .views import TripRequestModelViewSet, TripRequestCreateAPIView, TripRequestListAPIView, UserTripsDetailAPIView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'trip-request', TripRequestModelViewSet)

urlpatterns = [
    path("user-trips/<int:pk>/", UserTripsDetailAPIView.as_view(), name="user-trips"),
    path("trip-request/", TripRequestCreateAPIView.as_view(), name="trip-request-list"),
    path("trip-request-list/", TripRequestListAPIView.as_view(), name="trip-request-list"),
]

urlpatterns += router.urls
