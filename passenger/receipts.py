from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from airport.models import Booking


def download_ticket(request, slug):
    """Generate pdf."""
    # Model data
    data = {'object': Booking.objects.get(id=slug)}
    # Rendered
    html_string = render_to_string('passenger/receipts/ticket-pdf.html', data)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(result, content_type='application/pdf;')
    response['Content-Disposition'] = f"inline; filename=ticket-{data['object'].code}.pdf "
    return response
