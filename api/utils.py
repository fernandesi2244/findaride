from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse

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
