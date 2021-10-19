from django.shortcuts import render
from django.views import View


class HomeView(View):
    template_name = "finance/index.html"

    def get(self):
        return render(self.request, self.template_name)

    def post(self):
        pass


class LoginView(View):
    template_name = "finance/auth/sign-in.html"

    def get(self):
        return render(self.request, self.template_name)

    def post(self):
        pass


class SignUpView(View):
    template_name = "finance/auth/sign-up.html"

    def get(self):
        return render(self.request, self.template_name)

    def post(self):
        pass


class FormView(View):
    template_name = "finance/basic-form-elements.html"

    def get(self):
        return render(self.request, self.template_name)

    def post(self):
        pass


class ContactView(View):
    template_name = "finance/contact.html"

    def get(self):
        return render(self.request, self.template_name)

    def post(self):
        pass


class TableView(View):
    template_name = "finance/jquery-datatable.html"

    def get(self):
        return render(self.request, self.template_name)

    def post(self):
        pass

