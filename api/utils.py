from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from threading import *

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To

def send_trip_marked_full_email(participant_list, trip):
    subject = "findaride: Trip marked full"
    from_email = settings.SENDGRID_EMAIL
    to = [To(participant.email) for participant in participant_list.all()]

    # Load the HTML template
    html_content = render_to_string('emails/marked_full.html', {'dep': trip.departure_location.address.split(",")[0], 'arr': trip.arrival_location.address.split(",")[0]})

    message = Mail(
        from_email=from_email,
        to_emails=to,
        subject=subject,
        html_content=html_content)
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

def send_trip_joined_email(user, trip):
    subject = "findaride: Joined a trip"
    from_email = settings.SENDGRID_EMAIL
    to = [To(user.email),]

    # Load the HTML template
    html_content = render_to_string('emails/trip_joined.html', {'user': user, 'trip': trip})

    message = Mail(
        from_email=from_email,
        to_emails=to,
        subject=subject,
        html_content=html_content)
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

def send_join_email(participant_list, trip):
    subject = "findaride: Request to join your trip"
    from_email = settings.SENDGRID_EMAIL
    to = [To(participant.email) for participant in participant_list.all()]

    # Load the HTML template
    html_content = render_to_string('emails/join_request.html', {'dep': trip.departure_location.address.split(",")[0], 'arr': trip.arrival_location.address.split(",")[0]})

    message = Mail(
        from_email=from_email,
        to_emails=to,
        subject=subject,
        html_content=html_content)
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

def send_member_left_email(participant_list, trip):
    subject = "findaride: A member has left your trip"
    from_email = settings.SENDGRID_EMAIL
    to = [To(participant.email) for participant in participant_list.all()]

    # Load the HTML template
    html_content = render_to_string('emails/member_left.html', {'dep': trip.departure_location.address.split(",")[0], 'arr': trip.arrival_location.address.split(",")[0]})

    message = Mail(
        from_email=from_email,
        to_emails=to,
        subject=subject,
        html_content=html_content)
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

def send_absolute_rejection_email(user):
    subject = "findaride: Request(s) to join trip(s) failed"
    from_email = settings.SENDGRID_EMAIL
    to = [To(user.email),]

    # Load the HTML template
    html_content = render_to_string('emails/absolute_rejection.html', {'user': user})

    message = Mail(
        from_email=from_email,
        to_emails=to,
        subject=subject,
        html_content=html_content)
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)