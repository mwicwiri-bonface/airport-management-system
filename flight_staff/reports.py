from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from airport.models import Booking, Flight


def bookings_report(request):
    """Generate pdf."""
    # Model data
    data = {'object_list': Booking.objects.filter(flight__plane=request.user.flightstaff.flightstaffprofile.plane)}
    # Rendered
    html_string = render_to_string('staff/reports/booking-pdf.html', data)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(result, content_type='application/pdf;')
    response['Content-Disposition'] = "inline; filename=ticket-bookings.pdf "
    return response


def flights_report(request):
    """Generate pdf."""
    # Model data
    data = {'object_list': Flight.objects.filter(plane=request.user.flightstaff.flightstaffprofile.plane)}
    # Rendered
    html_string = render_to_string('staff/reports/flights-pdf.html', data)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(result, content_type='application/pdf;')
    response['Content-Disposition'] = "inline; filename=ticket-flights.pdf "
    return response
