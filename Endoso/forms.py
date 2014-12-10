#encoding:utf-8
from django.forms import ModelForm, TextInput
from django import forms
from django.forms.widgets import Textarea
from Endoso.models import DeclaracionEndoso, SolicitudEndoso
from datetime import date

class DeclaracionEndosoForm(ModelForm): #Clase que genera el formulario de la declaracion de endoso.
    class Meta:
        model = DeclaracionEndoso
        fields = ['FechaEndoso','ExistenciaInicial', 'TarifaMensual']
        widgets = {
                    'FechaEndoso' : TextInput(attrs = {'class':'input-small','placeholder':'dd/mm/aaaa'}),
                    'ExistenciaInicial' : TextInput(attrs = {'class':'input-medium','placeholder':'Existencia Inicial'}),
                    'TarifaMensual' : TextInput(attrs = {'class':'input-medium','placeholder':'Tarifa Mensual'}),
        }

class SolicitudEndosoForm(ModelForm): #Clase que genera el formulario para la solicitud de endoso
    class Meta:
        now = date.today()
        model = SolicitudEndoso
        fields = ['TipoEndoso','FechaSolicitudEndoso','Observaciones']
        widgets = {
                   'TipoEndoso': forms.Select(attrs= {'class':'input-medium'}),
                   'FechaSolicitudEndoso':TextInput(attrs = {'class':'input-small','placeholder':'dd/mm/aaaa','value':now.strftime("%d/%m/%Y"),'readonly':'true'}),
                   'Observaciones':Textarea(attrs = {'class':'span9','placeholder':'Observaciones de la Solicitud de Endoso'})
        }