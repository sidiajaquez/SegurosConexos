from django.http import HttpResponse
from django.conf import settings

from xhtml2pdf import pisa
import cStringIO
import cgi
import os

def generar_pdf(html): #convierte el html en pdf
    result = cStringIO.StringIO()
    pdf = pisa.pisaDocument(cStringIO.StringIO(html.encode("UTF-8")), dest=result, link_callback = fetch_resources, encoding='UTF-8')
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))

def fetch_resources(uri,rel): #metodo utilizado para poder obtener la ruta mas amigable de las imagenes y poderlas presentar en el reporte pdf
    path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL,""))
        
    return path