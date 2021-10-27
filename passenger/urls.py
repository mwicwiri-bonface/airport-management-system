from django.urls import path
from .views import IndexView, AboutView, ContactView, ProfileView, PassengerLoginView, \
    PassengerSignUpView, VerifyEmail, log_out, payment_method, booking, faq, FlightsListView, change_password, \
    success_page, receipts, FeedbackView

urlpatterns = [
    path('logout/', log_out, name="logout"),
    path('verify/<uidb64>/<token>/', VerifyEmail.as_view(), name='verify'),
    path('sign-up/', PassengerSignUpView.as_view(), name="sign_up"),
    path('login/', PassengerLoginView.as_view(), name="login"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('feedback/', FeedbackView.as_view(), name="feedback"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('about/', AboutView.as_view(), name="about_us"),
    path('payment_method/', payment_method, name="payment_method"),
    path('booking/', booking, name="booking"),
    path('log_out/', log_out, name="log_out"),
    path('faq/', faq, name="faq"),
    path('flights/', FlightsListView.as_view(), name="flights"),
    path('change_password/', change_password, name="change_password"),
    path('success_page/', success_page, name="success_page"),
    path('receipts/', receipts, name="receipts"),
    path('', IndexView.as_view(), name="index"),
]
