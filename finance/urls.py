from django.urls import path

from finance.views import HomeView, LoginView, SignUpView, FormView, ContactView, TableView

urlpatterns = [
    path('table/', TableView.as_view(), name="table"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('form/', FormView.as_view(), name="form"),
    path('sign-up/', SignUpView.as_view(), name="sign_up"),
    path('login/', LoginView.as_view(), name="login"),
    path('', HomeView.as_view(), name="index"),

]
