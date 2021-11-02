from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def passenger_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='passenger:index'):
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


def pilot_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='pilot:login'):
    """
    Decorator for views that checks that the logged in user is a pilot,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_pilot and u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def security_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='security:login'):
    """
    Decorator for views that checks that the logged in user is security,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_security and u.is_authenticated,
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


def attendant_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='attendant:login'):
    """
    Decorator for views that checks that the logged in user is attendant,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_attendant and u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def maintenance_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='maintenance:login'):
    """
    Decorator for views that checks that the logged in user is maintenance,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_maintenance and u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
