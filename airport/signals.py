from django.db.models.signals import post_save
from django.dispatch import receiver

from airport.models import Booking
from flight_staff.models import CheckBooking


@receiver(post_save, sender=Booking)
def booking_check(sender, instance, created, **kwargs):
    if created:
        CheckBooking.objects.create(ticket=instance)


