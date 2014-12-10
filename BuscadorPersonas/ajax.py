#encoding:utf-8
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from ConexosAgropecuarios.models import Persona, Telefono
from Direcciones.models import Direccion, Sepomex 
from django.db.models import Q
from django.utils import simplejson

@dajaxice_register
def buscar_persona(req,datosBuscar,tipoPersona): #Recibe el dato por el cual se filtrará la busqueda de personas y un indicador de si es persona fisica 'F o moral 'M' y retorna la información de las personas encontradas.
    dajax = Dajax()
    try:
        datos = list()
        if tipoPersona == 'F':
            personas = Persona.objects.filter((Q(Rfc__contains=datosBuscar) | Q(PrimerNombre__contains=datosBuscar) | Q(SegundoNombre__contains=datosBuscar) | Q(ApellidoPaterno__contains=datosBuscar) | Q(ApellidoMaterno__contains=datosBuscar)),Q(TipoPersona=tipoPersona))
            
            for persona in personas:
                datos.append({'IdPersona':persona.IdPersona,'Nombre':persona.PrimerNombre + " " + persona.SegundoNombre,'ApellidoPaterno':persona.ApellidoPaterno,'ApellidoMaterno':persona.ApellidoMaterno,'Rfc':persona.Rfc})
                
        elif tipoPersona == 'M':
            personas = Persona.objects.filter(Q(RazonSocial__contains=datosBuscar),Q(TipoPersona=tipoPersona))
           
            for persona in personas:
                datos.append({'IdPersona':persona.IdPersona,'RazonSocial':persona.RazonSocial,'Rfc':persona.Rfc}) 
        
        elif tipoPersona == 'T':
            personas = Persona.objects.filter(Q(RazonSocial__contains=datosBuscar) | Q(Rfc__contains=datosBuscar) | Q(PrimerNombre__contains=datosBuscar) | Q(SegundoNombre__contains=datosBuscar) | Q(ApellidoPaterno__contains=datosBuscar) | Q(ApellidoMaterno__contains=datosBuscar))
           
            for persona in personas:
                direccion = Direccion.objects.filter(Persona_id = persona.IdPersona)[0]
                telefono = Telefono.objects.filter(IdPersona_id = persona.IdPersona)[0]
                datos.append({'IdPersona':persona.IdPersona,'RazonSocial':persona.RazonSocial, 'Nombre':persona.PrimerNombre + " " + persona.SegundoNombre + " " + persona.ApellidoPaterno + " " + persona.ApellidoMaterno, 'Rfc':persona.Rfc, 'TipoPersona': persona.TipoPersona,'Direccion':direccion.Calle,'Telefono':telefono.Numero})                        
                               
    except:
        return dajax.json()
    
    return simplejson.dumps({'personas':datos})

@dajaxice_register
def obtener_Persona_IdPersona(req, idPersona): #Función que busca una persona mediante un idpersona, retorna la persona encontrada.
    dajax = Dajax()
    try:
        personas = Persona.objects.filter(IdPersona = idPersona)
        datos = list()
        for persona in personas:
            fecha = persona.FechaNacimiento.strftime("%d/%m/%Y")
            datos.append({'IdPersona':persona.IdPersona,'PrimerNombre':persona.PrimerNombre,'SegundoNombre':persona.SegundoNombre,'ApellidoPaterno':persona.ApellidoPaterno,'ApellidoMaterno':persona.ApellidoMaterno,'Rfc':persona.Rfc,'Curp':persona.Curp,'Sexo':persona.Sexo,'Email':persona.Email, 'EstadoCivil':persona.EstadoCivil,'FechaNacimiento': str(fecha), 'EsSocio':persona.EsSocio, 'TipoPersona':persona.TipoPersona, 'RazonSocial':persona.RazonSocial})
    
    except:
        return dajax.json()
    
    return simplejson.dumps({'personas':datos})

