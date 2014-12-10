#encoding:utf-8
from Constancias.models import Constancia
from django.db import models

# Create your models here
class DeclaracionEndoso(models.Model): #Clase que genera el modelo para gestionar la declaración de endoso.
    
    IdDeclaracionEndoso = models.AutoField(primary_key=True)       
    Constancia = models.ForeignKey(Constancia, verbose_name = "The related Constancia")
    FechaEndoso = models.DateTimeField(verbose_name='Fecha de Solicitud',null=True, blank = True) 
    ExistenciaInicial = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    TarifaMensual = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    PeriodoInicio = models.DateTimeField(verbose_name='Periodo Inicio',null=True, blank = True)
    PeriodoFin = models.DateTimeField(verbose_name='Periodo Fin',null=True, blank = True)
    CierreMes =  models.NullBooleanField(max_length=1, null=True, blank=True, verbose_name = 'Cierre de mes')
    Observaciones = models.CharField(max_length=500, blank = True)
    DeclaracionNueva = models.NullBooleanField(max_length=1, null=True, blank=True, verbose_name = 'Declaracion nueva')
    ImportePagado = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    FechaPago = models.DateTimeField(verbose_name='Fecha Pago',null=True, blank = True)
    IdStatusDeclaracion = models.IntegerField(max_length=30, null=True, blank = True)
    FormaPago = models.CharField(max_length=20, blank = True)

    class Meta:
        verbose_name = 'DeclaracionEndoso'
        verbose_name_plural = 'declaracionendoso'
        ordering = ('IdDeclaracionEndoso',)
        db_table = 'declaracionendoso'
    
    def __unicode__(self):
        return self.IdDeclaracionEndoso
    
class DeclaracionEndosoPorDia(models.Model): #Clase que genera el modelo para gestionar la declaracion de endoso por dia.
    
    IdDeclaracionEndosoPorDia = models.AutoField(primary_key=True)       
    DeclaracionEndoso = models.ForeignKey(DeclaracionEndoso, verbose_name = "The related Endoso")
    Dia = models.IntegerField(blank = True)
    Entrada = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    Salida = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    Precio = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    Existencia = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    Valor = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    TarifaMensual = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    TarifaDiaria = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    Cuota = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    
    class Meta:
        verbose_name = 'DeclaracionEndosoPorDia'
        verbose_name_plural = 'declaracionendosopordia'
        ordering = ('IdDeclaracionEndosoPorDia',)
        db_table = 'declaracionendosopordia'
    
    def __unicode__(self):
        return self.IdDeclaracionEndosoPorDia
        
class Endoso(models.Model): #Clase que genera el modelo para gestionar el endoso.
    
    IdEndoso = models.AutoField(primary_key=True)
    DeclaracionEndoso = models.ForeignKey(DeclaracionEndoso, verbose_name = "The related Endoso")
    BienesAsegurados = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    SumaAsegurada = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    PorcentajeFondo = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    ImporteFondo = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    PorcentajeReaseguro = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    ImporteReaseguro = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    PorcentajeTotal = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    ImporteTotal = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    
    class Meta:
        verbose_name = 'Endoso'
        verbose_name_plural = 'endoso'
        ordering = ('IdEndoso',)
        db_table = 'endoso'
    
    def __unicode__(self):
        return self.IdEndoso
    
class DeclaracionTransporte(models.Model): #Clase que genera el modelo para gestionar la declaración de transporte.
    
    IdDeclaracionTransporte = models.AutoField(primary_key=True)
    PeriodoInicio = models.DateTimeField(verbose_name='Periodo de Inicio',null=True, blank = True) 
    PeriodoFin = models.DateTimeField(verbose_name='Periodo de Fin',null=True, blank = True) 
    DescripcionBienAsegurado = models.CharField(max_length=300, blank = True)   
    Observaciones = models.CharField(max_length=500, blank = True)
    Fecha = models.DateTimeField(verbose_name='Fecha',null=True, blank = True)
    Constancia = models.ForeignKey(Constancia, verbose_name = "The related Constancia")    
    CierreMes =  models.NullBooleanField(max_length=1, null=True, blank=True, verbose_name = 'Cierre de mes')
    DeclaracionNueva = models.NullBooleanField(max_length=1, null=True, blank=True, verbose_name = 'Declaracion nueva')
    ImportePagado = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    FechaPago = models.DateTimeField(verbose_name='Fecha Pago',null=True, blank = True)
    IdStatusDeclaracion = models.IntegerField(max_length=30, null=True, blank = True)
    FormaPago = models.CharField(max_length=20, blank = True)
    
    class Meta:
        verbose_name = 'DeclaracionTransporte'
        verbose_name_plural = 'declaraciontransporte'
        ordering = ('IdDeclaracionTransporte',)
        db_table = 'declaraciontransporte'
        
    def __unicode__(self):
        return self.IdDeclaracionTransporte
    
