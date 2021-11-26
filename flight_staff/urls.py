from django.urls import path

from .reports import bookings_report, flights_report
from .views import IndexView, FlightStaffLoginView, FlightStaffSignUpView, LogoutView, ProfileView, \
    ChangePasswordView, FeedBackView, BookingListView, FlightsListView, AttendantsListView

urlpatterns = [
    path('flights-pdf/', flights_report, name="flights-pdf"),
    path('bookings-pdf/', bookings_report, name="bookings-pdf"),
    path('attendants/', AttendantsListView.as_view(), name="attendants"),
    path('flights/', FlightsListView.as_view(), name="flights"),
    path('bookings/', BookingListView.as_view(), name="bookings"),
    path('login/', FlightStaffLoginView.as_view(), name="login"),
    path('register/', FlightStaffSignUpView.as_view(), name="register"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('change-password/', ChangePasswordView.as_view(), name="change-password"),
    path('feedback/', FeedBackView.as_view(), name="feedback"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('', IndexView.as_view(), name="index"),
]
