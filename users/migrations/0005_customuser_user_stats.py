# Generated by Django 4.2.6 on 2023-12-07 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_userstats"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="user_stats",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user",
                to="users.userstats",
            ),
        ),
    ]
