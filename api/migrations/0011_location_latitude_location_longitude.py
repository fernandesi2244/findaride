# Generated by Django 4.2.6 on 2023-11-25 22:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0010_alter_joinrequest_participants_that_accepted_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="location",
            name="latitude",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="location",
            name="longitude",
            field=models.FloatField(default=0.0),
        ),
    ]
