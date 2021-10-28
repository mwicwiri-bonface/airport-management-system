from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm, forms

from finance.models import FinanceProfile, Finance, Payment, FinanceFeedback


class FinanceSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Finance
        fields = ['last_name', 'first_name', 'email', 'username']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_finance = True
        user.is_active = False
        if commit:
            user.save()
        return user


class FinanceProfileForm(ModelForm):
    class Meta:
        model = FinanceProfile
        fields = ['gender', 'phone_number', 'country']


class FinanceForm(ModelForm):
    class Meta:
        model = Finance
        fields = ['last_name', 'first_name', 'email']


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ['mpesa', ]

    def clean_mpesa(self):
        mpesa = self.cleaned_data.get('mpesa')
        if len(mpesa) != 10:
            raise ValidationError("Mpesa code is invalid, please confirm")
        return mpesa


class FinanceFeedbackForm(ModelForm):
    class Meta:
        model = FinanceFeedback
        exclude = ['user', ]


class FinanceAuthenticationForm(AuthenticationForm):

    def clean(self):
        super().clean()
        if self.user_cache is not None and not self.user_cache.is_finance:
            logout(self.request)
            raise forms.ValidationError('Invalid username or password', code='invalid login')
