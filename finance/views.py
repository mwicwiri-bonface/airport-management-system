from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views import View

from finance.forms import FinanceAuthenticationForm


class HomeView(View):
    template_name = "finance/index.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        pass


class FinanceLoginView(LoginView):
    template_name = "finance/accounts/login.html"
    authentication_form = FinanceAuthenticationForm

    def form_valid(self, form):
        login(self.request, form.get_user())
        messages.success(self.request, "You've logged in successfully.")
        return redirect("finance:index")


class SignUpView(View):
    template_name = "finance/accounts/register.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        pass


class FormView(View):
    template_name = "finance/page-profile.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        pass


class ContactView(View):
    template_name = "finance/app-contact.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        pass


class TableView(View):
    template_name = "finance/project-list.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        pass
