# Generated by Django 4.2.6 on 2023-11-15 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_joinrequest_trip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmationrequest',
            name='join_request',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.joinrequest'),
        ),
        migrations.AlterField(
            model_name='joinrequest',
            name='num_participants_accepted',
            field=models.IntegerField(default=0),
        ),
    ]
