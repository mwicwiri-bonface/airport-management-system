from django.urls import path

from .views import IndexView, FlightStaffLoginView, FlightStaffSignUpView, LogoutView, ProfileView, \
    ChangePasswordView, FeedBackView

urlpatterns = [
    path('login/', FlightStaffLoginView.as_view(), name="login"),
    path('register/', FlightStaffSignUpView.as_view(), name="register"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('change-password/', ChangePasswordView.as_view(), name="change-password"),
    path('feedback/', FeedBackView.as_view(), name="feedback"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('', IndexView.as_view(), name="index"),
]