class DeclaracionTransportePorUnidad(models.Model): #Clase que genera el modelo para gestionar la declaración de transporte por unidad.
    
    IdDeclaracionTransportePorUnidad = models.AutoField(primary_key=True)
    DeclaracionTransporte = models.ForeignKey(DeclaracionTransporte, verbose_name = "The related Declaración")
    Romaneaje = models.IntegerField(max_length=30, null=True, blank = True)
    Fecha = models.DateTimeField(verbose_name='Fecha',null=True, blank = True)
    Cantidad = models.IntegerField(max_length=30, null=True, blank = True) 
    SumaAseguradaUnitaria = models.DecimalField(max_digits=19, decimal_places=4, blank = True) 
    SumaAseguradaTotal = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    Origen = models.CharField(max_length=100, blank = True)
    Destino = models.CharField(max_length=100, blank = True)
    
    class Meta:
        verbose_name = 'DeclaracionTransportePorUnidad'
        verbose_name_plural = 'declaraciontransporteporunidad'
        ordering = ('IdDeclaracionTransportePorUnidad',)
        db_table = 'declaraciontransporteporunidad'
    
    def __unicode__(self):
        return self.IdDeclaracionTransportePorUnidad
    
class SolicitudEndoso(models.Model): #Clase para el modelo de la generacion de solicitudes de endoso
    TIPO_ENDOSO = (
                   ('AUMENTO','AUMENTO'),
                   ('CANCELACIÓN','CANCELACIÓN'),
                   ('DISMINUCIÓN','DISMINUCIÓN'),
                   ('MODIFICACIÓN','MODIFICACIÓN'),
    )
    
    IdSolicitudEndoso = models.AutoField(primary_key=True)
    Constancia = models.ForeignKey(Constancia,verbose_name="The related Constancia")
    TipoEndoso = models.CharField(max_length=15,null=True,blank=True,choices=TIPO_ENDOSO,verbose_name='Tipo de Endoso')
    FechaSolicitudEndoso = models.DateTimeField(null=True,blank=True,verbose_name='Fecha de Solicitud Endoso')
    Observaciones = models.TextField(null=True,blank=True,verbose_name='Observaciones Solicitud')
    Utilizado = models.NullBooleanField(null=True,blank=True,verbose_name='Utilizado')
    FolioSolicitudEndoso = models.CharField(null=True, blank=True, max_length=30, verbose_name = "Folio Solicitud Endoso")
    ReimprimirSolicitudEndoso = models.NullBooleanField(null=True,blank=True,default=True,verbose_name='Reimprimir Solicitud Endoso')
    
    class Meta:
        verbose_name = 'SolicitudEndoso'
        verbose_name_plural = 'SolicitudesEndoso'
        ordering = ('IdSolicitudEndoso',)
        db_table = 'SolicitudEndoso'
    
    def __unicode__(self):
        return self.IdSolicitudEndoso
    
class EndosoTransporte(models.Model): #Clase que genera el modelo para gestionar el endoso de transporte en la base de datos.
    
    IdEndosoTransporte = models.AutoField(primary_key=True)
    DeclaracionTransporte = models.ForeignKey(DeclaracionTransporte, verbose_name = "The related Endoso Transporte")
    BienesAsegurados = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    SumaAsegurada = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    PorcentajeFondo = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    ImporteFondo = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    PorcentajeReaseguro = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    ImporteReaseguro = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    PorcentajeTotal = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    ImporteTotal = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    
    class Meta:
        verbose_name = 'EndosoTransporte'
        verbose_name_plural = 'endosotransporte'
        ordering = ('IdEndosoTransporte',)
        db_table = 'endosotransporte'
    
    def __unicode__(self):
        return self.IdEndosoTransporte

class DescripcionBienEndosoAD(models.Model): #Clase que genera el modelo para gestionar los endosos de aumento y disminucion de los bienes en las constancias
    DECLARACION_SOLICITUD = (
                ('FACTURA','FACTURA'),
                ('PEDIMENTO','PEDIMENTO'),
                ('MANIFESTACIÓN','MANIFESTACIÓN'),
                ('AVALÚO','AVALÚO'),
                ('DECLARACIÓN DEL SOCIO','DECLARACIÓN DEL SOCIO'),
                ('OTROS','OTROS'),
    )    
    IdDescripcionBienEndosoAD = models.AutoField(primary_key=True)
    Constancia = models.ForeignKey(Constancia, verbose_name = "The related Constancia")
    NombreEquipo = models.CharField(max_length=50, null=True, blank=True, verbose_name = "Nombre del Equipo")
    Marca = models.CharField(max_length=30, null=True, blank=True, verbose_name="Marca del Equipo")
    Modelo = models.CharField(max_length=10, null=True, blank=True, verbose_name="Modelo del Equipo")
    Serie = models.CharField(max_length=20, null=True, blank=True, verbose_name="Serie del Equipo")
    FechaBien = models.DateField(null=True, blank=True, verbose_name="Fecha Elaboracion del Bien")
    DocumentacionEvaluacion = models.CharField(max_length=30,null=True, blank=True, choices = DECLARACION_SOLICITUD,verbose_name="Documentacion para su Evaluacion")
    Cantidad = models.IntegerField(null=True, blank=True, verbose_name="Cantidad")
    ValorUnitario = models.DecimalField(max_digits = 12, decimal_places = 2, null=True, blank = True, verbose_name="Valor Unitario")
    SolicitudEndoso = models.ForeignKey(SolicitudEndoso, verbose_name = "The related SolicitudEndoso")
    Utilizado = models.NullBooleanField(null=True,blank=True,verbose_name='Utilizado')
    
    class Meta:
        verbose_name = 'DescripcionBienEndosoAD'
        verbose_name_plural = 'DescripcionBienesEndosoAD'
        ordering = ('IdDescripcionBienEndosoAD',)
        db_table = 'DescripcionBienEndosoAD'
        
    def __unicode__(self):
        return self.IdDescripcionBienEndosoAD
    
