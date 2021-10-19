from django.db.models.signals import post_save
from django.dispatch import receiver

from finance.models import Finance, FinanceProfile


@receiver(post_save, sender=Finance)
def finance_profile(sender, instance, created, **kwargs):
    if created:
        FinanceProfile.objects.create(user=instance)
        instance.financeprofile.save()
