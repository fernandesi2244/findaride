from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from phonenumber_field.modelfields import PhoneNumberField
from datetime import timedelta
from django.utils import timezone

class CustomUser(AbstractBaseUser, PermissionsMixin):
    PRINCETON = "PU"
    COLLEGE_CHOICES = [
        (PRINCETON, "Princeton University"),
    ]

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    college = models.CharField(
        max_length=5,
        choices=COLLEGE_CHOICES,
        default=PRINCETON,
    )

    phone_number = PhoneNumberField(blank=True)

    email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    user_stats = models.OneToOneField('users.UserStats', on_delete=models.CASCADE, related_name='user', null=True)

    class Meta:
        ordering = ['first_name']

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

def in_24_hours():
    return timezone.now() + timedelta(hours=24)

class UserStats(models.Model):
    miles_ridden = models.IntegerField(default=0)
    number_trips = models.IntegerField(default=0)
    past_riders = models.ManyToManyField('users.CustomUser', blank=True)

    @property
    def number_riders(self):
        # get number of distinct users I've ridden with from user.trips.all()
        distinct_riders = set()
        for trip in self.user.trips.all():
            distinct_riders.update(trip.participant_list.all().values_list('id', flat=True))
        return len(distinct_riders)

class ActivationToken(models.Model):
    token = models.CharField(max_length=150, unique=True)
    expiry = models.DateTimeField(default=in_24_hours)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} {self.expiry.strftime("%m/%d/%Y, %H:%M:%S")}'

