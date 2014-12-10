#encoding:utf-8
from ConexosAgropecuarios.models import Persona
from Programas.models import Programa
from django.db import models

# Create your models here.
class Solicitud(models.Model): #Clase que genera el modelo para gestionar la solicitud de aseguramiento del socio en la base de datos.
    
    DECLARACION_SOLICITUD = (
                ('ANUAL','ANUAL'),
                ('A DECLARACIÓN','A DECLARACIÓN'),
    )
    
    IdSolicitud = models.AutoField(primary_key=True)
    FolioSolicitud = models.CharField(max_length=20, null=True, blank = True,verbose_name='Folio de Solicitud')
    FechaSolicitud = models.DateTimeField(verbose_name='Fecha de Solicitud',null=True, blank = True)      
    PersonaSolicitante = models.ForeignKey(Persona, related_name = 'PersonaSolicitante')
    PersonaAsegurada = models.ForeignKey(Persona, related_name = 'PersonaAsegurada')
    PersonaContratante = models.ForeignKey(Persona, related_name = 'PersonaContratante')
    Programa = models.ForeignKey(Programa)
    Unidades = models.IntegerField(null=True, blank = True)
    ValorUnidad = models.DecimalField(max_digits = 12, decimal_places = 2, null=True, blank = True)
    DeclaracionSolicitud = models.CharField(max_length = 13, null= True, blank = True, choices = DECLARACION_SOLICITUD)
    Observaciones = models.TextField(null=True, blank=True, verbose_name ="Observaciones de la Solicitud")
    Estatus = models.NullBooleanField(null=True, blank=True, verbose_name ="Aceptado o Rechazado")

    class Meta:
        verbose_name = 'Solicitud'
        verbose_name_plural = 'Solicitudes'
        ordering = ('IdSolicitud',)
        db_table = 'Solicitud'
    
    def __unicode__(self):
        return self.IdSolicitud

class Beneficiario(models.Model): #Clase para la generacion del modelo de gestion de beneficiarios SOlicitud
    IdBeneficiario = models.AutoField(primary_key=True)
    Solicitud = models.ForeignKey(Solicitud)
    PersonaBeneficiario = models.ForeignKey(Persona)
    Porcentaje = models.DecimalField(max_digits = 12, decimal_places = 2, null=True, blank = True)
    
    class Meta:
        verbose_name = 'Beneficiario'
        verbose_name_plural = 'Beneficiarios'
        ordering = ('IdBeneficiario',)
        db_table = 'Beneficiario'

    def __unicode__(self):
        return self.IdBeneficiario
    
class RelacionAnexaSolicitud(models.Model): #Modelo para la relacion anexa de la solicitud
    IdRelacionAnexaSolicitud = models.AutoField(primary_key=True)
    Solicitud = models.ForeignKey(Solicitud, verbose_name = "The related Solicitud")
    UbicacionBienLat = models.CharField(max_length=15, null=True, blank=True, verbose_name ="Latitud del Bien")
    UbicacionBienLng = models.CharField(max_length=15, null=True, blank=True, verbose_name ="Longitud del Bien")
    CP = models.CharField(max_length=5, null=True, blank=True, verbose_name="Codigo Postal")
    DescripcionBienAsegurado = models.TextField(null=True, blank=True, verbose_name ="Descripcion del Bien Asegurado")
    ObservacionesSolicitante = models.TextField(null=True, blank=True, verbose_name ="Observaciones del Solicitante")
    FechaRelacionAnexa = models.DateField(null=True, blank=True, verbose_name ="Fecha de ELaboracion Relacion Anexa")
    
    class Meta:
        verbose_name = 'RelacionAnexaSolicitud'
        verbose_name_plural = 'RelacionAnexaSolicitudes'
        ordering = ('Solicitud',)
        db_table = 'RelacionAnexaSolicitud'
        
    def __unicode__(self):
        return self.DescripcionBienAsegurado
    
class DescripcionDetalladaBienSolicitado(models.Model): #Se genera el modelo para guardar la descripcion de los bienes para asegurar
    DECLARACION_SOLICITUD = (
                ('FACTURA','FACTURA'),
                ('PEDIMENTO','PEDIMENTO'),
                ('MANIFESTACIÓN','MANIFESTACIÓN'),
                ('AVALÚO','AVALÚO'),
                ('DECLARACIÓN DEL SOCIO','DECLARACIÓN DEL SOCIO'),
                ('OTROS','OTROS'),
    )    
    
    IdDescripcionDetalladaBienSolicitado = models.AutoField(primary_key=True)
    RelacionAnexaSolicitud = models.ForeignKey(RelacionAnexaSolicitud, verbose_name = "The related RelacionAnexaSolicitud")
    NombreEquipo = models.CharField(max_length=50, null=True, blank=True, verbose_name = "Nombre del Equipo")
    Marca = models.CharField(max_length=30, null=True, blank=True, verbose_name="Marca del Equipo")
    Modelo = models.CharField(max_length=10, null=True, blank=True, verbose_name="Modelo del Equipo")
    Serie = models.CharField(max_length=20, null=True, blank=True, verbose_name="Serie del Equipo")
    FechaBien = models.DateField(null=True, blank=True, verbose_name="Fecha Elaboracion del Bien")
    DocumentacionEvaluacion = models.CharField(max_length=30,null=True, blank=True, choices = DECLARACION_SOLICITUD,verbose_name="Documentacion para su Evaluacion")
    Cantidad = models.IntegerField(null=True, blank=True, verbose_name="Cantidad")
    ValorUnitario = models.DecimalField(max_digits = 12, decimal_places = 2, null=True, blank = True, verbose_name="Valor Unitario")
    
    class Meta:
        verbose_name = 'DescripcionDetalladaBienSolicitado'
        verbose_name_plural = 'DescripcionDetalladaBienesSolicitados'
        ordering = ('IdDescripcionDetalladaBienSolicitado',)
        db_table = 'DescripcionDetalladaBienSolicitado'
        
    def __unicode__(self):
        return self.NombreEquipo

