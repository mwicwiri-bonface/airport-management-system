from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm, forms

from .models import FlightStaff, FlightStaffProfile, FlightStaffFeedback


class FlightStaffSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = FlightStaff
        fields = ['last_name', 'first_name', 'email', 'username', 'user_type']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_flight_staff = True
        user.is_active = False
        if commit:
            user.save()
        return user


class FlightStaffProfileForm(ModelForm):
    class Meta:
        model = FlightStaffProfile
        fields = ['image', 'gender', 'phone_number', 'country', 'plane']


class FlightStaffForm(ModelForm):
    class Meta:
        model = FlightStaff
        fields = ['last_name', 'first_name', 'email']


class FlightStaffFeedbackForm(ModelForm):
    class Meta:
        model = FlightStaffFeedback
        fields = ['subject', 'message']


class FlightStaffAuthenticationForm(AuthenticationForm):

    def clean(self):
        super().clean()
        if self.user_cache is not None and not self.user_cache.is_flight_staff:
            logout(self.request)
            raise forms.ValidationError("Sorry invalid credentials.",
                                        code='invalid login')
