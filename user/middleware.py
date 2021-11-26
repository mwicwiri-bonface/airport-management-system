from django.http import HttpResponseRedirect
from django.urls import reverse


class FinanceRequiredMiddleware(object):
    """
    Middleware that checks that the logged in user is Finance,
    redirects to the log-in page if necessary.
    """
    FINANCE_REQUIRED_URLS = ['finance/', "finance/change-password/", "finance/profile/", "finance/feedback/",
                             "finance/payments/", "finance/payments-pdf/"]

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
    Middleware that checks that the logged in user is Flight Staff,
    redirects to the log-in page if necessary.
    """
    FLIGHT_STAFF_REQUIRED_URLS = ['staff/', "staff/change-password/", "staff/profile/", "staff/feedback/",
                                  "staff/bookings/", "staff/flights/", "staff/attendants/", "staff/flights-pdf/",
                                  "staff/bookings-pdf/"]

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
