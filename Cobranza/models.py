#encoding:utf-8
from django.db import models
from Constancias.models import Constancia
from Solicitud.models import Solicitud
from Endoso.models import DeclaracionEndoso, DeclaracionTransporte, SolicitudEndoso

# Create your models here.
class PagoConstancia(models.Model):
    IdPago = models.AutoField(primary_key=True)
    Constancia = models.ForeignKey(Constancia, verbose_name = "The related Constancia")
    FolioRecibo = models.CharField(null=True, blank=True, max_length=20, verbose_name = "Folio Recibo")
    
    class Meta:
        verbose_name = 'PagoConstancia'
        verbose_name_plural = 'PagoConstancias'
        ordering = ('IdPago',)
        db_table = 'PagoConstancia'
        
    def __unicode__(self):
        return self.IdPago
    
class PagoEndosoDeclaracion(models.Model):
    IdPagoEndosoDeclaracion = models.AutoField(primary_key=True)
    DeclaracionEndoso = models.ForeignKey(Constancia, verbose_name = "The related Declaracion")
    FolioRecibo = models.CharField(null=True, blank=True, max_length=20, verbose_name = "Folio Recibo")
    
    class Meta:
        verbose_name = 'pagoendosodeclaracion'
        verbose_name_plural = 'pagoendosodeclaracion'
        ordering = ('IdPagoEndosoDeclaracion',)
        db_table = 'pagoendosodeclaracion'
        
    def __unicode__(self):
        return self.IdPagoEndosoDeclaracion
    
class PagoEndosoTransporte(models.Model):
    IdPagoEndosoTransporte = models.AutoField(primary_key=True)
    DeclaracionTransporte = models.ForeignKey(Constancia, verbose_name = "The related Transporte")
    FolioRecibo = models.CharField(null=True, blank=True, max_length=20, verbose_name = "Folio Recibo")
    
    class Meta:
        verbose_name = 'pagoendosotransporte'
        verbose_name_plural = 'pagoendosotransporte'
        ordering = ('IdPagoEndosoTransporte',)
        db_table = 'pagoendosotransporte'
        
    def __unicode__(self):
        return self.IdPagoEndosoTransporte
    
class PagoEndosoADC(models.Model):
    IdPagoEndosoADC = models.AutoField(primary_key=True)
    Constancia = models.ForeignKey(Constancia, verbose_name = "The related Constancia")
    SolicitudEndoso = models.ForeignKey(SolicitudEndoso, verbose_name = "The related Solicitud de Endoso")
    FechaPago = models.DateTimeField(verbose_name='Fecha de Pago',null=True, blank = True)
    MontoAPagar = models.DecimalField(max_digits = 19, decimal_places = 4, null=True, blank = True, verbose_name="Monto a Pagar")
    TipoEndoso = models.CharField(max_length=15, verbose_name = "Tipo de Endoso")
    SumaAseguradaAumento = models.DecimalField(max_digits=19, decimal_places=4, null=True, blank=True, verbose_name="Suma Asegurada Aumento")
    FolioRecibo = models.CharField(max_length=20, verbose_name = "Folio Recibo")
    FormaPago = models.CharField(max_length=20, verbose_name = "Forma de Pago")
    
    class Meta:
        verbose_name = 'pagoendosoadc'
        verbose_name_plural = 'pagoendosoadc'
        ordering = ('IdPagoEndosoADC',)
        db_table = 'pagoendosoadc'
        
    def __unicode__(self):
        return self.IdPagoEndosoADC
    
class PagoPrimaDeposito(models.Model):
    IdPagoPrimaDeposito = models.AutoField(primary_key=True)
    Constancia = models.ForeignKey(Constancia, verbose_name = "The related Constancia")
    FechaPago = models.DateTimeField(verbose_name='Fecha de Pago',null=True, blank = True)
    FolioRecibo = models.CharField(max_length=20, verbose_name = "Folio Recibo")
    Monto = models.DecimalField(max_digits = 19, decimal_places = 4, null=True, blank = True, verbose_name="Monto")
    
    class Meta:
        verbose_name = 'PagoPrimaDeposito'
        verbose_name_plural = 'pagoprimadeposito'
        db_table = 'pagoprimadeposito'
    
    def __unicode__(self):
        return self.IdPagoPrimaDeposito
    
class PagoEndosoCancelacion(models.Model):
    IdPagoEndosoCancelacion = models.AutoField(primary_key=True)
    Constancia = models.ForeignKey(Constancia, verbose_name = "The related Constancia")
    FechaPago = models.DateTimeField(verbose_name='Fecha de Pago',null=True, blank = True)
    FolioRecibo = models.CharField(max_length=20, verbose_name = "Folio Recibo")
    Monto = models.DecimalField(max_digits = 19, decimal_places = 4, null=True, blank = True, verbose_name="Monto")
    
    class Meta:
        verbose_name = 'PagoEndosoCancelacion'
        verbose_name_plural = 'pagoendosocancelacion'
        db_table = 'pagoendosocancelacion'
    
    def __unicode__(self):
        return self.IdPagoEndosoCancelacion
    
class CobroEndosoCancelacion(models.Model):
    IdCobroEndosoCancelacion = models.AutoField(primary_key=True)
    Constancia = models.ForeignKey(Constancia, verbose_name = "The related Constancia")
    FechaCobro = models.DateTimeField(verbose_name='Fecha de Cobro',null=True, blank = True)
    FolioRecibo = models.CharField(max_length=20, verbose_name = "Folio Recibo")
    Monto = models.DecimalField(max_digits = 19, decimal_places = 4, null=True, blank = True, verbose_name="Monto")
    
    class Meta:
        verbose_name = 'CobroEndosoCancelacion'
        verbose_name_plural = 'cobroendosocancelacion'
        db_table = 'cobroendosocancelacion'
    
    def __unicode__(self):
        return self.IdCobroEndosoCancelacion

class EndosoRehabilitacion(models.Model): #Metodo para llevar el control de los endosos de rehabilitacion
    IdEndosoRehabilitacion = models.AutoField(primary_key=True)
    Constancia = models.ForeignKey(Constancia, verbose_name = "The related Constancia")
    Solicitud = models.ForeignKey(Solicitud, verbose_name = "The related Solicitud")
    FolioEndoso = models.CharField(null = True, blank = True, max_length = 20, verbose_name = "Folio Endoso Rehabilitacion")
    FechaEndoso = models.DateTimeField(null=True, blank=True, verbose_name="Fecha Endoso Rehabilitacion")
    
    class Meta:
        verbose_name = 'EndosoRehabilitacion'
        verbose_name_plural = 'EndososRehabilitacion'
        ordering = ('IdEndosoRehabilitacion',)
        db_table = 'EndosoRehabilitacion'
    
    def __unicode__(self):
        return self.IdEndosoRehabilitacion
