from django.shortcuts import render
from django.views import View


class IndexView(View):
    template_name = "staff/index.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)


class ButtonsView(View):
    template_name = "staff/buttons.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)


class CardsView(View):
    template_name = "staff/cards.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)


class Error404View(View):
    template_name = "staff/404.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)


class BlankView(View):
    template_name = "staff/blank.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)


class ChartsView(View):
    template_name = "staff/charts.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)


class ForgotPasswordView(View):
    template_name = "staff/forgot-password.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)


class LoginView(View):
    template_name = "staff/login.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)


class RegisterView(View):
    template_name = "staff/register.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)


class TablesView(View):
    template_name = "staff/tables.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

