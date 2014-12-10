#encoding:utf-8
from django.forms import ModelForm, TextInput
from Solicitud.models import Solicitud, RelacionAnexaSolicitud, DescripcionDetalladaBienSolicitado, ActaVerificacionSolicitud, MedidaSeguridadActaVerificacion
from django import forms
from django.forms.widgets import Textarea

class SolicitudForm(ModelForm): #Clase que genera el formulario de la solicitud de aseguramiento.
        class Meta:
            model = Solicitud
            fields = ['DeclaracionSolicitud','FolioSolicitud', 'FechaSolicitud', 'Unidades', 'ValorUnidad' ,'Observaciones']
            widgets = {
                        'DeclaracionSolicitud' : forms.Select(attrs= {'class':'input-medium'}),
                        'FolioSolicitud' : TextInput(attrs = {'class':'input-medium','placeholder':'Número Solicitud','disabled':''}),
                        'FechaSolicitud' : TextInput(attrs = {'class':'input-small','required':'','placeholder':'Fecha de Solicitud','readonly':''}),
                        'Unidades' : TextInput(attrs = {'class':'input-small','placeholder':'Unidades'}),
                        'ValorUnidad' : TextInput(attrs = {'class':'input-large','placeholder':'Valor Por Unidad'}),
                        'Observaciones' : Textarea(attrs = {'class':'span9','placeholder':'Observaciones'})
            }

class RelacionAnexaSolicitudForm(ModelForm): #Clase para generar el formulario de la relacion anexa a la solicitud
    class Meta:
        model = RelacionAnexaSolicitud
        fields = ['UbicacionBienLat','UbicacionBienLng','CP','DescripcionBienAsegurado','ObservacionesSolicitante']
        widgets = {
                   'UbicacionBienLat' : TextInput(attrs = {'class':'input-medium','placeholder':'Latitud'}),
                   'UbicacionBienLng' : TextInput(attrs = {'class':'input-medium','placeholder':'Longitud'}),
                   'CP' : TextInput(attrs = {'class':'input-small','placeholder':'CP','readonly':''}),
                   'DescripcionBienAsegurado' : Textarea(attrs = {'class':'span9','placeholder':'Descripción Bien'}),
                   'ObservacionesSolicitante' : Textarea(attrs = {'class':'span9','placeholder':'Observaciones Solicitante'})
        }

class DescripcionDetalladaBienSolicitadoForm(ModelForm): #Clase para generar la descripcion detallada de los bienes solicitados
    class Meta:
        model = DescripcionDetalladaBienSolicitado
        fields = ['NombreEquipo','Marca','Modelo','Serie','FechaBien','DocumentacionEvaluacion','Cantidad','ValorUnitario']
        widgets = {
                   'NombreEquipo' : TextInput(attrs = {'class':'input-xlarge', 'placeholder':'Equipo'}),
                   'Marca' : TextInput(attrs = {'class':'input-medium','placeholder':'Marca'}),
                   'Modelo': TextInput(attrs = {'class':'input-medium','placeholder':'Modelo'}),
                   'Serie': TextInput(attrs = {'class':'input-medium','placeholder':'Serie'}),
                   'FechaBien' : TextInput(attrs = {'class':'input-small','placeholder':'dd/mm/aaaa'}),
                   'DocumentacionEvaluacion' : forms.Select(attrs= {'class':'input-medium'}),
                   'Cantidad': TextInput(attrs = {'class':'input-medium','placeholder':'Cantidad'}),
                   'ValorUnitario': TextInput(attrs = {'class':'input-medium','placeholder':'Valor Unitario'})
        }
        
class ActaVerificacionSolicitudForm(ModelForm): #Generacion del formulario para la captura de los datos en el acta de verificacion de la solicitud
    class Meta:
        model = ActaVerificacionSolicitud
        fields = ['DictamenInspeccion']
        widgets = {
                   'DictamenInspeccion' : Textarea (attrs = {'class':'span9','placeholder':'Dictamen InspecciÓn'})
        }
        
class MedidaSeguridadActaVerificacionForm(ModelForm): #Clase para la generacion del Select para las medidas de seguridad
    class Meta:
        model = MedidaSeguridadActaVerificacion
        fields = ['MedidasSeguridad']
        widgets = {
                   'MedidasSeguridad': forms.Select(attrs= {'class':'input-medium'})
        }