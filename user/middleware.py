from django.http import HttpResponseRedirect
from django.urls import reverse


class FinanceRequiredMiddleware(object):
    """
    This middleware is to restrict paths defined in CLIENT_REQUIRED_URLS to be
    accessible by users who are clients only. Copy any paths defined in urls.py
    that are supposed to be the client view only and append to the CLIENT_REQUIRED_URLS list.
    """
    FINANCE_REQUIRED_URLS = ['finance/']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            if path in self.FINANCE_REQUIRED_URLS:
                return HttpResponseRedirect(reverse('finance:login'))
        elif request.user.is_authenticated and not request.user.is_finance:
            path = request.path_info.lstrip('/')
            if path in self.FINANCE_REQUIRED_URLS:
                return HttpResponseRedirect(reverse('finance:login'))


class FlightStaffRequiredMiddleware(object):
    """
    This middleware is to restrict paths defined in CLIENT_REQUIRED_URLS to be
    accessible by users who are clients only. Copy any paths defined in urls.py
    that are supposed to be the client view only and append to the CLIENT_REQUIRED_URLS list.
    """
    FLIGHT_STAFF_REQUIRED_URLS = ['staff/', "staff/change-password/", "staff/profile/", "staff/feedback/"]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            print(f"{path}, user is not logged in")
            if path in self.FLIGHT_STAFF_REQUIRED_URLS:
                return HttpResponseRedirect(reverse('flight_staff:login'))
        elif request.user.is_authenticated and not request.user.is_flight_staff:
            path = request.path_info.lstrip('/')
            if path in self.FLIGHT_STAFF_REQUIRED_URLS:
                return HttpResponseRedirect(reverse('flight_staff:login'))
