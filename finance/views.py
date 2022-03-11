from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, ListView

from finance.forms import FinanceAuthenticationForm, FinanceFeedbackForm, FinanceProfileForm, FinanceForm, \
    FinanceSignUpForm
from finance.models import FinanceFeedback, Payment


class FinanceLoginView(LoginView):
    template_name = "finance/login.html"
    authentication_form = FinanceAuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"Hi {user.get_full_name}, you've logged in successfully.")
        return redirect('finance:index')


class FinanceSignUpView(CreateView):
    form_class = FinanceSignUpForm
    template_name = "finance/register.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        messages.success(self.request, f"Hi {user.get_full_name}, your account has been created successfully wait for "
                                       f"approval.")
        return redirect('finance:login')


class HomeView(View):
    template_name = "finance/index.html"

    def get(self, *args, **kwargs):
        context = {"pending_payments_count": Payment.objects.filter(is_confirmed=False).count(),
                   "confirmed_payments_count": Payment.objects.filter(is_confirmed=True).count()}
        return render(self.request, self.template_name, context)


class ProfileView(View):
    template_name = "finance/profile.html"

    def get(self, *args, **kwargs):
        request = self.request
        p_form = FinanceProfileForm(instance=request.user.finance.financeprofile)
        form = FinanceForm(instance=request.user.finance)
        return render(self.request, self.template_name, {"p_form": p_form, "form": form})

    def post(self, *args, **kwargs):
        request = self.request
        p_form = FinanceProfileForm(request.POST, request.FILES,
                                    instance=request.user.finance.financeprofile)
        form = FinanceForm(request.POST, instance=request.user.finance)
        if form.is_valid() and p_form.is_valid():
            form.save()
            p_form.save()
            messages.success(request, 'profile updated successfully')
        else:
            return render(request, self.template_name, {"p_form": p_form, "form": form})
        return redirect("finance:profile")


class ChangePasswordView(View):
    template_name = "finance/change-password.html"

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
        return redirect("finance:change-password")


class FeedBackView(View):
    template_name = "finance/feedback.html"

    def get(self, *arg, **kwargs):
        request = self.request
        form = FinanceFeedbackForm()
        return render(request, self.template_name, {"form": form})

    def post(self, *args, **kwargs):
        request = self.request
        form = FinanceFeedbackForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user.finance
            if FinanceFeedback.objects.filter(user=instance.user, subject=instance.subject, message=instance.message
                                              ).exists():
                messages.info(request, f"Sorry, {instance.subject} has already been sent.")
            else:
                instance.save()
                messages.success(request, 'feedback has been sent successfully.')
        else:
            return render(request, self.template_name, {"form": form})
        return redirect("finance:feedback")


class PaymentListView(ListView):
    model = Payment
    template_name = "finance/payments.html"

    def post(self, *args, **kwargs):
        request = self.request
        confirm = request.POST.get('confirm')
        undo = request.POST.get('undo')
        if confirm is not None:
            instance = get_object_or_404(Payment, id=confirm)
            instance.is_confirmed = True
            instance.finance = request.user.finance
            instance.save()
            booking = instance.booking
            booking.paid = True
            booking.save()
            messages.success(request, f"Payment has been confirmed successfully")
        elif undo is not None:
            instance = get_object_or_404(Payment, id=undo)
            instance.is_confirmed = False
            instance.finance = request.user.finance
            instance.save()
            booking = instance.booking
            booking.paid = False
            booking.save()
            messages.info(request, f"Payment has been Confirmation has been undone successfully")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class LogoutView(View):
    def get(self, *args, **kwargs):
        logout(self.request)
        messages.info(self.request, f"You've logged out successfully.")
        return redirect("finance:index")
