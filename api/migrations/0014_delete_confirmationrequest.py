# Generated by Django 4.2.6 on 2023-12-11 21:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_alter_location_postal_code'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ConfirmationRequest',
        ),
    ]
