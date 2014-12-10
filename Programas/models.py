#encoding:utf-8
from django.db import models
from ConexosAgropecuarios.models import Persona

# Create your models here.
class TipoSeguro(models.Model): #Clase que genera el modelo TipoSeguro el cual contiene los campos para la gestión de información y el campo id persona el cual enlaza con el modelo Persona.
    
    IdTipoSeguro = models.AutoField(primary_key= True)
    DescripcionTipoSeguro =  models.CharField(max_length=12, blank = True)
    Producto = models.CharField(max_length=200, blank = True)
    
    class Meta:
        verbose_name = 'TipoSeguro'
        verbose_name_plural = 'tiposeguro'
        db_table = "tiposeguro"
        
    def __unicode__(self):
        return self.IdTipoSeguro

class SubTipoSeguro(models.Model): #Clase que genera el modelo subTipoSeguro el cual contiene los campos para la gestión de información.
    
    IdSubTipoSeguro = models.AutoField(primary_key= True)
    DescripcionSubTipoSeguro = models.CharField(max_length=12, blank = True) 
    TipoSeguro = models.ForeignKey(TipoSeguro)
    
    class Meta:
        verbose_name = 'SubTipoSeguro'
        verbose_name_plural = 'subtiposeguro'
        db_table = "subtiposeguro"
        
    def __unicode__(self):
        return self.IdSubTipoSeguro

class ContratoFondo(models.Model): # Clase que para la tabla ContratoFondo
    IdContratoFondo = models.AutoField(primary_key=True)
    NumeroContrato = models.CharField(verbose_name='Número Contrato', max_length=20)

    class Meta:
        verbose_name = 'ContratoFondo'
        verbose_name_plural = 'ContratosFondo'
        ordering = ('IdContratoFondo',)
        db_table = 'contratosfondo'
        
    def __unicode__(self):
        return self.IdContratoFondo
  
class Programa(models.Model): # Clase que genera el modelo programa el cual contiene los campos para la gestión de información.
    
    #MONEDAS = ( SE QUITA EL CHOICE PORQUE DEPENDIENDO DEL CONTRATO SE OBTIENE EL TIPO DE MONEDA
    #            ('1','PESO MEXICANO'),
    #            ('2','DOLAR ESTADOUNIDENSE'),
    #)
    
    #contratosFondo = [(e.IdContratoFondo, e.NumeroContrato) for e in ContratoFondo.objects.all()]
    
    IdPrograma = models.AutoField(primary_key= True)
    IdTipoSeguro = models.CharField(max_length=11, null=True, blank=True, verbose_name = 'Id Tipo Seguro')
    IdSubTipoSeguro = models.CharField(max_length=11, null=True, blank=True, verbose_name = 'Id Sub Tipo Seguro')
    IdTipoMoneda = models.CharField(max_length=11, null=True, blank = True)
    Ejercicio = models.CharField(max_length=4, null=True, blank=True)
    FechaPrograma = models.DateTimeField(verbose_name='Fecha Programa', null=True, blank = True)
    Observaciones = models.CharField(max_length=500, null=True, blank=True, verbose_name = 'Observaciones')
    IdContratoFondo = models.CharField(max_length=30, null=True, blank = True, verbose_name = 'Id Contrato Fondo')
    FolioPrograma = models.CharField(max_length=10, null=True, blank=True, verbose_name = 'Folio Programa')
    Utilizado = models.NullBooleanField(max_length=1, null=True, blank=True, verbose_name = 'Utilizado')
    PersonaHabilitador = models.ForeignKey(Persona)
    
    class Meta:
        verbose_name = 'Programa'
        verbose_name_plural = 'Programas'
        db_table = "Programas"
        
    def __unicode__(self):
        return self.IdPrograma
    
class Cobertura(models.Model): # Clase que genera el modelo cobertura el cual contiene los campos para la gestión de información.
    
    IdCobertura = models.AutoField(primary_key = True)
    Descripcion = models.CharField(max_length = 40, blank = True) 
    TipoSeguro = models.ForeignKey(TipoSeguro)
    
    class Meta:
        verbose_name = 'Cobertura'
        verbose_name_plural = 'cobertura'
        db_table = "cobertura"
        
    def __unicode__(self):
        return self.IdCobertura     
        
class CoberturaPrograma(models.Model): # Clase que genera el modelo CoberturaPrograma el cual contiene los campos para la gestión de información.
    
    IdCoberturaPrograma = models.AutoField(primary_key = True)    
    IdCobertura = models.IntegerField(blank = True)
    Programa = models.ForeignKey(Programa)
    
    class Meta:
        verbose_name = 'CoberturaPrograma'
        verbose_name_plural = 'coberturaprograma'
        db_table = 'coberturaprograma'
        
    def __unicode__(self):
        return self.IdCoberturaPrograma 

class AreaInfluenciaPrograma(models.Model): # Clase que genera el modelo para gestionar la información del área de influencia de los programas.
    
    IdAreaInfluenciaPrograma = models.AutoField(primary_key = True) 
    Programa = models.ForeignKey(Programa)
    IdAreaInfluencia = models.IntegerField(verbose_name = 'Area Influencia')
    
    class Meta:
        verbose_name = 'AreaInfluenciaPrograma'
        verbose_name_plural = 'areainfluenciaprograma'
        db_table = 'areainfluenciaprograma'
    
    def __unicode__(self):
        return self.IdAreaInfluenciaPrograma 