from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import CreateView, ListView

from airport.models import Place, Flight, Booking
from passenger.forms import PassengerForm, PassengerProfileForm, PassengerSignUpForm, PassengerAuthenticationForm
from passenger.models import Passenger
from user.decorators import passenger_required
from user.tokens import account_activation_token
from utils.utils import generate_key


class PassengerLoginView(LoginView):
    template_name = 'passenger/include/accounts.html'
    authentication_form = PassengerAuthenticationForm

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        print(form.get_user())
        login(self.request, form.get_user())
        data = {'message': 'User has logged in successfully'}
        return JsonResponse(data)


class PassengerSignUpView(CreateView):
    form_class = PassengerSignUpForm
    template_name = 'passenger/include/accounts.html'

    def get_form_kwargs(self):
        kwargs = super(PassengerSignUpView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return JsonResponse(form.errors)

    def form_valid(self, form):
        name = form.instance.first_name
        last = form.instance.last_name
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        current_site = get_current_site(self.request)
        to_email = form.cleaned_data.get('email')
        subject = f'Passenger Email Verification.'
        msg_plain = render_to_string('passenger/emails/email.txt', {'user_name': user.get_full_name, })
        msg_html = render_to_string('passenger/emails/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        send_mail(subject, msg_plain, 'Air-kenya', [to_email], html_message=msg_html)
        data = {"message": f"Hi {name} {last}, your account has been created successfully verify your email."}
        return JsonResponse(data)


class VerifyEmail(View):

    def get(self, *args, **kwargs):
        uidb64 = kwargs['uidb64']
        token = kwargs['token']
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Passenger.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            if user.is_verified:
                messages.info(self.request, "you've already confirmed your email.")
            elif not user.is_verified:
                user.is_verified = True
                user.save()
                messages.info(self.request, "You've successfully verified your email. use your email to login")
            return redirect('passenger:login')
        else:
            data = {
                'message': 'The confirmation link was invalid, possibly because it has already been used.'
            }
            return JsonResponse(data)


class IndexView(View):
    template_name = "passenger/index.html"

    def get(self, *args, **kwargs):
        place = Place.objects.all()
        flight = Flight.objects.all()
        return render(self.request, self.template_name, {'place': place, 'flights': flight})

    def post(self, *args, **kwargs):
        pass


class AboutView(View):
    template_name = 'passenger/about-us.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        pass


class ContactView(View):
    template_name = "passenger/contact.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        pass


class FeedbackView(View):
    template_name = "passenger/feedback.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        pass


@method_decorator(passenger_required, name='dispatch')
class ProfileView(View):
    template_name = "passenger/profile.html"

    def get(self, *args, **kwargs):
        request = self.request
        p_form = PassengerProfileForm(instance=request.user.passenger.passengerprofile)
        form = PassengerForm(request.POST, instance=request.user.passenger)
        return render(self.request, self.template_name, {'p_form': p_form, 'form': form, })

    def post(self, *args, **kwargs):
        request = self.request
        p_form = PassengerProfileForm(request.POST, request.FILES, instance=request.user.passenger.passengerprofile)
        form = PassengerForm(request.POST, instance=request.user.passenger)
        if form.is_valid() and p_form.is_valid():
            form.save()
            p_form.save()
            messages.success(request, "Your Profile has been updated!")
        return render(self.request, self.template_name, {'p_form': p_form, 'form': form, })


class FlightsListView(ListView):
    template_name = "passenger/flights.html"
    model = Flight
    paginate_by = 5

    def get_queryset(self):
        object_list = Flight.objects.filter(departure__gte=timezone.now())
        return object_list

    def post(self, *args, **kwargs):
        city_from = self.request.POST.get('city_from')
        city_to = self.request.POST.get('city_to')
        if city_from == city_to:
            messages.info(self.request, f"sorry you can't move from {city_from} to {city_to}")
            return redirect('passenger:index')
        else:
            object_list = self.get_queryset().filter(route__source=city_from, route__destination=city_to)
        return render(self.request, self.template_name, {'object_list': object_list})


@passenger_required
def booking_api(request):
    if request.method == "POST":
        flight_id = request.POST.get('id')
        if Flight.objects.filter(id=flight_id).exists():
            flight = Flight.objects.get(id=flight_id)
            Booking.objects.create(flight=flight, passenger=request.user.passenger, code=generate_key(12, 12))
            messages.success(request, "Flight has been booked successfully")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@passenger_required
def change_password(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
    return render(request, 'passenger/change-password.html', {'form': form})


@passenger_required
def payment_method(request):
    return render(request, 'passenger/payment-method.html')


@passenger_required
def booking(request):
    return render(request, 'passenger/booking.html')


@passenger_required
def success_page(request):
    return render(request, 'passenger/success-page.html')


def faq(request):  # Not Done
    context = {}
    return render(request, 'passenger/faq.html', context)


@passenger_required
def receipts(request):
    return render(request, 'passenger/receipts.html')


def log_out(request):
    logout(request)
    messages.info(request, f"You've logged out successfully.")
    return redirect('passenger:index')
