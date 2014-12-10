#encoding:utf-8
from django.db import models
from Programas.models import CoberturaPrograma, Programa

class Cotizador(models.Model): #Clase que genera el modelo para gestionar las cotizaciones de los programas en la base de datos.
    IdCotizador = models.AutoField(primary_key=True)
    Programa = models.ForeignKey(Programa)
    PorcentajeFondo = models.IntegerField(max_length=30, null=True, blank = True)
    PorcentajeReaseguro = models.IntegerField(max_length=30, null=True, blank = True)
    Prima = models.IntegerField(max_length=30, null=True, blank = True)
    FolioCotizador = models.CharField(max_length=10, blank = True)
    TotalTarifa = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    Vigencia = models.CharField(max_length=20, blank = True)
    
    class Meta:
        verbose_name = 'Cotizador'
        verbose_name_plural = 'cotizador'
        ordering = ('IdCotizador',)
        db_table = 'cotizador'
    
    def __unicode__(self):
        return self.IdCotizador
    
class CotizadorCobertura(models.Model): #Clase que genera el modelo para gestionar las cotizaciones de las coberturas en la base de datos.
    IdCotizadorCobertura = models.AutoField(primary_key=True)
    Cotizador = models.ForeignKey(Cotizador)
    CoberturaPrograma = models.ForeignKey(CoberturaPrograma)
    Tarifa = models.DecimalField(max_digits=19, decimal_places=2, blank = True)
    Fondo = models.DecimalField(max_digits=19, decimal_places=2, blank = True)
    Reaseguro = models.DecimalField(max_digits=19, decimal_places=2, blank = True)
    Remocion = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    Deducible = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    ParticipacionAPerdida = models.DecimalField(max_digits=19, decimal_places=4, blank = True)
    
    class Meta:
        verbose_name = 'CotizadorCoberutra'
        verbose_name_plural = 'cotizadorcobertura'
        ordering = ('IdCotizadorCobertura',)
        db_table = 'cotizadorcobertura'
    
    def __unicode__(self):
        return self.IdCotizadorCobertura
    
class VigenciaCotizador(models.Model): #Clase que nos permite generar el modelo para el catálogo de la vigencia del cotizador.

    IdVigenciaCotizador = models.AutoField(primary_key=True)
    Descripcion = models.CharField(verbose_name='Descripcion', max_length=150)
    DiasVigencia = models.IntegerField(max_length=30, null=True, blank = True)
    
    class Meta:
        verbose_name = 'VigenciaCotizador'
        verbose_name_plural = 'vigenciacotizador'
        ordering = ('IdVigenciaCotizador',)
        db_table = 'vigenciacotizador'
        
    def __unicode__(self):
        return self.IdVigenciaCotizador

