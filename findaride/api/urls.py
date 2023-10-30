from django.urls import path
from . import views

urlpatterns = [
    path('create-trip-request/', views.TripRequestView, name='create_trip_request'),
    # path('user-confirmation-requests/<int:user-id>/', ..., name='user_confirmation_requests'),
]