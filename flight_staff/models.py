from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import User, Profile, Feedback


class FlightStaff(User):
    pass

    class Meta:
        verbose_name = 'FlightStaff'
        verbose_name_plural = 'FlightStaffs'


class FlightStaffProfile(Profile):
    user = models.OneToOneField(FlightStaff, on_delete=models.CASCADE)
    dob = models.DateField(help_text="Date Of Birth")

    class Meta:
        verbose_name = 'Flight Staff Profile'
        verbose_name_plural = 'FlightStaffs Profile'


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

