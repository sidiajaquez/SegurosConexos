#encoding:utf-8
from Direcciones.models import Direccion
from django.forms import ModelForm, TextInput
from django import forms

class DireccionForm(ModelForm): # Clase que genera el formulario de direcciones.
    class Meta:
        model = Direccion
        fields = ['TipoDireccion','Detalle','Calle','NumeroExterior','NumeroInterior']
        widgets = {
                   'TipoDireccion':forms.Select(attrs = {'class':'input-medium'}),
                   'Detalle':TextInput(attrs = {'class':'input-xlarge','placeholder':'Detalle'}),
                   'Calle':TextInput(attrs = {'class':'input-xlarge','placeholder':'Calle'}),
                   'NumeroExterior':TextInput(attrs = {'class':'input-small','placeholder':'# Exterior'}),
                   'NumeroInterior':TextInput(attrs = {'class':'input-small','placeholder':'# Interior'}),
        }