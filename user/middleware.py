from django.http import HttpResponseRedirect
from django.urls import reverse


class FinanceRequiredMiddleware(object):
    FINANCE_REQUIRED_URLS = ['finance/', "finance/change-password/", "finance/profile/", "finance/feedback/"]

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
