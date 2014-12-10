from django import template
from ConexosAgropecuarios.forms import TelefonoForm 

register = template.Library()

@register.inclusion_tag('telefonos.html',takes_context=True)
def show_telefonos(context): # Muestra el formulario de la plantilla telefonos.html para reutilizar codigo y permite cargarlo en otra plantilla
    return {'formularioTelefonos':TelefonoForm(auto_id='%s')}