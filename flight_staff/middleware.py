from django.http import HttpResponseRedirect
from django.conf import settings
from re import compile

EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            print('PATH IN MIDDLEWARE >>>', path)
            if not any(m.match(path) for m in EXEMPT_URLS):
                return HttpResponseRedirect(settings.LOGIN_URL)


class ClientRequiredMiddleware(object):
    """
    This middleware is to restrict paths defined in CLIENT_REQUIRED_URLS to be
    accessible by users who are clients only. Copy any paths defined in urls.py
    that are supposed to be the client view only and append to the CLIENT_REQUIRED_URLS list.
    """
    CLIENT_REQUIRED_URLS = ['client/profile/']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_client:
            path = request.path_info.lstrip('/')
            if path in self.CLIENT_REQUIRED_URLS:
                return HttpResponseRedirect('/')
