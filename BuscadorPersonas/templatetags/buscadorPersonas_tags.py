from django import template

register = template.Library()

@register.inclusion_tag('buscadorPersonas.html',takes_context=True)
def show_buscadorPersonas(context): #Tag que contiene el modal para la busqueda de personas.
    modalVacio = ''
    return {'modal':modalVacio}