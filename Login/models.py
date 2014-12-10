from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UsuarioFondo(models.Model): #Modelo para el profile de los usuarios
    User = models.OneToOneField(User)
    ClaveFondo = models.CharField(max_length=4, null=True, blank = True,verbose_name='Clave del Fondo')
    BaseDatos = models.CharField(max_length=30, null=True, blank=True, verbose_name='Base de Datos')
    
    #def __unicode__(self): Se omite el metodo ya que en el admin se personalizan los campos de retorno
        #if self.ClaveFondo and self.BaseDatos:
        #    return self.ClaveFondo + ' ' + self.BaseDatos
        #else: 
        #    return self.User.username + ' ' + self.User.first_name + ' ' + self.User.last_name
    
    class Meta:
        verbose_name = 'UsuarioFondo'
        verbose_name_plural = 'UsuariosFondos'  

# create our user object to attach to our usuariofondo object
def create_usuariofondo_user_callback(sender, instance, **kwargs):
    usuariofondo, new = UsuarioFondo.objects.get_or_create(User = instance)
    
post_save.connect(create_usuariofondo_user_callback, User)