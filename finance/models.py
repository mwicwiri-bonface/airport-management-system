from autoslug import AutoSlugField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField

from airport.models import Booking
from passenger.models import Passenger
from user.models import User, Profile, Feedback


class Finance(User):
    pass

    class Meta:
        verbose_name = 'Finance'
        verbose_name_plural = 'Finances'


class FinanceProfile(Profile):
    user = models.OneToOneField(Finance, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Finance Profile'
        verbose_name_plural = 'Finances Profile'


class FinanceFeedback(Feedback):
    user = models.ForeignKey(Finance, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Finance Feedback'
        verbose_name_plural = 'Finance Feedback'


class Payment(models.Model):
    slug = AutoSlugField(populate_from='name')
    code = models.CharField(max_length=20)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, null=True)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')
    mpesa = models.CharField(max_length=100, help_text="This is the M-Pesa Code for the transaction")
    finance = models.ForeignKey(Finance, on_delete=models.CASCADE, help_text="Finance officer")
    is_confirmed = models.BooleanField(default=False)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)


