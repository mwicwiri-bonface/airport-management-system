from django.urls import path

from flight_staff.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
]
