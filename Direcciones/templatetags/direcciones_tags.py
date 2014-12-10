from django import template
from Direcciones.forms import DireccionForm

register = template.Library()

@register.inclusion_tag('direcciones.html',takes_context=True)
def show_direcciones(context):   
    return {'formularioDirecciones':DireccionForm(auto_id='%s')}