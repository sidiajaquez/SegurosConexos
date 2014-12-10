#encoding:utf-8
from ConexosAgropecuarios.models import Persona
from django.db import models

class Sepomex(models.Model): # Clase que genera el modelo para gestionar la información del catálogo de sepomex.
    IdSepomex = models.IntegerField(primary_key=True, db_column='IdSepomex') # Field name made lowercase.
    DCodigo = models.CharField(max_length=5L, db_column='DCodigo', blank=True) # Field name made lowercase.
    DAsenta = models.CharField(max_length=200L, db_column='DAsenta', blank=True) # Field name made lowercase.
    DTipoAsenta = models.CharField(max_length=100L, db_column='DTipoAsenta', blank=True) # Field name made lowercase.
    DMnpio = models.CharField(max_length=200L, db_column='DMnpio', blank=True) # Field name made lowercase.
    DEstado = models.CharField(max_length=100L, db_column='DEstado', blank=True) # Field name made lowercase.
    DCiudad = models.CharField(max_length=200L, db_column='DCiudad', blank=True) # Field name made lowercase.
    DCp = models.CharField(max_length=5L, db_column='DCp', blank=True) # Field name made lowercase.
    CEstado = models.CharField(max_length=2L, db_column='CEstado', blank=True) # Field name made lowercase.
    COficina = models.CharField(max_length=5L, db_column='COficina', blank=True) # Field name made lowercase.
    CCp = models.CharField(max_length=5L, db_column='CCp', blank=True) # Field name made lowercase.
    CTipoAsenta = models.CharField(max_length=50L, db_column='CTipoAsenta', blank=True) # Field name made lowercase.
    CMnpio = models.CharField(max_length=5L, db_column='CMnpio', blank=True) # Field name made lowercase.
    IdAsentaCpCons = models.CharField(max_length=10L, db_column='IdAsentaCpcons', blank=True) # Field name made lowercase.
    DZona = models.CharField(max_length=10L, db_column='DZona', blank=True) # Field name made lowercase.
    CCveCiudad = models.CharField(max_length=5L, db_column='CCveCiudad', blank=True) # Field name made lowercase.
    
    class Meta:
        db_table = 'sepomex'

class Direccion(models.Model): #Clase que genera el modelo Direccion que permite guardar direcciones a una persona
    TIPO_DIRECCIONES = (
                    ('1','DOMICILIO'),
                    ('2','TRABAJO'),
    )
    IdDireccion = models.AutoField(primary_key=True)
    Persona = models.ForeignKey(Persona, verbose_name = 'IdPersona')
    TipoDireccion = models.CharField(max_length=2, choices= TIPO_DIRECCIONES, null=True, verbose_name = 'Tipo de Dirección')
    Detalle = models.CharField(max_length=200, null=True, blank = True, verbose_name = 'Detalle')
    Calle = models.CharField(max_length=200, null=True, blank = True, verbose_name = 'Calle')
    NumeroExterior = models.CharField(max_length=30, null=True, blank = True, verbose_name = 'Número Exterior')
    NumeroInterior = models.CharField(max_length=30, null=True, blank = True, verbose_name = 'Número Interior')
    IdSepomex = models.CharField(max_length=11, null=True, blank = True, verbose_name = 'Id Sepomex')
    
    class Meta:
        verbose_name = 'Direccion'
        verbose_name_plural = 'Direcciones'
        ordering = ('Persona',)
        db_table = "Direcciones"
        
    def __unicode__(self):
        return self.Calle
