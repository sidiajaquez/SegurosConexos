#encoding:utf-8
from django.forms import ModelForm, TextInput
from Cotizador.models import Cotizador
from django import forms

class CotizadorForm(ModelForm):# Genera el formulario Cotizador a partir del  modelo Cotizador el cual contiene los campos del formulario y su comportamiento.
    class Meta:
        model = Cotizador   
         
        fields = ['PorcentajeFondo', 'PorcentajeReaseguro']   
        widgets = {
                    'PorcentajeFondo': TextInput(attrs = {'class':'input-mini','required':''}),
                    'PorcentajeReaseguro': TextInput(attrs = {'class':'input-mini','required':''}),
        }