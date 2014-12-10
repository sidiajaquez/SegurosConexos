#encoding:utf-8
from django.forms import ModelForm, TextInput
from Programas.models import Programa
from django import forms
from django.forms.widgets import Textarea

class ProgramaForm(ModelForm):# Genera el formulario Programa a partir del  modelo Programa el cual contiene los campos del formulario y su comportamiento.
    class Meta:
        model = Programa   
         
        fields = ['IdTipoSeguro', 'IdSubTipoSeguro', 'IdTipoMoneda', 'Ejercicio', 'Observaciones', 'IdContratoFondo', 'PersonaHabilitador']   
        widgets = {
                    'IdTipoSeguro': forms.Select(attrs= {'class':'input-large'}),
                    'IdSubTipoSeguro': forms.Select(attrs= {'class':'input-large'}),
                    'IdTipoMoneda': forms.Select(attrs= {'class':'input-large'}),   
                    'Ejercicio': TextInput(attrs = {'class':'input-large'}),
                    'Observaciones':Textarea(attrs = {'class':'span9','placeholder':'Observaciones'}),    
                    'IdContratoFondo': forms.Select(attrs= {'class':'input-large'}),
                    'PersonaHabilitador': TextInput(attrs = {'class':'input-large','placeholder':'Habilitador'}),
        }