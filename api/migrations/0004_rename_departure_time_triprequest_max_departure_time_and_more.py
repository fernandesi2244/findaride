# Generated by Django 4.2.6 on 2023-11-12 21:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_location_latitude_remove_location_longitude_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='triprequest',
            old_name='departure_time',
            new_name='max_departure_time',
        ),
        migrations.AddField(
            model_name='triprequest',
            name='comment',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='triprequest',
            name='min_departure_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 12, 16, 38, 28, 213449)),
            preserve_default=False,
        ),
    ]
