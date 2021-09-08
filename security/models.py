from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import User, Profile, Feedback


class Security(User):
    pass

    class Meta:
        verbose_name = 'Security'
        verbose_name_plural = 'Securitys'


class SecurityProfile(Profile):
    user = models.OneToOneField(Security, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Security Profile'
        verbose_name_plural = 'Securitys Profile'


class SecurityFeedback(Feedback):
    user = models.ForeignKey(Security, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Security Feedback'
        verbose_name_plural = 'Security Feedback'


@receiver(post_save, sender=Security)
def security_profile(sender, instance, created, **kwargs):
    if created:
        SecurityProfile.objects.create(user=instance)
        instance.securityprofile.save()