@dajaxice_register
def buscar_todas_personas(req,datosBuscar,esSocio):
    dajax = Dajax()
    try:

        if esSocio=="1":           
            personas = Persona.objects.filter((Q(Rfc__contains=datosBuscar) | Q(RazonSocial__contains=datosBuscar) | Q(PrimerNombre__contains=datosBuscar) | Q(SegundoNombre__contains=datosBuscar) | Q(ApellidoPaterno__contains=datosBuscar) | Q(ApellidoMaterno__contains=datosBuscar)),Q(EsSocio=esSocio))
        else:
            personas = Persona.objects.filter(Q(Rfc__contains=datosBuscar) | Q(RazonSocial__contains=datosBuscar) | Q(PrimerNombre__contains=datosBuscar) | Q(SegundoNombre__contains=datosBuscar) | Q(ApellidoPaterno__contains=datosBuscar) | Q(ApellidoMaterno__contains=datosBuscar))

 
        datos = list()
        
        for persona in personas:
            #Se busca la direccion del socio por si alguno no tuviera se manda vacio
            direccionDatosPersona = Direccion.objects.filter(Persona = persona.IdPersona)
            DomicilioPersona = ''
            IdSepomexPersona = ''
            for direccionPersona in direccionDatosPersona:
                DomicilioPersona = direccionPersona.Calle
                IdSepomexPersona = direccionPersona.IdSepomex
                if direccionPersona.TipoDireccion == "2":
                    DomicilioPersona = direccionPersona.Calle
                    IdSepomexPersona = direccionPersona.IdSepomex
                    break

            #Se busca el telefono de la persona, por si no tuviera se manda en blaco
            telefonoDatosPersona = Telefono.objects.filter(IdPersona = persona.IdPersona)
            TelefonoPersona = ''
            for telefonoPersona in telefonoDatosPersona:
                TelefonoPersona = telefonoPersona.Numero
                if telefonoPersona.TipoTelefono == 'TRABAJO':
                    TelefonoPersona = telefonoPersona.Numero
                    break

            if IdSepomexPersona == '':
                CP =''
                Municipio = ''
                Estado = ''
            else:
                DireccionSepomex = Sepomex.objects.using('catalogos').filter(IdSepomex = IdSepomexPersona)[0]
                CP = DireccionSepomex.DCp
                Municipio = DireccionSepomex.DMnpio
                Estado = DireccionSepomex.DEstado
                
            datos.append({'IdPersona':persona.IdPersona,'Rfc':persona.Rfc,'PrimerNombre':persona.PrimerNombre,'SegundoNombre':persona.SegundoNombre,'RazonSocial':persona.RazonSocial,'ApellidoPaterno':persona.ApellidoPaterno,'ApellidoMaterno':persona.ApellidoMaterno,'Direccion':DomicilioPersona,'Telefono':TelefonoPersona,'CP':CP,'Municipio':Municipio,'Estado':Estado})
    
    except:
        return dajax.json()
    
    return simplejson.dumps({'personas':datos})

@dajaxice_register
def obtenerPersonaPorTipo(req,datosBuscar,tipoPersona): # Función que obtiene la información de las personas que tienen relacion con datosBuscar el cual filtra por tipo de persona.
    dajax = Dajax()
    try:

        if tipoPersona == 'F':
            personas = Persona.objects.filter((Q(Rfc__contains=datosBuscar) | Q(PrimerNombre__contains=datosBuscar) | Q(SegundoNombre__contains=datosBuscar) | Q(ApellidoPaterno__contains=datosBuscar) | Q(ApellidoMaterno__contains=datosBuscar)),Q(TipoPersona=tipoPersona))
                            
        elif tipoPersona == 'M':
            personas = Persona.objects.filter(Q(RazonSocial__contains=datosBuscar),Q(TipoPersona=tipoPersona))
                
        datos = list()
        
        for persona in personas:
            #Se busca la direccion del socio por si alguno no tuviera se manda vacio
            direccionDatosPersona = Direccion.objects.filter(Persona = persona.IdPersona)
            DomicilioPersona = ''
            IdSepomexPersona = ''
            for direccionPersona in direccionDatosPersona:
                DomicilioPersona = direccionPersona.Calle
                IdSepomexPersona = direccionPersona.IdSepomex
                if direccionPersona.TipoDireccion == "2":
                    DomicilioPersona = direccionPersona.Calle
                    IdSepomexPersona = direccionPersona.IdSepomex
                    break

            #Se busca el telefono de la persona, por si no tuviera se manda en blanco
            telefonoDatosPersona = Telefono.objects.filter(IdPersona = persona.IdPersona)
            TelefonoPersona = ''
            for telefonoPersona in telefonoDatosPersona:
                TelefonoPersona = telefonoPersona.Numero
                if telefonoPersona.TipoTelefono == 'TRABAJO':
                    TelefonoPersona = telefonoPersona.Numero
                    break

            if IdSepomexPersona == '':
                CP =''
                Municipio = ''
                Estado = ''
            else:
                DireccionSepomex = Sepomex.objects.using('catalogos').filter(IdSepomex = IdSepomexPersona)[0]
                CP = DireccionSepomex.DCp
                Municipio = DireccionSepomex.DMnpio
                Estado = DireccionSepomex.DEstado
                
            datos.append({'IdPersona':persona.IdPersona,'Rfc':persona.Rfc,'PrimerNombre':persona.PrimerNombre,'SegundoNombre':persona.SegundoNombre,'RazonSocial':persona.RazonSocial,'ApellidoPaterno':persona.ApellidoPaterno,'ApellidoMaterno':persona.ApellidoMaterno,'Direccion':DomicilioPersona,'Telefono':TelefonoPersona,'CP':CP,'Municipio':Municipio,'Estado':Estado})
    
    except:
        return dajax.json()
    
    return simplejson.dumps({'personas':datos})