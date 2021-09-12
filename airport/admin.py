from admin_interface.models import Theme
from django.contrib import admin
from django.contrib.auth.models import Group

from airport.models import Place, Route, Airline, Check, Plane, Flight, Booking


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'updated', 'created')
    search_fields = ('name',)
    list_filter = ('updated', 'created')

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class AirlineAdmin(admin.ModelAdmin):
    list_display = ('name', 'updated', 'created')
    search_fields = ('name',)
    list_filter = ('updated', 'created')

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class RouteAdmin(admin.ModelAdmin):
    list_display = ('code', 'source', 'destination', 'updated', 'created')
    search_fields = ('code',)
    list_filter = ('updated', 'created')

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class PlaneAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'airline', 'updated', 'created')
    search_fields = ('code',)
    list_filter = ('updated', 'created')

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class FlightAdmin(admin.ModelAdmin):
    list_display = ('code', 'plane', 'seats_no', 'arrival', 'route', 'price', 'updated', 'created')
    search_fields = ('code',)
    list_filter = ('updated', 'created')

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class BookingAdmin(admin.ModelAdmin):
    list_display = ('code', 'flight', 'passenger', 'updated', 'created')
    search_fields = ('code',)
    list_filter = ('updated', 'created')

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


admin.site.register(Place, PlaceAdmin)
admin.site.register(Airline, AirlineAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Plane, PlaneAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Check)
admin.site.unregister(Group)
admin.site.unregister(Theme)
