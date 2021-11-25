from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from utils.utils import generate_key

GENDER_TYPES = (
    ('m', 'Male'),
    ('f', 'Female')
)


class User(AbstractUser):
    slug = AutoSlugField(populate_from='slug_name')
    is_passenger = models.BooleanField(default=False, help_text="Means user can login to disposer's portal")
    is_flight_staff = models.BooleanField(default=False, help_text="Means user can login to staff portal")
    is_finance = models.BooleanField(default=False, help_text="Means user can login to finance portal")
    is_archived = models.BooleanField(default=False, help_text="Means User cannot login")
    is_verified = models.BooleanField(default=False, help_text="Means email is valid")
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True,
                                   help_text="means last time table instance was edited")
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True,
                                   help_text="time table instance was created")

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def slug_name(self):
        slug = generate_key(8, 8)
        return slug


class Profile(models.Model):
    slug = AutoSlugField(populate_from='slug_name')
    country = CountryField(blank_label="Select country", default="ke")
    image = models.ImageField(upload_to='user/profile/%Y/%m/', default="user/profile/default.jpg")
    gender = models.CharField(
        choices=GENDER_TYPES,
        default='m',
        max_length=2,
        null=True,
        blank=True
    )
    phone_number = PhoneNumberField(blank=True, null=True)
    is_active = models.BooleanField(_('Active'), default=False, help_text=_('Activated, users profile is published'))
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)

    @property
    def slug_name(self):
        slug = generate_key(8, 8)
        return slug


class Feedback(models.Model):
    slug = AutoSlugField(populate_from='slug_name')
    subject = models.CharField(max_length=200)
    message = models.TextField(help_text="Feedback sent by users to admin")
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin", null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.subject}"

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback'

    @property
    def slug_name(self):
        slug = generate_key(8, 8)
        return slug


# signal to send an email to the admin when a user creates a new account
@receiver(post_save, sender=User, dispatch_uid='register')
def register(sender, instance, **kwargs):
    if kwargs.get('created', False):
        subject = 'Verification of the %s account' % instance.get_full_name
        message = 'A new user has registered'
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, [from_email], fail_silently=False)


# automatically sends mail to applicant when they click apply button
@receiver(post_save, sender=Feedback)
def feedback(sender, instance, created, **kwargs):
    if created:
        print(instance.admin.email)
        to_email = instance.admin.email
        subject = instance.subject
        msg_plain = render_to_string('applicant/emails/feedback.txt', {'message': instance.message, })
        msg_html = render_to_string('applicant/emails/feedback.html', {
            'instance': instance,
        })
        send_mail(subject, msg_plain, 'Varal Software Trainee', [to_email], html_message=msg_html)
