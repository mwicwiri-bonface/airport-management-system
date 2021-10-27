from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm, forms

from .models import Passenger, PassengerProfile, PassengerFeedback


class PassengerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Passenger
        fields = ['last_name', 'first_name', 'email', 'username']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_passenger = True
        user.is_active = True
        if commit:
            user.save()
        return user


class PassengerProfileForm(ModelForm):
    class Meta:
        model = PassengerProfile
        fields = ['image', 'gender', 'phone_number', 'country']


class PassengerForm(ModelForm):
    class Meta:
        model = Passenger
        fields = ['last_name', 'first_name', 'email']


class PassengerFeedbackForm(ModelForm):
    class Meta:
        model = PassengerFeedback
        fields = ['subject', 'message']


class PassengerAuthenticationForm(AuthenticationForm):

    def clean(self):
        super().clean()
        if self.user_cache is not None and not self.user_cache.is_passenger:
            logout(self.request)
            raise forms.ValidationError('Invalid username or password', code='invalid login')
