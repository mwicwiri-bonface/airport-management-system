from django.urls import path

from finance.views import HomeView, SignUpView, FormView, ContactView, TableView, FinanceLoginView

urlpatterns = [
    path('table/', TableView.as_view(), name="table"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('form/', FormView.as_view(), name="form"),
    path('sign-up/', SignUpView.as_view(), name="sign_up"),
    path('login/', FinanceLoginView.as_view(), name="login"),
    path('', HomeView.as_view(), name="index"),

]
