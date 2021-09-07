from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import User, Profile, Feedback


class Staff(User):
    pass

    class Meta:
        verbose_name = 'Staff'
        verbose_name_plural = 'Staffs'


class StaffProfile(Profile):
    user = models.OneToOneField(Staff, on_delete=models.CASCADE)
    dob = models.DateField(help_text="Date Of Birth")

    class Meta:
        verbose_name = 'Staff Profile'
        verbose_name_plural = 'Staffs Profile'


class StaffFeedback(Feedback):
    user = models.ForeignKey(Staff, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Staff Feedback'
        verbose_name_plural = 'Staff Feedback'


@receiver(post_save, sender=Staff)
def staff_profile(sender, instance, created, **kwargs):
    if created:
        StaffProfile.objects.create(user=instance)
        instance.staffprofile.save()

