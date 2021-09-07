from autoslug import AutoSlugField
from django.db import models
from djmoney.models.fields import MoneyField
from django.utils.translation import gettext_lazy as _

from passenger.models import Passenger


class Place(models.Model):
    slug = AutoSlugField(populate_from='name')
    name = models.CharField(max_length=250, unique=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)

    def __str__(self):
        return self.name


class Route(models.Model):
    slug = AutoSlugField(populate_from='code')
    code = models.CharField(max_length=100)
    source = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="source")
    destination = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="destination")
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)

    def __str__(self):
        return f"from {self.source.name} to {self.destination.name} :: {self.code}"


class Check(models.Model):
    status = models.BooleanField(default=0)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)


class Airline(models.Model):
    slug = AutoSlugField(populate_from='name')
    name = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)

    def __str__(self):
        return self.name


class Plane(models.Model):
    slug = AutoSlugField(populate_from='code')
    code = models.CharField(max_length=50, help_text="Plane number")
    name = models.CharField(max_length=100)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)

    def __str__(self):
        return f"{self.airline.name} - {self.name} :: {self.code}"


class Flight(models.Model):
    slug = AutoSlugField(populate_from='code')
    code = models.CharField(max_length=100, help_text="flight no")
    plane = models.ForeignKey(Plane, on_delete=models.CASCADE)
    seats_no = models.IntegerField(default=0, help_text="Number of seats")
    arrival = models.DateTimeField()
    departure = models.DateTimeField()
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)


class Booking(models.Model):
    slug = AutoSlugField(populate_from='code')
    code = models.CharField(max_length=20)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
