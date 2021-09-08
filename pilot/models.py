from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from airport.models import Plane
from user.models import User, Profile, Feedback


class Pilot(User):
    pass

    class Meta:
        verbose_name = 'Pilot'
        verbose_name_plural = 'Pilots'


class PilotProfile(Profile):
    user = models.OneToOneField(Pilot, on_delete=models.CASCADE)
    plane = models.ForeignKey(Plane, on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name = 'Pilot Profile'
        verbose_name_plural = 'Pilots Profile'


class PilotFeedback(Feedback):
    user = models.ForeignKey(Pilot, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Pilot Feedback'
        verbose_name_plural = 'Pilot Feedback'


@receiver(post_save, sender=Pilot)
def pilot_profile(sender, instance, created, **kwargs):
    if created:
        PilotProfile.objects.create(user=instance)
        instance.pilotprofile.save()



