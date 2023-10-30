from django.urls import path
from .views import TripRequestModelViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'model-viewset', TripRequestModelViewSet)

urlpatterns = [
    # path('create-trip-request/', views.TripRequestView, name='create_trip_request'),
    # path('user-confirmation-requests/<int:user-id>/', ..., name='user_confirmation_requests'),
]