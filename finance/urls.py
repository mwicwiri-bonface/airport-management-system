from django.urls import path

from finance.views import FormView, ContactView, TableView, FinanceLoginView, LogoutView, \
    FeedBackView, ChangePasswordView, ProfileView, FinanceSignUpView, HomeView
from flight_staff.views import TablesView

urlpatterns = [
    path('login/', FinanceLoginView.as_view(), name="login"),
    path('register/', FinanceSignUpView.as_view(), name="register"),
    path('tables/', TablesView.as_view(), name="tables"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('change-password/', ChangePasswordView.as_view(), name="change-password"),
    path('feedback/', FeedBackView.as_view(), name="feedback"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('', HomeView.as_view(), name="index"),

]
