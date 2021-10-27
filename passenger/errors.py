from django.shortcuts import render


def error_404(request, exception):
    return render(request, 'passenger/error/404.html')


def error_403(request, exception):
    return render(request, 'passenger/error/403.html')


def error_500(request):
    return render(request, 'passenger/error/500.html')


def error_400(request, exception):
    return render(request, 'passenger/error/400.html')