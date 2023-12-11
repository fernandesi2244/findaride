from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from .models import Trip, TripUserDetails

def send_trip_joined_email(user, trip):
    subject = "findaride: Joined a trip"
    from_email = settings.EMAIL_HOST_USER
    to = [user.email,]

    # Load the HTML template
    html_content = render_to_string('emails/trip_joined.html', {'user': user, 'trip': trip})

    # Create the email body with both HTML and plain text versions
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, "text/html")
    email.send()

def send_join_email(participant_list, user):
    subject = "findaride: Request to join your trip"
    from_email = settings.EMAIL_HOST_USER
    to = [participant.email for participant in participant_list.all()]

    # Load the HTML template
    html_content = render_to_string('emails/join_request.html', {'user': user})

    # Create the email body with both HTML and plain text versions
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, "text/html")
    email.send()

def send_member_left_email(participant_list):
    subject = "findaride: A member has left your trip"
    from_email = settings.EMAIL_HOST_USER
    to = [participant.email for participant in participant_list.all()]

    # Load the HTML template
    html_content = render_to_string('emails/member_left.html')

    # Create the email body with both HTML and plain text versions
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, "text/html")
    email.send()

def create_new_trip(trip_request):
    new_trip = Trip.objects.create(
        num_participants=1,
        departure_location=trip_request.departure_location,
        arrival_location=trip_request.arrival_location,
        earliest_departure_time=trip_request.earliest_departure_time,
        latest_departure_time=trip_request.latest_departure_time,
        num_luggage_bags=trip_request.num_luggage_bags,
        num_join_requests=0,
        college=trip_request.user.college,
        is_full=False
    )
    new_trip.participant_list.add(trip_request.user)
    TripUserDetails.objects.create(
        trip=new_trip,
        user=trip_request.user,
        earliest_departure_time=trip_request.earliest_departure_time,
        latest_departure_time=trip_request.latest_departure_time,
        num_luggage_bags=trip_request.num_luggage_bags
    )

    return new_trip