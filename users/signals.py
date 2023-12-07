from django_cas_ng.signals import cas_user_authenticated, cas_user_logout
from django.dispatch import receiver
from .models import UserStats
import json

@receiver(cas_user_authenticated)
def cas_user_authenticated_callback(sender, user, created, attributes, **kwargs):
    if created: 
        names = attributes['pudisplayname'].split(',')
        user.first_name = names[1]
        user.last_name = names[0]
        user.email = attributes['mail']
        #for now
        user.is_staff = True
        user.is_superuser = True
        user.save()

        user_stats = UserStats()
        user_stats.save()
        user.user_stats = user_stats
        user.save()
        print(f'created user: {names[1]} {names[0]}, email: {user.email}')