class ActaVerificacionSolicitud(models.Model): #Modelo para Guardar el acta de verificacion
    IdActaVerificacionSolicitud = models.AutoField(primary_key=True)
    Solicitud = models.ForeignKey(Solicitud, verbose_name = "The related Solicitud")
    FechaPrellenada = models.DateField(null=True, blank=True, verbose_name="Fecha Elaboracion de Acta Prellenada")
    FechaCampo = models.DateField(null=True, blank=True, verbose_name="Fecha Elaboracion Acta de Campo")
    DictamenInspeccion = models.TextField(null=True, blank=True, verbose_name ="Dictamen de la Inspeccion")
    
    class Meta:
        verbose_name = 'ActaVerificacionSolicitud'
        verbose_name_plural = 'ActaVerificacionSolicitudes'
        ordering = ('IdActaVerificacionSolicitud',)
        db_table = 'ActaVerificacionSolicitud'
        
    def __unicode__(self):
        return self.IdActaVerificacionSolicitud
    
class MedidaSeguridadActaVerificacion(models.Model): #Modelo que guarda las medidas de seguridad que tiene el bien asegurable
    MEDIDAS_SEGURIDAD = (
                ('EXTINTORES','EXTINTORES'),
                ('HIDRANTES', 'HIDRANTES'),
    )
    IdMedidaSeguridad = models.AutoField(primary_key=True)
    ActaVerificacionSolicitud = models.ForeignKey(ActaVerificacionSolicitud, verbose_name = "The related ActaVerificacionSolicitud")
    MedidasSeguridad = models.CharField(max_length=50,null=True, blank=True, choices = MEDIDAS_SEGURIDAD,verbose_name="Medidas de Seguridad")
    
    class Meta:
        verbose_name = "MedidaSeguridadActaVerificacion"
        verbose_name_plural = "MedidasSeguridadActaVerificacion"
        ordering = ("IdMedidaSeguridad",)
        db_table = 'MedidaSeguridadActaVerificacion'
        
    def __unicode__(self):
        return self.IdMedidaSeguridad
    
class RelacionAnexaActaVerificacion(models.Model): #Modelo para la relacion anexa al acta de verificacion
    IdRelacionAnexaActaVerificacion = models.AutoField(primary_key=True)
    Solicitud = models.ForeignKey(Solicitud, verbose_name = "The related Solicitud")
    UbicacionBienLat = models.CharField(max_length=15, null=True, blank=True, verbose_name ="Latitud del Bien")
    UbicacionBienLng = models.CharField(max_length=15, null=True, blank=True, verbose_name ="Longitud del Bien")
    CP = models.CharField(max_length=5, null=True, blank=True, verbose_name="Codigo Postal")
    DescripcionBienAsegurado = models.TextField(null=True, blank=True, verbose_name ="Descripcion del Bien Asegurado")
    FechaRelacionAnexaActaVerificacion = models.DateField(null=True, blank=True, verbose_name ="Fecha de Elaboracion Relacion Anexa Acta Verificacion")
    
    class Meta:
        verbose_name = 'RelacionAnexaActaVerificacion'
        verbose_name_plural = 'RelacionAnexaActasVerificacion'
        ordering = ('Solicitud',)
        db_table = 'RelacionAnexaActaVerificacion'
        
    def __unicode__(self):
        return self.DescripcionBienAsegurado

class DescripcionBienActaVerificacion(models.Model): #Se genera el modelo para guardar la descripcion de los bienes para asegurar en la relacion anexa al acta de verificacion
    DECLARACION_SOLICITUD = (
                ('FACTURA','FACTURA'),
                ('PEDIMENTO','PEDIMENTO'),
                ('MANIFESTACIÓN','MANIFESTACIÓN'),
                ('AVALÚO','AVALÚO'),
                ('DECLARACIÓN DEL SOCIO','DECLARACIÓN DEL SOCIO'),
                ('OTROS','OTROS'),
    )    
    
    IdDescripcionBienActaVerificacion = models.AutoField(primary_key=True)
    RelacionAnexaActaVerificacion = models.ForeignKey(RelacionAnexaActaVerificacion, verbose_name = "The related RelacionAnexaActaVerificacion")
    NombreEquipo = models.CharField(max_length=50, null=True, blank=True, verbose_name = "Nombre del Equipo")
    Marca = models.CharField(max_length=30, null=True, blank=True, verbose_name="Marca del Equipo")
    Modelo = models.CharField(max_length=10, null=True, blank=True, verbose_name="Modelo del Equipo")
    Serie = models.CharField(max_length=20, null=True, blank=True, verbose_name="Serie del Equipo")
    FechaBien = models.DateField(null=True, blank=True, verbose_name="Fecha Elaboracion del Bien")
    DocumentacionEvaluacion = models.CharField(max_length=30,null=True, blank=True, choices = DECLARACION_SOLICITUD,verbose_name="Documentacion para su Evaluacion")
    Cantidad = models.IntegerField(null=True, blank=True, verbose_name="Cantidad")
    ValorUnitario = models.DecimalField(max_digits = 12, decimal_places = 2, null=True, blank = True, verbose_name="Valor Unitario")
    
    class Meta:
        verbose_name = 'DescripcionBienActaVerificacion'
        verbose_name_plural = 'DescripcionBienesActaVerificacion'
        ordering = ('IdDescripcionBienActaVerificacion',)
        db_table = 'DescripcionBienActaVerificacion'
        
    def __unicode__(self):
        return self.NombreEquipo