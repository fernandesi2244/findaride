# Generated by Django 4.2.6 on 2023-11-14 21:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "api",
            "0005_rename_min_departure_time_triprequest_earliest_departure_time_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="trip",
            name="join_requests",
        ),
        migrations.RemoveField(
            model_name="triprequest",
            name="join_requests",
        ),
        migrations.AddField(
            model_name="joinrequest",
            name="trip_request",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="join_requests",
                to="api.triprequest",
            ),
        ),
        migrations.AlterField(
            model_name="trip",
            name="blacklisted_users",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="blacklisted_trips",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]