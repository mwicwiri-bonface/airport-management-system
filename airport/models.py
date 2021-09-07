from django.db import models
from djmoney.models.fields import MoneyField


class Route(models.Model):
    source = models.CharField(max_length=50)
    source_code = models.CharField(max_length=3)
    destination = models.CharField(max_length=50)
    destination_code = models.CharField(max_length=3)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)


class Plane(models.Model):
    plane_id = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)


class Flight(models.Model):
    flight_no = models.IntegerField(primary_key=True, default=1007)
    airline_name = models.CharField(max_length=50)
    no_of_seats = models.IntegerField(default=0)
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)


class Booking(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)


