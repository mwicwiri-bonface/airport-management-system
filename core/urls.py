
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    # password reset
    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="accounts/password-reset/password_reset_form.html",
             html_email_template_name="accounts/password-reset/email_reset_template.html",
             subject_template_name="accounts/password-reset/password_reset_subject.txt",
         ),
         name="password_reset"),
    path('reset_password_done/',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password-reset/password_reset_done.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="accounts/password-reset/password_reset_confirm.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="accounts/password-reset/password_reset_complete.html"),
         name="password_reset_complete"),

    path('admin/', admin.site.urls),
    path('finance/', include(('finance.urls', 'finance'), namespace="finance")),
    path('staff/', include(('flight_staff.urls', 'flight_staff'), namespace="staff")),
    path('', include(('passenger.urls', 'passenger'), namespace="passenger")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'passenger.errors.error_404'
handler500 = 'passenger.errors.error_500'
handler403 = 'passenger.errors.error_403'
handler400 = 'passenger.errors.error_400'
