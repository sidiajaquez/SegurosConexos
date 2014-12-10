#encoding:utf-8
from django.db import models
from ConexosAgropecuarios.models import Persona, PersonalApoyo
from Constancias.models import Constancia
from django.conf import settings

import uuid
from PIL import Image
from Cotizador.models import CotizadorCobertura

# Create your models here.
class AvisoSiniestro(models.Model): #Clase que nos permite gestionar la informacion de los aivsos de siniestro en la base de datos.
    
    IdAvisoSiniestro = models.AutoField(primary_key= True)
    Constancia = models.ForeignKey(Constancia, verbose_name = "The related Constancia")
    FechaAviso = models.DateTimeField(verbose_name='FechaAviso',null=True, blank = True)
    FechaSiniestro = models.DateTimeField(verbose_name='FechaSiniestro',null=True, blank = True)
    PersonaAvisa = models.ForeignKey(Persona, related_name = 'PersonaAviso')
    PersonaTecnico = models.ForeignKey(Persona, related_name = 'PersonaTecnico')
    NombreAvisa = models.CharField(max_length=50, blank = True)
    ViaAviso = models.CharField(max_length=30, blank = True)
    DescripcionBienAfectado = models.CharField(max_length=30, blank = True)
    HoraAviso = models.CharField(max_length=8, blank = True)
    HoraSiniestro = models.CharField(max_length=8, blank = True)
    OtraVia = models.NullBooleanField(max_length=1, null=True, blank=True, verbose_name = 'Otra Via')
    FolioAviso = models.CharField(max_length=20, blank = True)
    TipoAviso = models.CharField(max_length=10, blank = True)
    CausaSiniestro = models.CharField(max_length=50, null=True, blank = True, verbose_name = 'Causa Siniestro')
    IdStatusAvisoSiniestro = models.IntegerField(blank = True)
    CausaAgravante = models.CharField(max_length=50, null=True, blank = True, verbose_name = 'Causa Agravante')
    CotizadorCobertura = models.ForeignKey(CotizadorCobertura, verbose_name = "The related Cotizador Cobertura")
    Deducible = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    ParticipacionAPerdida = models.DecimalField(max_digits=19, decimal_places=4, blank = True)    
        
    class Meta:
        verbose_name = 'AvisoSiniestro'
        verbose_name_plural = 'avisosiniestros'
        db_table = 'avisosiniestro'
        
    def __unicode__(self):
        return self.IdAvisoSiniestro

#Metodo para cambiar el nombre del archivo de imagen y su directorio
def path_and_rename_image(instance, filename):
    extension = filename.split('.')[-1]
    directory = 'siniestros'
    name = uuid.uuid4().hex
    
    return '%s/%s.%s' % (directory,name,extension)

#Metodo para cambiar el nombre del archivo del thumbnail y su directorio
def path_and_rename_thumbnail(instance, filename):
    extension = filename.split('.')[-1]
    directory = 'thumbnails_siniestros'
    name = uuid.uuid4().hex
    
    return '%s/%s.%s' % (directory,name,extension)

class ImagenSiniestro(models.Model): #Modelo para las imagenes de los siniestros
    IdImagenSiniestro = models.AutoField(primary_key=True)
    Imagen = models.ImageField(upload_to=path_and_rename_image)
    Thumbnail = models.ImageField(upload_to=path_and_rename_thumbnail)
    DateAdded = models.DateTimeField(null=True,blank=True,verbose_name='Fecha de Alta Imagen')
    
    def save(self):
        if not self.IdImagenSiniestro and not self.Imagen:
            return
        super(ImagenSiniestro,self).save()
        image = Image.open(self.Imagen)
        imageThumbnail =Image.open(self.Thumbnail)
        (width, height) = image.size
        size = scale_dimension(width, height, settings.HEIGHT_IMAGES)
        sizeThumbnail = scale_dimension(width, height, settings.HEIGHT_THUMBNAIL)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.Imagen.path)
        imageThumbnail = imageThumbnail.resize(sizeThumbnail, Image.ANTIALIAS)
        imageThumbnail.save(self.Thumbnail.path)
    
    class Meta:
        verbose_name = 'ImagenSiniestro'
        verbose_name_plural = 'ImagenesSiniestros'
        ordering = ('IdImagenSiniestro',)
        db_table = 'ImagenSiniestro'
    
    def __unicode__(self):
        return self.Imagen.name


def scale_dimension(width,height,IMAGEHEIGHT): #Metodo utilizado para cambiar los tamaños de las imagenes tanto original y thumbs
    ratio = float(height) / float(IMAGEHEIGHT)
    ancho = float(width) / float(ratio)
    
    return (int(ancho), int(IMAGEHEIGHT))
    
