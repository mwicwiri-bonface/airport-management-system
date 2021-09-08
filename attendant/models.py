from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import User, Profile, Feedback


class Attendant(User):
    pass

    class Meta:
        verbose_name = 'Attendant'
        verbose_name_plural = 'Attendants'


class AttendantProfile(Profile):
    user = models.OneToOneField(Attendant, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Attendant Profile'
        verbose_name_plural = 'Attendants Profile'


class AttendantFeedback(Feedback):
    user = models.ForeignKey(Attendant, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Attendant Feedback'
        verbose_name_plural = 'Attendant Feedback'


@receiver(post_save, sender=Attendant)
def attendant_profile(sender, instance, created, **kwargs):
    if created:
        AttendantProfile.objects.create(user=instance)
        instance.attendantprofile.save()

