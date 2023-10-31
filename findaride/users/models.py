from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from phonenumber_field.modelfields import PhoneNumberField
from datetime import timedelta
from django.utils import timezone

from api.models import ConfirmationRequest

class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    phone_number = PhoneNumberField(blank=True)

    email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    class Meta:
        ordering = ['first_name']

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def acceptJoinRequest(self, joinRequest):
        joinRequest.participants_that_accepted.add(self)
        joinRequest.num_participants_accepted += 1
        joinRequest.save()

        if joinRequest.num_participants_accepted == joinRequest.trip_requested.num_participants:
            # send confirmation request to user that requested trip
            confirmationRequest = ConfirmationRequest.objects.create(
                join_request=joinRequest
            )

            # TODO: send email notification (or by preferred notification method) to user that informing them that all participants have accepted them


def in_24_hours():
    return timezone.now() + timedelta(hours=24)

class ActivationToken(models.Model):
    token = models.CharField(max_length=150, unique=True)
    expiry = models.DateTimeField(default=in_24_hours)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} {self.expiry.strftime("%m/%d/%Y, %H:%M:%S")}'

