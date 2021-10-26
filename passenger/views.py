from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import CreateView

from airport.models import Place, Flight
from passenger.forms import PassengerForm, PassengerProfileForm, PassengerSignUpForm, PassengerAuthenticationForm
from passenger.models import Passenger
from user.decorators import passenger_required
from user.tokens import account_activation_token


class PassengerLoginView(LoginView):
    template_name = 'passenger/account/login.html'
    authentication_form = PassengerAuthenticationForm

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        print(form.get_user())
        login(self.request, form.get_user())
        return redirect('passenger:index')


class PassengerSignUpView(CreateView):
    form_class = PassengerSignUpForm
    template_name = "passenger/account/signup.html"

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
        return render(self.request, self.template_name, {'form': form})

    def form_valid(self, form):
        name = form.instance.first_name
        last = form.instance.last_name
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        current_site = get_current_site(self.request)
        to_email = form.cleaned_data.get('email')
        subject = f'Software Trainee Passenger Email Verification.'
        msg_plain = render_to_string('passenger/emails/email.txt', {'user_name': user.get_full_name, })
        msg_html = render_to_string('passenger/emails/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        send_mail(subject, msg_plain, 'Varal Consultancy', [to_email], html_message=msg_html)
        messages.success(self.request, f"Hi {name} {last}, your account has been created"
                                       f" successfully verify your email.")
        return redirect("passenger:login")


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


def log_out(request):
    logout(request)
    messages.info(request, f"You've logged out successfully.")
    return redirect('passenger:index')


@passenger_required
def profile(request):
    p_form = PassengerProfileForm(instance=request.user.passenger.passengerprofile)
    form = PassengerForm(request.POST, instance=request.user.passenger)
    if request.method == "POST":
        p_form = PassengerProfileForm(request.POST, request.FILES, instance=request.user.passenger.passengerprofile)
        form = PassengerForm(request.POST, instance=request.user.passenger)
        if form.is_valid() and p_form.is_valid():
            form.save()
            p_form.save()
            messages.success(request, "Your Profile has been updated!")
    context = {
        'p_form': p_form,
        'form': form,
    }
    return render(request, 'passenger/my-profile.html', context)


def faq(request):  # Not Done
    context = {}
    return render(request, 'passenger/faq.html', context)


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


class IndexView(View):
    template_name = "passenger/index.html"

    def get(self, *args, **kwargs):
        place = Place.objects.all()
        flight = Flight.objects.all()
        return render(self.request, self.template_name, {'place': place, 'flights': flight})

    def post(self, *args, **kwargs):
        pass


class AboutView(View):
    template_name = "passenger/about.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        pass


class AgentsView(View):
    template_name = "passenger/agents.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        pass


class BlogView(View):
    template_name = "passenger/blog.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        pass


class BlogDetailsView(View):
    template_name = "passenger/index.html"

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


class ProfileView(View):
    template_name = "passenger/profile.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        pass


class PropertyView(View):
    template_name = "passenger/property.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        pass


class PropertyComparisonView(View):
    template_name = "passenger/property-comparison.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        pass


class PropertyDetailsView(View):
    template_name = "passenger/property-details.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        pass


class PropertySubmitView(View):
    template_name = "passenger/property-submit.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        pass


def error(request):
    return render(request, 'passenger/error/404.html')


def about_us(request):
    return render(request, 'passenger/about-us.html')


def payment_method(request):
    return render(request, 'passenger/payment-method.html')


def booking(request):
    return render(request, 'passenger/booking.html')


def contact(request):
    return render(request, 'passenger/contact.html')


def flights(request):
    return render(request, 'passenger/flights.html')


def index(request):
    return render(request, 'passenger/index.html')


def signup(request):
    return render(request, 'passenger/signup.html')


def success_page(request):
    return render(request, 'passenger/success-page.html')


def receipts(request):
    return render(request, 'passenger/receipts.html')