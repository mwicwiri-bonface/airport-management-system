from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import User, Profile, Feedback


class Maintenance(User):
    pass

    class Meta:
        verbose_name = 'Maintenance'
        verbose_name_plural = 'Maintenances'


class MaintenanceProfile(Profile):
    user = models.OneToOneField(Maintenance, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Maintenance Profile'
        verbose_name_plural = 'Maintenances Profile'


class MaintenanceFeedback(Feedback):
    user = models.ForeignKey(Maintenance, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Maintenance Feedback'
        verbose_name_plural = 'Maintenance Feedback'


@receiver(post_save, sender=Maintenance)
def maintenance_profile(sender, instance, created, **kwargs):
    if created:
        MaintenanceProfile.objects.create(user=instance)
        instance.maintenanceprofile.save()


