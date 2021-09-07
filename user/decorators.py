from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def passenger_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='passenger:login'):
    """
    Decorator for views that checks that the logged in user is passenger,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_passenger and u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def staff_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='staff:login'):
    """
    Decorator for views that checks that the logged in user is a staff,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.staff and u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def flight_staff_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='flight_staff:login'):
    """
    Decorator for views that checks that the logged in user is flight staff,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_flight_staff and u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def finance_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='finance:login'):
    """
    Decorator for views that checks that the logged in user is finance,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_finance and u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
