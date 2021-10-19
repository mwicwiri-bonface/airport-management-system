from django.shortcuts import render
from django.views import View


class HomeView(View):
    template_name = "finance/index.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        pass


class LoginView(View):
    template_name = "finance/auth/sign-in.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        pass


class SignUpView(View):
    template_name = "finance/auth/sign-up.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        pass


class FormView(View):
    template_name = "finance/basic-form-elements.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        pass


class ContactView(View):
    template_name = "finance/contact.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        pass


class TableView(View):
    template_name = "finance/jquery-datatable.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        pass

