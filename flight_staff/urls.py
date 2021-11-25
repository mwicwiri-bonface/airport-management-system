from django.urls import path

from .views import IndexView, ButtonsView, CardsView, Error404View, BlankView, ChartsView, ForgotPasswordView, \
    TablesView, FlightStaffLoginView, FlightStaffSignUpView, LogoutView, ProfileView, ChangePasswordView

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('buttons/', ButtonsView.as_view(), name="buttons"),
    path('cards/', CardsView.as_view(), name="cards"),
    path('404/', Error404View.as_view(), name="404"),
    path('blank/', BlankView.as_view(), name="blank"),
    path('charts/', ChartsView.as_view(), name="charts"),
    path('forgot-password/', ForgotPasswordView.as_view(), name="forgot-password"),
    path('login/', FlightStaffLoginView.as_view(), name="login"),
    path('register/', FlightStaffSignUpView.as_view(), name="register"),
    path('tables/', TablesView.as_view(), name="tables"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('change-password/', ChangePasswordView.as_view(), name="change-password"),
    path('logout/', LogoutView.as_view(), name="logout"),
]