class ControlEndoso(models.Model): #Clase para la generacion del modelo que almacena todos los endosos que se realicen
    TIPO_ENDOSO = (
                   ('AUMENTO','AUMENTO'),
                   ('CANCELACIÓN','CANCELACIÓN'),
                   ('DISMINUCIÓN','DISMINUCIÓN'),
                   ('MODIFICACIÓN','MODIFICACIÓN'),
    )    
    IdControlEndoso = models.AutoField(primary_key=True)
    Constancia = models.ForeignKey(Constancia, verbose_name = "The related Constancia")
    SolicitudEndoso = models.ForeignKey(SolicitudEndoso,verbose_name = "The related SolicitudEndoso") 
    FolioEndoso = models.CharField(null=True, blank=True, max_length=30, verbose_name = "Folio Endoso")
    FechaEndoso = models.DateTimeField(null=True, blank=True, verbose_name = "Fecha del Endoso")
    TipoEndoso = models.CharField(max_length=15,null=True,blank=True,choices=TIPO_ENDOSO,verbose_name='Tipo de Endoso')
    SumaAseguradaAnterior = models.DecimalField(max_digits = 12, decimal_places = 4, null=True, blank = True, verbose_name="Suma Asegurada Anterior")
    SumaAseguradaEndoso = models.DecimalField(max_digits = 12, decimal_places = 4, null=True, blank = True, verbose_name="Suma Asegurada Endoso")
    SumaAseguradaActual = models.DecimalField(max_digits = 12, decimal_places = 4, null=True, blank = True, verbose_name="Suma Asegurada Actual")
    Estatus = models.IntegerField(null=True, blank=True, verbose_name ="Estado del Endoso")
    
    class Meta:
        verbose_name = 'ControlEndoso'
        verbose_name_plural = 'ControlEndosos'
        ordering = ('-IdControlEndoso',)
        db_table = 'ControlEndoso'
    
    def __unicode__(self):
        return self.IdControlEndoso
    
class EndosoCancelacion(models.Model): #Clase que genera el modelo para gestionar el endoso de cancelacion en la base de datos.
    
    IdEndosoCancelacion = models.AutoField(primary_key=True)
    Constancia = models.ForeignKey(Constancia, verbose_name = "The related Constancia")
    SolicitudEndoso = models.ForeignKey(SolicitudEndoso, verbose_name = "The related Solicitud Endoso")
    FolioEndosoCancelacion = models.CharField(null=True, blank=True, max_length=30, verbose_name = "Folio Endoso Cancelacion")
    FechaCancelacion = models.DateTimeField(null=True, blank=True, verbose_name = "Fecha de la cancelacion")
    Monto = models.DecimalField(max_digits = 19, decimal_places = 4, null=True, blank = True, verbose_name="Monto")
    TipoEndoso = models.CharField(max_length=4,null=True,blank=True,verbose_name='Tipo de Endoso')
    
    class Meta:
        verbose_name = 'EndosoCancelacion'
        verbose_name_plural = 'endosocancelacion'
        ordering = ('IdEndosoCancelacion',)
        db_table = 'endosocancelacion'
    
    def __unicode__(self):
        return self.IdEndosoCancelacion
    
class PeriodoPagoCuotaAnual(models.Model): #Clase que genera el modelo para almacenar el peridio de pago de la cuota anual.
    
    IdPeriodoPagoCuotaAnual = models.AutoField(primary_key=True)
    DiasDesde = models.IntegerField(null=True, blank=True, verbose_name ="Dias desde")
    DiasHasta = models.IntegerField(null=True, blank=True, verbose_name ="Dias hasta")
    Porcentaje = models.DecimalField(max_digits = 19, decimal_places = 4, null=True, blank = True, verbose_name="Porcentaje")   
    
    class Meta:
        verbose_name = 'PeriodoPagoCuotaAnual'
        verbose_name_plural = 'periodopagocuotaanual'
        ordering = ('IdPeriodoPagoCuotaAnual',)
        db_table = 'periodopagocuotaanual'
    
    def __unicode__(self):
        return self.IdPeriodoPagoCuotaAnual