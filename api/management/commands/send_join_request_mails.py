from django.core.management.base import BaseCommand
from api.models import Trip, JoinRequest
from api.utils import send_join_email
from datetime import datetime

class Command(BaseCommand):
    help = 'Send emails to trips with join requests'

    def handle(self, *args, **kwargs):
        utcnow = datetime.utcnow()
        unique_trips = Trip.objects.filter(join_requests__isnull=False).filter(latest_departure_time__gte=utcnow).distinct()

        for trip in unique_trips:
            send_join_email(trip.participant_list, trip)
            self.stdout.write(f'sending email to {trip.id}')