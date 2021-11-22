from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from airport.models import Plane
from user.models import User, Profile, Feedback


class FlightStaff(User):
    class UserType(models.TextChoices):
        PILOT = 'pilot', "Pilot"
        SECURITY = 'security', "Security"
        MAINTENANCE = 'maintenance', "Maintenance"
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


@receiver(post_save, sender=FlightStaff)
def flight_staff_profile(sender, instance, created, **kwargs):
    if created:
        FlightStaffProfile.objects.create(user=instance)
        instance.flightstaffprofile.save()
