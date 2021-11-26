from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from airport.models import Booking
from flight_staff.models import FlightStaff, FlightStaffProfile, CheckBooking


@receiver(post_save, sender=FlightStaff)
def flight_staff_profile(sender, instance, created, **kwargs):
    if created:
        FlightStaffProfile.objects.create(user=instance)
        instance.flightstaffprofile.save()


@receiver(post_save, sender=Booking)
def check(sender, instance, created, **kwargs):
    if created:
        # this ensures only attendants in same plane as passenger can check passenger bookings
        attendant = FlightStaff.objects.alias(entries=Count('checkbooking')).filter(
            user_type="attendant", is_active=True, flightstaffprofile__plane=instance.flight.plane).order_by(
            'entries').first()
        if attendant:
            CheckBooking.objects.create(ticket=instance, attendant=attendant)
            instance.checkbooking.save()
