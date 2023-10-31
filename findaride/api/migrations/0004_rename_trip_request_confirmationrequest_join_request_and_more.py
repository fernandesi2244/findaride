# Generated by Django 4.2.6 on 2023-10-31 06:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_rename_depature_time_trip_departure_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='confirmationrequest',
            old_name='trip_request',
            new_name='join_request',
        ),
        migrations.RenameField(
            model_name='joinrequest',
            old_name='num_members_accepted',
            new_name='num_participants_accepted',
        ),
        migrations.RenameField(
            model_name='trip',
            old_name='trip_requests',
            new_name='join_requests',
        ),
        migrations.RenameField(
            model_name='trip',
            old_name='num_trip_requests',
            new_name='num_join_requests',
        ),
        migrations.AddField(
            model_name='joinrequest',
            name='participants_that_accepted',
            field=models.ManyToManyField(related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
