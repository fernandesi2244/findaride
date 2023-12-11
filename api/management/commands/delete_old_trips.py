from django.core.management.base import BaseCommand
from api.models import TripRequest, Trip
from geopy.distance import geodesic
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Delete old trips'

    def handle(self, *args, **kwargs):
        old_trips = Trip.objects.filter(latest_departure_time__lte=(timezone.now()-timedelta(days=365)))
        for trip in old_trips.all():
            for participant in trip.participant_list.all():
                user_stats = participant.user_stats

                if user_stats:
                    user_stats.number_trips += 1
                    from_coord = (trip.departure_location.latitude, trip.departure_location.longitude)
                    to_coord = (trip.arrival_location.latitude, trip.arrival_location.longitude)
                    user_stats.miles_ridden += int(geodesic(from_coord, to_coord).miles)
                    for participant in trip.participant_list.all():
                        user_stats.past_riders.add(participant)

                    user_stats.save()

        
        self.stdout.write(f'deleting {old_trips.count()} trips')
        old_trips.delete()

        old_trip_requests = TripRequest.objects.filter(latest_departure_time__lte=timezone.now())

        self.stdout.write(f'deleting {old_trip_requests.count()} trip requests')
        old_trip_requests.delete()