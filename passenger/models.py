from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import User, Profile, Feedback


class Passenger(User):
    pass

    class Meta:
        verbose_name = 'Passenger'
        verbose_name_plural = 'Passengers'


class PassengerProfile(Profile):
    user = models.OneToOneField(Passenger, on_delete=models.CASCADE)
    dob = models.DateField(help_text="Date Of Birth", null=True)

    class Meta:
        verbose_name = 'Passenger Profile'
        verbose_name_plural = 'Passengers Profile'


class PassengerFeedback(Feedback):
    user = models.ForeignKey(Passenger, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Passenger Feedback'
        verbose_name_plural = 'Passenger Feedback'


@receiver(post_save, sender=Passenger)
def passenger_profile(sender, instance, created, **kwargs):
    if created:
        PassengerProfile.objects.create(user=instance)
        instance.passengerprofile.save()
