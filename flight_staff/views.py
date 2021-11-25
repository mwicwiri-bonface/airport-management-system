from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView

from flight_staff.forms import FlightStaffAuthenticationForm, FlightStaffSignUpForm, FlightStaffProfileForm, \
    FlightStaffForm


class FlightStaffLoginView(LoginView):
    template_name = "staff/login.html"
    authentication_form = FlightStaffAuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"Hi {user.get_full_name}, you've logged in successfully.")
        return redirect('flight_staff:index')


class FlightStaffSignUpView(CreateView):
    form_class = FlightStaffSignUpForm
    template_name = "staff/register.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        messages.success(self.request, f"Hi {user.get_full_name}, your account has been created successfully wait for "
                                       f"approval.")
        return redirect('flight_staff:login')


class IndexView(View):
    template_name = "staff/index.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)


class ProfileView(View):
    template_name = "staff/profile.html"

    def get(self, *args, **kwargs):
        request = self.request
        p_form = FlightStaffProfileForm(instance=request.user.flightstaff.flightstaffprofile)
        form = FlightStaffForm(instance=request.user.flightstaff)
        return render(self.request, self.template_name, {"p_form": p_form, "form": form})

    def post(self, *args, **kwargs):
        request = self.request
        p_form = FlightStaffProfileForm(request.POST, request.FILES,
                                        instance=request.user.flightstaff.flightstaffprofile)
        form = FlightStaffForm(request.POST, instance=request.user.flightstaff)
        if form.is_valid() and p_form.is_valid():
            form.save()
            p_form.save()
            messages.success(request, 'profile updated successfully')
        else:
            return render(request, self.template_name, {"p_form": p_form, "form": form})
        return redirect("flight_staff:profile")


class ChangePasswordView(View):
    template_name = "staff/change-password.html"

    def get(self, *arg, **kwargs):
        request = self.request
        form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, *args, **kwargs):
        request = self.request
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
        else:
            return render(request, self.template_name, {"form": form})
        return redirect("flight_staff:change-password")


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


class TablesView(View):
    template_name = "staff/tables.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)


class LogoutView(View):
    def get(self, *args, **kwargs):
        logout(self.request)
        messages.info(self.request, f"You've logged out successfully.")
        return redirect("flight_staff:index")
