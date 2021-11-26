from django.apps import AppConfig


class FlightStaffConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'flight_staff'

    def ready(self):
        import flight_staff.signals
