from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from airport.models import Plane, Booking
from user.models import User, Profile, Feedback


class FlightStaff(User):
    class UserType(models.TextChoices):
        PILOT = 'pilot', "Pilot"
        ATTENDANT = 'attendant', "Attendant"

    user_type = models.CharField(max_length=250, choices=UserType.choices, default=UserType.ATTENDANT)

    class Meta:
        verbose_name = 'Flight Staff'
        verbose_name_plural = 'Flight Staff'


class FlightStaffProfile(Profile):
    user = models.OneToOneField(FlightStaff, on_delete=models.CASCADE)
    plane = models.ForeignKey(Plane, on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name = 'Flight Staff Profile'
        verbose_name_plural = 'Flight Staff Profiles'


class FlightStaffFeedback(Feedback):
    user = models.ForeignKey(FlightStaff, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Flight Staff Feedback'
        verbose_name_plural = 'Flight Staff Feedback'


class CheckBooking(models.Model):
    status = models.BooleanField(default=False)
    attendant = models.ForeignKey(FlightStaff, on_delete=models.CASCADE, null=True)
    ticket = models.OneToOneField(Booking, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)

