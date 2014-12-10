#encoding:utf-8
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from Direcciones.models import Sepomex, Direccion
from django.db.models import Q
from django.utils import simplejson

@dajaxice_register
def buscar_sepomex(req, datosBuscar): #Recibe los datos de la funcion js buscarSepomex y regresa los datos en json por medio de la variable sepomex
    dajax = Dajax() 
    try:
        catalogoSepomex = Sepomex.objects.using('catalogos').filter(Q(DCodigo__contains=datosBuscar) | Q(DAsenta__icontains=datosBuscar) | Q(DMnpio__icontains=datosBuscar) | Q(DEstado__icontains=datosBuscar) | Q(DCiudad__icontains=datosBuscar))
        datos = list()
        for sepomex in catalogoSepomex:
            datos.append({'IdSepomex':sepomex.IdSepomex,'Cp':sepomex.DCodigo,'Asentamiento':sepomex.DAsenta,'Municipio':sepomex.DMnpio,'Estado':sepomex.DEstado,'Ciudad':sepomex.DCiudad})
    except:
        return dajax.json()
    
    return simplejson.dumps({'sepomex':datos})

@dajaxice_register
def buscar_direcciones_idsepomex(req, idPersona): #Recibe los datos de la función js buscarSepomex y regresa los datos en json por medio de la variable sepomex
    dajax = Dajax()
    try:    
              
        catalogoSepomex = Direccion.objects.filter(Persona_id=idPersona)
                  
        datos = list()
        for direccion in catalogoSepomex:
            sepomex = Sepomex.objects.using('catalogos').filter(IdSepomex = direccion.IdSepomex)[0]
            datos.append({'IdDireccion':direccion.IdDireccion,'TipoDireccion':direccion.TipoDireccion,'Calle':direccion.Calle,
                          'NumeroExterior':direccion.NumeroExterior,'NumeroInterior':direccion.NumeroInterior, 'Detalle': direccion.Detalle,'IdSepomex':direccion.IdSepomex,'Cp':sepomex.DCodigo,
                          'Colonia':sepomex.DAsenta.upper(),'Ciudad':sepomex.DCiudad.upper(),'Municipio':sepomex.DMnpio.upper(),'Estado':sepomex.DEstado.upper()}) 
            
    except:
        return dajax.json()
    
    return simplejson.dumps({'direcciones':datos})

@dajaxice_register
def eliminar_direccion(request, idDireccion): #Función que recibe el idDirecciones con el cual se buscará el registro en la base de datos y se eliminara.
    dajax = Dajax()
    Direccion.objects.filter(IdDireccion = idDireccion).delete()
    
    return dajax.json()   