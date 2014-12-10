from ConexosAgropecuarios.models import Persona, Telefono
from Login.models import UsuarioFondo
from django.contrib import admin

class UsuarioFondoAdmin(admin.ModelAdmin): #Administracion de los usuarios fondo
    list_display = ('Usuario','ClaveFondo','BaseDatos',)
    
    def Usuario(self,object): #Regresa el nombre del usuario
        return object.User.username

admin.site.register(Persona),
admin.site.register(Telefono),
admin.site.register(UsuarioFondo,UsuarioFondoAdmin),