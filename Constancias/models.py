#encoding:utf-8
from Solicitud.models import Solicitud
from django.db import models

# Create your models here.
class Constancia(models.Model): #Clase para generar el modelo de la constancia
    IdConstancia = models.AutoField(primary_key=True)
    Solicitud = models.ForeignKey(Solicitud, verbose_name = "The related Solicitud")
    VigenciaInicio = models.DateTimeField(null=True, blank=True, verbose_name ="Fecha de Inicio de la Vigencia")
    VigenciaFin = models.DateTimeField(null=True, blank=True, verbose_name ="Fecha Final de la Vigencia")
    FechaEmision = models.DateTimeField(null=True, blank=True, verbose_name ="Fecha de Emision de la Constancia")
    FechaPago = models.DateTimeField(null=True, blank=True, verbose_name = "Fecha de Pago de la Constancia")
    FolioConstancia = models.CharField(null=True, blank=True, max_length=20, verbose_name = "Folio Constancia")
    SumaAsegurada = models.DecimalField(max_digits = 12, decimal_places = 4, null=True, blank = True, verbose_name="Suma Asegurada")
    CuotaNeta = models.DecimalField(max_digits = 12, decimal_places = 4, null=True, blank = True, verbose_name="Cuota Constancia")
    Estatus = models.IntegerField(null=True, blank=True, verbose_name ="Estado de la Constancia")
    FormaPago = models.CharField(null=True, blank=True, max_length=20, verbose_name="Forma de Pago")
    Utilizado = models.NullBooleanField(null=True, blank=True, verbose_name='Utilizado')
    UtilizadoDeclaracion = models.NullBooleanField(null=True, blank=True, verbose_name='Utilizado en Declaracion')
    
    class Meta:
        verbose_name = 'Constancia'
        verbose_name_plural = 'Constancias'
        ordering = ('IdConstancia',)
        db_table = 'Constancia'
        
    def __unicode__(self):
        return self.IdConstancia
        
class ConstanciaCobertura(models.Model): #Modelo para la generacion de la tabla Constancias Coberturas
    IdConstanciaCobertura = models.AutoField(primary_key=True)
    Constancia = models.ForeignKey(Constancia, verbose_name = "The related Constancia", on_delete = models.CASCADE)
    IdCobertura = models.IntegerField(null=True, blank=True, verbose_name = "The Related Cobertura")
    Tarifa = models.DecimalField(max_digits = 12, decimal_places = 4, null = True, blank = True, verbose_name = "Tarifa Cobertura")
    TarifaFondo = models.DecimalField(max_digits = 12, decimal_places = 4, null = True, blank = True, verbose_name = "Tarifa Fondo")
    TarifaReaseguro = models.DecimalField(max_digits = 12, decimal_places = 4, null = True, blank = True, verbose_name = "Tarifa Reaseguro")
    CuotaFondo = models.DecimalField(max_digits = 12, decimal_places = 4, null = True, blank = True, verbose_name = "Cuota Fondo")
    CuotaReaseguro = models.DecimalField(max_digits = 12, decimal_places = 4, null = True, blank = True, verbose_name = "Cuota Reaseguro")
    
    class Meta:
        verbose_name = 'ConstanciaCobertura'
        verbose_name_plural = 'ConstanciasCoberturas'
        ordering = ('IdConstanciaCobertura',)
        db_table = 'ConstanciaCobertura'
    
    def __unicode__(self):
        return self.IdConstanciaCobertura
    