#encoding:utf-8
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.http import HttpResponse
from dajax.core import Dajax
from ConexosAgropecuarios.models import ContratoFondo, Moneda

@dajaxice_register
def MonedaContratoReaseguro(request, IdContratoReaseguro): #Metodo que recibe el tipo de contrato seleccionado en el combo para buscar las posibles monedas en el que puede asegurarse
    ContratoFondoReaseguro = ContratoFondo.objects.get(IdContratoFondo = IdContratoReaseguro)
    Monedas = list()
    if ContratoFondoReaseguro.IdMoneda == 3: #Si es pesos y dolares
        for i in [1,2]:
            TipoMoneda = Moneda.objects.using('catalogos').get(IdMoneda = i)
            Monedas.append({"IdMoneda": TipoMoneda.IdMoneda,'DescripcionMoneda':TipoMoneda.Descripcion})
    else:
        TipoMoneda = Moneda.objects.using('catalogos').get(IdMoneda = ContratoFondoReaseguro.IdMoneda)
        Monedas.append({"IdMoneda": TipoMoneda.IdMoneda,'DescripcionMoneda':TipoMoneda.Descripcion})
       
        
    return simplejson.dumps({'Monedas':Monedas})
    