class BienAfectadoAviosoSiniestro(models.Model): #Clase que nos permite generar el modelo de la tabla bienafectadoavisosiniestro de la base de datos.
    
    IdBienAfectado = models.AutoField(primary_key= True)
    AvisoSiniestro = models.ForeignKey(AvisoSiniestro, verbose_name = "The related Aviso de Siniestro")
    IdBienConstancia = models.IntegerField(blank = True)
    NumeroBienAfectado = models.IntegerField(blank = True)
    EstadoDelDano = models.CharField(max_length=20, blank = True)
    Descripcion = models.CharField(max_length=500, blank = True)
    TieneAumento = models.NullBooleanField(max_length=1, null=True, blank=True, verbose_name = 'Tiene Aumento')
    
    class Meta:
        verbose_name = 'BienAfectadoAvisoSiniestro'
        verbose_name_plural = 'bienafectadoavisosiniestro'
        db_table = "bienafectadoavisosiniestro"
        
    def __unicode__(self):
        return self.IdBienAfectado   

class Improcedencia(models.Model): #Clase para la generacion del modelo de Improcedencia que se encuentra en la BD Catalogos
    IdImprocedencia = models.AutoField(primary_key=True)
    Descripcion = models.CharField(null = True, blank = True, verbose_name = 'Descripcion', max_length = 100)
    
    class Meta:
        verbose_name = 'Improcedencia'
        verbose_name_plural = 'Improcedencias'
        db_table = 'Improcedencia'
    
    def __unicode__(self):
        return self.Descripcion

class CausaSiniestro(models.Model): #Clase que nos permite generar el modelo de la tabla causasiniestro.

    IdCausaSiniestro = models.AutoField(primary_key=True)
    Descripcion = models.CharField(verbose_name='Descripcion', max_length=50) 
    
    class Meta:
        verbose_name = 'CausaSiniestro'
        verbose_name_plural = 'CausaSiniestro'
        ordering = ('IdCausaSiniestro',)
        db_table = 'causasiniestro'
        
    def __unicode__(self):
        return self.IdCausaSiniestro

class Inspeccion(models.Model): #Clase que nos permite generar el modelo de la tabla inspección.

    IdInspeccion = models.AutoField(primary_key=True)
    AvisoSiniestro = models.ForeignKey(AvisoSiniestro, verbose_name = "The related Aviso de Siniestro") 
    PersonalApoyo = models.ForeignKey(PersonalApoyo, verbose_name = "The related Personal de Apoyo")
    FolioInspeccion = models.CharField(verbose_name='Folio de Inspeccion', max_length=20)
    Constancia = models.ForeignKey(Constancia, verbose_name = "The related Constancia")
    FechaInspeccion = models.DateTimeField(verbose_name='FechaInspeccion',null=True, blank = True)
    
    class Meta:
        verbose_name = 'Inspeccion'
        verbose_name_plural = 'Inspecciones'
        db_table = 'inspeccion'
        
    def __unicode__(self):
        return self.IdInspeccion
    
class ActaSiniestro(models.Model): #Clase que nos permite generar el modelo de la tabla actasiniestro en la base de datos.
        
    IdActaSiniestro = models.AutoField(primary_key=True)
    Inspeccion = models.ForeignKey(Inspeccion, verbose_name = "The related Inspección") 
    FolioActaSiniestro = models.CharField(max_length=50, blank = True)
    TipoAviso = models.CharField(max_length=50, blank = True)
    FechaSiniestro = models.DateTimeField(verbose_name='FechaSiniestro',null=True, blank = True)
    MontoDano = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    HoraSiniestro = models.CharField(max_length=8, blank = True)
    
    class Meta:
        verbose_name = 'ActaSiniestro'
        verbose_name_plural = 'ActaSiniestro'
        db_table = 'actasiniestro'
        
    def __unicode__(self):
        return self.IdActaSiniestro
    
class BienActaSiniestro(models.Model): #Clase que nos permite generar el modelo de la tabla bienactasiniestro en la base de datos.
        
    IdBienActaSiniestro = models.AutoField(primary_key=True)
    IdBienAfectado = models.IntegerField(blank = True) 
    RiesgoAfectado = models.CharField(max_length=20, blank = True)
    UnidadesAfectadas = models.CharField(max_length=20, blank = True)
    Solvento = models.CharField(max_length=20, blank = True)
    Proporcion = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    FuePerdida = models.NullBooleanField(max_length=1, null=True, blank=True, verbose_name = 'FuePerdida')
    Monto = models.DecimalField(max_digits=19, decimal_places=4, blank = True)   
    Descripcion = models.CharField(max_length=200, blank = True)
    ActaSiniestro = models.ForeignKey(ActaSiniestro, verbose_name = "The related Acta Siniestro")
    TipoBienActaSiniestro = models.CharField(max_length=11, blank = True) 
    
    class Meta:
        verbose_name = 'bienactasiniestro'
        verbose_name_plural = 'bienesactasiniestro'
        db_table = 'bienactasiniestro'
        
    def __unicode__(self):
        return self.IdBienActaSiniestro