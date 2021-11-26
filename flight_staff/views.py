from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, ListView

from airport.models import Booking, Flight
from flight_staff.forms import FlightStaffAuthenticationForm, FlightStaffSignUpForm, FlightStaffProfileForm, \
    FlightStaffForm, FlightStaffFeedbackForm, DepartureForm, ArrivalForm
from flight_staff.models import FlightStaffFeedback, FlightStaff, CheckBooking


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
        context = {}
        request = self.request
        context['bookings_count'] = Booking.objects.filter(
            flight__plane=request.user.flightstaff.flightstaffprofile.plane).count()
        context['flights_count'] = Flight.objects.filter(
            plane=request.user.flightstaff.flightstaffprofile.plane).count()
        context['attendants_count'] = FlightStaff.objects.filter(
            user_type="attendant", flightstaffprofile__plane=request.user.flightstaff.flightstaffprofile.plane).count()
        return render(self.request, self.template_name, context)


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
            instance = p_form.save(commit=False)
            # This makes sure attendant does not change plane after selecting
            if request.user.flightstaff.flightstaffprofile.plane:
                instance.plane = request.user.flightstaff.flightstaffprofile.plane
            instance.save()
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


class FeedBackView(View):
    template_name = "staff/feedback.html"

    def get(self, *arg, **kwargs):
        request = self.request
        form = FlightStaffFeedbackForm()
        return render(request, self.template_name, {"form": form})

    def post(self, *args, **kwargs):
        request = self.request
        form = FlightStaffFeedbackForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user.flightstaff
            if FlightStaffFeedback.objects.filter(user=instance.user, subject=instance.subject, message=instance.message
                                                  ).exists():
                messages.info(request, f"Sorry, {instance.subject} has already been sent.")
            else:
                instance.save()
                messages.success(request, 'feedback has been sent successfully.')
        else:
            return render(request, self.template_name, {"form": form})
        return redirect("flight_staff:feedback")


class BookingListView(ListView):
    template_name = "staff/bookings.html"

    def get_queryset(self):
        request = self.request
        object_list = Booking.objects.filter(flight__plane=request.user.flightstaff.flightstaffprofile.plane)
        return object_list

    def post(self, *args, **kwargs):
        request = self.request
        check = request.POST.get('check')
        if check is not None:
            instance = get_object_or_404(Booking, id=check)
            instance = CheckBooking.objects.get(booking=instance)
            instance.status = True
            instance.save()
            messages.success(request, f"Booking has been Checked successfully")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class FlightsListView(View):
    template_name = "staff/flights.html"
    #
    # def get_queryset(self):
    #     request = self.request
    #     object_list = Flight.objects.filter(plane=request.user.flightstaff.flightstaffprofile.plane)
    #     return object_list

    def get(self, *args, **kwargs):
        request = self.request
        object_list = Flight.objects.filter(plane=request.user.flightstaff.flightstaffprofile.plane)
        context = {'d_form': DepartureForm(), 'a_form': ArrivalForm(), 'object_list': object_list}
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        request = self.request
        flight_id = request.POST.get('flight_id')
        departure = DepartureForm(request.POST)
        arrival = ArrivalForm(request.POST)
        if departure.is_valid():
            instance = get_object_or_404(Flight, id=flight_id)
            instance.departure = departure.departure
            instance.save()
            messages.success(request, f"Flight Departure has been set successfully")
        elif arrival.is_valid():
            instance = get_object_or_404(Flight, id=flight_id)
            instance.arrival = arrival.arrival
            instance.save()
            messages.success(request, f"Flight arrival has been set successfully")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AttendantsListView(ListView):
    template_name = "staff/attendants.html"

    def get_queryset(self):
        request = self.request
        object_list = FlightStaff.objects.filter(
            user_type="attendant", flightstaffprofile__plane=request.user.flightstaff.flightstaffprofile.plane)
        return object_list


class LogoutView(View):
    def get(self, *args, **kwargs):
        logout(self.request)
        messages.info(self.request, f"You've logged out successfully.")
        return redirect("flight_staff:index")
