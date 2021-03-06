from django.urls import path

from .receipts import download_ticket
from .views import IndexView, AboutView, ContactView, ProfileView, PassengerLoginView, \
    PassengerSignUpView, VerifyEmail, log_out, booking_payment, booking, faq, FlightsListView, change_password, \
    success_page, receipts, FeedbackView, booking_api, cancel_booking

urlpatterns = [
    path('logout/', log_out, name="logout"),
    path('verify/<uidb64>/<token>/', VerifyEmail.as_view(), name='verify'),
    path('sign-up/', PassengerSignUpView.as_view(), name="sign_up"),
    path('login/', PassengerLoginView.as_view(), name="login"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('feedback/', FeedbackView.as_view(), name="feedback"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('about/', AboutView.as_view(), name="about_us"),
    path('download_ticket/<slug>/', download_ticket, name="download_ticket"),
    path('cancel_booking/<slug>/', cancel_booking, name="cancel_booking"),
    path('payment/<slug>/', booking_payment, name="payment"),
    path('booking_api/', booking_api, name="booking_api"),
    path('booking/', booking, name="booking"),
    path('log_out/', log_out, name="log_out"),
    path('faq/', faq, name="faq"),
    path('flights/', FlightsListView.as_view(), name="flights"),
    path('change_password/', change_password, name="change_password"),
    path('success_page/<slug>/', success_page, name="success_page"),
    path('receipts/', receipts, name="receipts"),
    path('', IndexView.as_view(), name="index"),
]
