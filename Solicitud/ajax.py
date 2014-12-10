#encoding:utf-8
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from Solicitud.forms import SolicitudForm, RelacionAnexaSolicitudForm, ActaVerificacionSolicitudForm
from dajaxice.utils import deserialize_form
from dajax.core import Dajax
from Solicitud.models import Solicitud, Beneficiario, RelacionAnexaSolicitud, DescripcionDetalladaBienSolicitado, ActaVerificacionSolicitud, MedidaSeguridadActaVerificacion, RelacionAnexaActaVerificacion, DescripcionBienActaVerificacion
import datetime
from ConexosAgropecuarios.models import Persona, Telefono, ContratoFondo, Moneda
from Direcciones.models import Direccion, Sepomex
from Programas.models import Programa, TipoSeguro, SubTipoSeguro

@dajaxice_register
def guardar_solicitud(request, frmSolicitudAseguramiento, beneficiariosSolicitud):# Método que recibe el formulario de solicitud para obtener la información de sus controles y guardarlo en la base de datos.
    dajax = Dajax()

    if beneficiariosSolicitud == '':
        list_Beneficiarios = ''
    else:        
        array_convertido_string = simplejson.dumps(beneficiariosSolicitud, separators=('|',','))
        list_Beneficiarios = array_convertido_string.replace('[', '').replace(']', '').replace('"', '').split(';') 

    
    formulario_deserializado = deserialize_form(frmSolicitudAseguramiento)
              
    datos = {'DeclaracionSolicitud':formulario_deserializado.get('DeclaracionSolicitud'),'FolioSolicitud':"SA",
             'FechaSolicitud':datetime.datetime.strptime(formulario_deserializado.get('FechaSolicitud'),'%d/%m/%Y').strftime('%Y-%m-%d'),
             'Unidades':formulario_deserializado.get('Unidades'), 'ValorUnidad':formulario_deserializado.get('ValorUnidad'),
             'Observaciones':formulario_deserializado.get('Observaciones')
             }
    
    formulario = SolicitudForm(datos)
        
    if formulario.is_valid():
        if formulario_deserializado.get('varIdSolicitud') == '':
            solicitudAGuardar = Solicitud(FechaSolicitud = datetime.datetime.strptime(formulario_deserializado.get('FechaSolicitud'),'%d/%m/%Y').strftime('%Y-%m-%d'),
                                          PersonaSolicitante_id = formulario_deserializado.get('varIdPersonaSolicitante'), PersonaAsegurada_id = formulario_deserializado.get('varIdPersonaAsegurada'),
                                          PersonaContratante_id = formulario_deserializado.get('varIdPersonaContratante'),
                                          Programa_id = formulario_deserializado.get('varIdTipoPrograma'), Unidades = formulario_deserializado.get('Unidades'),
                                          ValorUnidad = formulario_deserializado.get('ValorUnidad'), DeclaracionSolicitud = formulario_deserializado.get('DeclaracionSolicitud'),
                                          Observaciones = formulario_deserializado.get('Observaciones').upper()
                                          )
            solicitudAGuardar.save()
            
            folioSolicitud = "SA" + formulario_deserializado.get('txtFolioPrograma') + "-" + str(solicitudAGuardar.IdSolicitud)
            
            Solicitud.objects.filter(IdSolicitud = solicitudAGuardar.IdSolicitud).update(FolioSolicitud = folioSolicitud)
            
            if list_Beneficiarios != '':
                for beneficiario in list_Beneficiarios:
                    guardar_beneficiarios_Solicitud(beneficiario,solicitudAGuardar,"Save")
                                          
            dajax.add_data(folioSolicitud, 'mensajeSolicitud')
        else:
            actualizarSolicitud(formulario_deserializado, list_Beneficiarios)
 
    else:
        dajax.alert('Formulario invalido')   
         
    return dajax.json()

def guardar_beneficiarios_Solicitud(beneficiario,solicitudAGuardar,accion): #Metodo para guardar las personas beneficiarias de la solicitud
    dajax = Dajax()
    
    listaBeneficiarios = beneficiario.split(',')
    if accion=="Update":
        guardarBeneficiario = Beneficiario(Solicitud_id = solicitudAGuardar, PersonaBeneficiario_id = listaBeneficiarios[0])
    else:
        guardarBeneficiario = Beneficiario(Solicitud = solicitudAGuardar, PersonaBeneficiario_id = listaBeneficiarios[0])
        
    guardarBeneficiario.save()
    
    return dajax.json()    

def actualizarSolicitud(solicitudRecibida, list_Beneficiarios): # Método que actualiza la información de la solicitud de aseguramiento.
    dajax = Dajax()   
           
    Solicitud.objects.filter(IdSolicitud = solicitudRecibida.get('varIdSolicitud')).update(
                                    FechaSolicitud = datetime.datetime.strptime(solicitudRecibida.get('FechaSolicitud'),'%d/%m/%Y').strftime('%Y-%m-%d'),
                                    PersonaSolicitante = solicitudRecibida.get('varIdPersonaSolicitante'), PersonaAsegurada = solicitudRecibida.get('varIdPersonaAsegurada'),
                                    PersonaContratante = solicitudRecibida.get('varIdPersonaContratante'),
                                    Programa = solicitudRecibida.get('varIdTipoPrograma'), Unidades = solicitudRecibida.get('Unidades'),
                                    ValorUnidad = solicitudRecibida.get('ValorUnidad'), DeclaracionSolicitud = solicitudRecibida.get('DeclaracionSolicitud'),
                                    Observaciones = solicitudRecibida.get('Observaciones').upper())
    
    if list_Beneficiarios != '':
        for beneficiarios in list_Beneficiarios:      
            list_beneficiarioSolicitud = beneficiarios.split(',')
            if list_beneficiarioSolicitud[1] == '':  
                guardar_beneficiarios_Solicitud(beneficiarios, solicitudRecibida.get('varIdSolicitud'), "Update")
    
    return dajax.json()

@dajaxice_register
def eliminar_beneficiario(request, idBeneficiarioSolicitud): #Función que recibe el idBeneficiario con el cual se buscara el registro en la base de datos y se eliminara.
    dajax = Dajax()
    Beneficiario.objects.filter(IdBeneficiario = idBeneficiarioSolicitud).delete()
    
    return dajax.json()

@dajaxice_register
def buscar_solicitudes(request): # Método que obtiene todas las solicitudes con idstatussolicitud igual a 1 que representa el status en proceso.
    dajax = Dajax()
    
    try:
        solicitudesObtenidas = Solicitud.objects.filter(FechaSolicitud__year = datetime.datetime.today().year).order_by("-IdSolicitud")
        
        datos = list()
        for solicitud in solicitudesObtenidas:
            persona = Persona.objects.filter(IdPersona = solicitud.PersonaAsegurada_id)[0]
            
            if persona.TipoPersona == 'F':
                nombre = persona.PrimerNombre + " " + persona.SegundoNombre + " " + persona.ApellidoPaterno + " " + persona.ApellidoMaterno
            else:
                nombre = persona.RazonSocial            
            
            programa = Programa.objects.filter(IdPrograma = solicitud.Programa_id)[0]
            tipoSeguro = TipoSeguro.objects.using('catalogos').filter(IdTipoSeguro = programa.IdTipoSeguro)[0]    
            subTipoSeguro = SubTipoSeguro.objects.using('catalogos').filter(IdSubTipoSeguro = programa.IdSubTipoSeguro)[0] 
            descripcionMoneda = Moneda.objects.using('catalogos').filter(IdMoneda = programa.IdTipoMoneda)[0]         
            
            fecha = solicitud.FechaSolicitud.strftime("%d/%m/%Y")
            datos.append({'FolioSolicitud':solicitud.FolioSolicitud,'PersonaAsegurada':nombre,'FechaSolicitud':fecha, 'TipoSeguro': tipoSeguro.DescripcionTipoSeguro, 'SubTipoSeguro': subTipoSeguro.DescripcionSubTipoSeguro,
                          'Moneda':descripcionMoneda.Descripcion,'IdSolicitud':solicitud.IdSolicitud})
    
    except:
        return dajax.json()
    
    return simplejson.dumps({'solicitudes':datos})

@dajaxice_register
def buscar_solicitudConId(request, idSolicitud): # Método que busca la información de una solicitud pasando el id de la solicitud que se desea encontrar.
    dajax = Dajax()
    
    try:
        solicitudesObtenidas = Solicitud.objects.filter(IdSolicitud = idSolicitud)
        datos = list()
        for solicitud in solicitudesObtenidas:
            personaSolicitante = datosPersona(solicitud.PersonaSolicitante_id)
            personaAsegurada = datosPersona(solicitud.PersonaAsegurada_id)
            personaContratante = datosPersona(solicitud.PersonaContratante_id)
            
            programa = Programa.objects.filter(IdPrograma = solicitud.Programa_id)[0]
            tipoSeguro = TipoSeguro.objects.using('catalogos').filter(IdTipoSeguro = programa.IdTipoSeguro)[0]    
            subTipoSeguro = SubTipoSeguro.objects.using('catalogos').filter(IdSubTipoSeguro = programa.IdSubTipoSeguro)[0]
            contrato = ContratoFondo.objects.filter(IdContratoFondo = programa.IdContratoFondo)[0] 
            descripcionMoneda = Moneda.objects.using('catalogos').filter(IdMoneda = programa.IdTipoMoneda)[0]
                        
            fecha = solicitud.FechaSolicitud.strftime("%d/%m/%Y")
            relacionAnexaSolicitud = RelacionAnexaSolicitud.objects.filter(Solicitud_id = solicitud.IdSolicitud)
            if relacionAnexaSolicitud: 
                tieneRelacionAnexaSolicitud = True
            else:
                tieneRelacionAnexaSolicitud = False
                
            valorUnitario = '{:10,.2f}'.format(solicitud.ValorUnidad)
            sumaAseguradaSolicitada = '{:10,.2f}'.format(solicitud.Unidades * solicitud.ValorUnidad)
            datos.append({'IdSolicitud':solicitud.IdSolicitud, 'FolioSolicitud': solicitud.FolioSolicitud,'DeclaracionSolicitud':solicitud.DeclaracionSolicitud,'FechaSolicitud':fecha,'NombreSolicitante':personaSolicitante[0]['NombrePersona'],
                          'RfcSolicitante':personaSolicitante[0]['RfcPersona'], 'NombreContratante':personaContratante[0]['NombrePersona'], 'RfcContratante': personaContratante[0]['RfcPersona'],
                          'Observaciones':solicitud.Observaciones, 'Unidades':'{:,}'.format(solicitud.Unidades), 'ValorUnidad':valorUnitario,'SumaAseguradaSolicitada': sumaAseguradaSolicitada,'DomicilioPersonaSolicitante':personaSolicitante[0]['DireccionPersona'],
                          'CpSolicitante':personaSolicitante[0]['CPPersona'], 'MunicipioSolicitante':personaSolicitante[0]['MunicipioPersona'], 'EstadoSolicitante':personaSolicitante[0]['EstadoPersona'],
                          'TelefonoSolicitante': personaSolicitante[0]['TelefonoPersona'],'DomicilioPersonaContratante':personaContratante[0]['DireccionPersona'],'CpContratante':personaContratante[0]['CPPersona'],
                          'MunicipioContratante':personaContratante[0]['MunicipioPersona'], 'EstadoContratante':personaContratante[0]['EstadoPersona'],'TelefonoContratante':personaContratante[0]['TelefonoPersona'],
                          'IdPersonaAsegurada':solicitud.PersonaAsegurada_id,'NombreAsegurado':personaAsegurada[0]['NombrePersona'],'RfcAsegurado':personaAsegurada[0]['RfcPersona'],'DomicilioPersonaAsegurado':personaAsegurada[0]['DireccionPersona'],
                          'CpAsegurado':personaAsegurada[0]['CPPersona'],'MunicipioAsegurado':personaAsegurada[0]['MunicipioPersona'], 'EstadoAsegurado':personaAsegurada[0]['EstadoPersona'],'TelefonoAsegurado':personaAsegurada[0]['TelefonoPersona'],
                          'TipoSeguro': tipoSeguro.DescripcionTipoSeguro, 'SubTipoSeguro': subTipoSeguro.DescripcionSubTipoSeguro,'Moneda':descripcionMoneda.Descripcion,'Ejercicio':programa.Ejercicio,
                          'NumeroContrato':contrato.NumeroContrato,'FolioPrograma':programa.FolioPrograma, 'IdPersonaSolicitante':solicitud.PersonaSolicitante_id, 'IdPersonaContratante': solicitud.PersonaContratante_id,
                          'IdTipoPrograma':solicitud.Programa_id,'TieneRelacionAnexaSolicitud':tieneRelacionAnexaSolicitud})
    
    except:
        return dajax.json()
    
    return simplejson.dumps({'solicitudEncontrada':datos})


@dajaxice_register
def buscar_solicitudes_relacion_anexa(request,opcion):
    dajax = Dajax()
    
    try:
        solicitudConRelacionAnexa = RelacionAnexaSolicitud.objects.filter(FechaRelacionAnexa__year = datetime.datetime.today().year).order_by("-IdRelacionAnexaSolicitud")
        
        datos = list()
        
        for relacionAnexa in solicitudConRelacionAnexa:       
            solicitudObtenida = Solicitud.objects.filter(IdSolicitud = relacionAnexa.Solicitud_id)[0]

            persona = Persona.objects.filter(IdPersona = solicitudObtenida.PersonaAsegurada_id)[0]
                        
            if persona.TipoPersona == 'F':
                nombre = persona.PrimerNombre + " " + persona.SegundoNombre + " " + persona.ApellidoPaterno + " " + persona.ApellidoMaterno
            else:
                nombre = persona.RazonSocial            
                
            programa = Programa.objects.filter(IdPrograma = solicitudObtenida.Programa_id)[0]
            tipoSeguro = TipoSeguro.objects.using('catalogos').filter(IdTipoSeguro = programa.IdTipoSeguro)[0]    
            subTipoSeguro = SubTipoSeguro.objects.using('catalogos').filter(IdSubTipoSeguro = programa.IdSubTipoSeguro)[0] 
            descripcionMoneda = Moneda.objects.using('catalogos').filter(IdMoneda = programa.IdTipoMoneda)[0]           
                
            fecha = solicitudObtenida.FechaSolicitud.strftime("%d/%m/%Y")
            
            if opcion == 1: #la opcion uno requiere solicitudes con relacion anexa sin dictaminar y aprobadas para generarsu relacion anexa
                if solicitudObtenida.Estatus == None or solicitudObtenida.Estatus: #Se trae aquellas solicitudes con relacion anexa sin dictaminar y aprobadas para generar su relacion anexa
                    datos.append({'FolioSolicitud':solicitudObtenida.FolioSolicitud,'PersonaAsegurada':nombre,'FechaSolicitud':fecha, 'TipoSeguro': tipoSeguro.DescripcionTipoSeguro, 
                                  'SubTipoSeguro': subTipoSeguro.DescripcionSubTipoSeguro,'Moneda':descripcionMoneda.Descripcion,'IdSolicitud':solicitudObtenida.IdSolicitud,'Estatus':solicitudObtenida.Estatus})
            if opcion == 2:
                if solicitudObtenida.Estatus == False: #Se trae aquellas solicitudes rechazadas
                    datos.append({'FolioSolicitud':solicitudObtenida.FolioSolicitud,'PersonaAsegurada':nombre,'FechaSolicitud':fecha, 'TipoSeguro': tipoSeguro.DescripcionTipoSeguro, 
                                  'SubTipoSeguro': subTipoSeguro.DescripcionSubTipoSeguro,'Moneda':descripcionMoneda.Descripcion,'IdSolicitud':solicitudObtenida.IdSolicitud,'Estatus':solicitudObtenida.Estatus})              
    
    except:
        return dajax.json()
    
    return simplejson.dumps({'solicitudes':datos})

@dajaxice_register
def buscar_beneficiarios_solicitud (request, idSolicitud): # Método que busca los beneficiarios de una solicitud pasando el id de la solicitud que se desea encontrar
    dajax = Dajax()

    try:
        beneficiariosSolicitud = Beneficiario.objects.filter(Solicitud_id = idSolicitud)
        datos = list()
        relacionAnexaSolicitud = RelacionAnexaSolicitud.objects.filter(Solicitud_id = idSolicitud)
        if relacionAnexaSolicitud: 
            tieneRelacionAnexaSolicitud = True
        else:
            tieneRelacionAnexaSolicitud = False
        for beneficiario in beneficiariosSolicitud:
            datosBeneficiario = datosPersona(beneficiario.PersonaBeneficiario_id)
            datos.append({'IdBeneficiario':beneficiario.IdBeneficiario,'IdPersonaBeneficiario':beneficiario.PersonaBeneficiario_id,'NombrePersonaBeneficiario':datosBeneficiario[0]['NombrePersona'],
                          'DomicilioPersonaBeneficiario':datosBeneficiario[0]['DireccionPersona'],'RfcPersonaBeneficiario':datosBeneficiario[0]['RfcPersona'],
                          'TieneRelacionAnexaSolicitud':tieneRelacionAnexaSolicitud})

    except:
        return dajax.json()

    return simplejson.dumps({'beneficiariosSolicitud':datos})


def datosPersona(id_Persona): #Por medio del idPersona se regresa la direccion, telefono y datos de la persona
    personaList = list()
    datosPersona = Persona.objects.filter(IdPersona = id_Persona)[0]
    
    if datosPersona.TipoPersona == 'F':
        nombreCompleto = datosPersona.PrimerNombre + " " + datosPersona.SegundoNombre + " " + datosPersona.ApellidoPaterno + " " + datosPersona.ApellidoMaterno
    else:
        nombreCompleto = datosPersona.RazonSocial
        
    #Se busca la direccion del socio por si alguno no tuviera se manda vacio
    direccionPersona = Direccion.objects.filter(Persona_id = id_Persona)
    DomicilioPersona = ''
    IdSepomexPersona = ''
    for direccion in direccionPersona:
        DomicilioPersona = direccion.Calle
        IdSepomexPersona = direccion.IdSepomex
        if direccion.TipoDireccion == "2":
            DomicilioPersona = direccion.Calle
            IdSepomexPersona = direccion.IdSepomex
            break
              
    if IdSepomexPersona == '':
        CPPersona =''
        MunicipioPersona = ''
        EstadoPersona = ''
        AsentamientoPersona = ''
    else:
        DireccionSepomexPersona = Sepomex.objects.using('catalogos').filter(IdSepomex = IdSepomexPersona)[0]
        CPPersona = DireccionSepomexPersona.DCp
        MunicipioPersona = DireccionSepomexPersona.DMnpio
        EstadoPersona = DireccionSepomexPersona.DEstado
        AsentamientoPersona = DireccionSepomexPersona.DAsenta
    
    #Se busca el telefono de la persona, por si no tuviera se manda en blaco
    telefonoDatosPersona = Telefono.objects.filter(IdPersona = id_Persona)
    TelefonoPersona = ''
    for telefono in telefonoDatosPersona:
        TelefonoPersona = telefono.Numero
        if telefono.TipoTelefono == 'TRABAJO':
            TelefonoPersona = telefono.Numero
            break
    
    personaList.append({'NombrePersona':nombreCompleto, 'RfcPersona':datosPersona.Rfc, 'DireccionPersona': DomicilioPersona, 'CPPersona': CPPersona, 
                        'AsentamientoPersona':AsentamientoPersona,'MunicipioPersona': MunicipioPersona, 'EstadoPersona': EstadoPersona, 'TelefonoPersona': TelefonoPersona})
    return personaList
 
@dajaxice_register
def eliminar_solicitud(request, idSolicitud): # Método que nos permite cancelar la solicitud de aseguramiento, recibiendo el id de la solicitud y actualizando el campo idStatusSolicitud con un 3 que representa el status cancelada.
    dajax = Dajax()   
           
    Solicitud.objects.filter(IdSolicitud = idSolicitud).delete()
    
    return dajax.json()

@dajaxice_register
def guardar_relacion_anexa_acta_verificacion(request, frmRelacionAnexaActaVerificacion, contenidos): #Metodo para guardar la relacion anexa al acta de verificacion
    dajax = Dajax()

    array_convertido_string = simplejson.dumps(contenidos, separators=('|',','))
    list_Contenidos = array_convertido_string.replace('[', '').replace(']', '').replace('"', '').split(';')

    formulario_deserializado = deserialize_form(frmRelacionAnexaActaVerificacion)
    if formulario_deserializado.get('varIdRelacionAnexaActaVerificacion') == '':
        fechaRelacionAnexaActaVerificacion = datetime.datetime.now()
        guardarRelacionAnexaActaVerificacion = RelacionAnexaActaVerificacion(Solicitud_id = formulario_deserializado.get('varIdSolicitud'), UbicacionBienLat = formulario_deserializado.get('UbicacionBienLat'),
                                                                             UbicacionBienLng = formulario_deserializado.get('UbicacionBienLng'), CP = formulario_deserializado.get('CP'),
                                                                             DescripcionBienAsegurado = formulario_deserializado.get('DescripcionBienAsegurado').upper(),
                                                                             FechaRelacionAnexaActaVerificacion = fechaRelacionAnexaActaVerificacion)
        guardarRelacionAnexaActaVerificacion.save()

        if list_Contenidos != '':
            for contenidos in list_Contenidos:
                guardar_bienes_acta_verificacion(contenidos,guardarRelacionAnexaActaVerificacion.IdRelacionAnexaActaVerificacion)

        dajax.add_data(guardarRelacionAnexaActaVerificacion.IdRelacionAnexaActaVerificacion, 'mensajeRelAnexa')
        
    else:
        actualizarRelacionAnexaActaVerificacion(formulario_deserializado, list_Contenidos)
    
    return dajax.json()

def actualizarRelacionAnexaActaVerificacion(relacionAnexaActaVerificacion,listContenidos): #Metodo para actualizar la relacion anexa al acta de verificacion y sus contenidos
    dajax = Dajax()   
           
    RelacionAnexaActaVerificacion.objects.filter(IdRelacionAnexaActaVerificacion = relacionAnexaActaVerificacion.get('varIdRelacionAnexaActaVerificacion')).update(                                                                                                                                                    
                                    UbicacionBienLat = relacionAnexaActaVerificacion.get('UbicacionBienLat'),UbicacionBienLng = relacionAnexaActaVerificacion.get('UbicacionBienLng'), 
                                    CP = relacionAnexaActaVerificacion.get('CP'),DescripcionBienAsegurado = relacionAnexaActaVerificacion.get('DescripcionBienAsegurado').upper(),
                                    FechaRelacionAnexaActaVerificacion = datetime.datetime.now())
    
    if listContenidos != '':
        for contenidos in listContenidos:      
            list_DescripcionContenidos = contenidos.split(',')
            if list_DescripcionContenidos[0] == '':  
                guardar_bienes_acta_verificacion(contenidos, relacionAnexaActaVerificacion.get('varIdRelacionAnexaActaVerificacion'))
    
    return dajax.json() 

def guardar_bienes_acta_verificacion(contenidos,idRelacionAnexaActaVerificacion): #Metodo para guardar la descripcion de los bienes de la relacion anexa al acta de verificacion
    dajax = Dajax()
    
    listaBienes = contenidos.split(',')
    guardarBien = DescripcionBienActaVerificacion(RelacionAnexaActaVerificacion_id = idRelacionAnexaActaVerificacion, NombreEquipo = listaBienes[1], Marca = listaBienes[2],
                                                     Modelo = listaBienes[3], Serie = listaBienes[4], DocumentacionEvaluacion = codificarUTF8(listaBienes[5]), 
                                                     FechaBien = datetime.datetime.strptime(listaBienes[6],'%d/%m/%Y').strftime('%Y-%m-%d'), 
                                                     Cantidad = listaBienes[7], ValorUnitario = listaBienes[8])
        
    guardarBien.save()
    
    return dajax.json()


@dajaxice_register
def guardar_relacion_anexa(request, frmRelacionAnexa, contenidos): #Metodo para guardar la relacion anexa de la solicitud de aseguramiento
    dajax = Dajax()  

    array_convertido_string = simplejson.dumps(contenidos, separators=('|',','))
    list_Contenidos = array_convertido_string.replace('[', '').replace(']', '').replace('"', '').split(';')
    
    formulario_deserializado = deserialize_form(frmRelacionAnexa)
    datos = {'UbicacionBienLat': formulario_deserializado.get('UbicacionBienLat'),'UbicacionBienLng':formulario_deserializado.get('UbicacionBienLng'),'CP':formulario_deserializado.get('CP'),
             'DescripcionBienAsegurado':formulario_deserializado.get('DescripcionBienAsegurado'),'ObservacionesSolicitante':formulario_deserializado.get('ObservacionesSolicitante')             
             }

    formulario = RelacionAnexaSolicitudForm(datos)
        
    if formulario.is_valid():
        if formulario_deserializado.get('varIdRelacionAnexaSolicitud') == '':
            fechaRelacionAnexa = datetime.datetime.now()
            relacionAnexaGuardar = RelacionAnexaSolicitud(Solicitud_id = formulario_deserializado.get('varIdSolicitud'), UbicacionBienLat = formulario_deserializado.get('UbicacionBienLat'),
                                          UbicacionBienLng = formulario_deserializado.get('UbicacionBienLng'), DescripcionBienAsegurado = formulario_deserializado.get('DescripcionBienAsegurado').upper(),
                                          ObservacionesSolicitante = formulario_deserializado.get('ObservacionesSolicitante').upper(), CP = formulario_deserializado.get('CP'),
                                          FechaRelacionAnexa = fechaRelacionAnexa
                                          )
            relacionAnexaGuardar.save()
            
            if list_Contenidos != '':
                for contenidos in list_Contenidos:
                    guardar_bienes_solicitados(contenidos,relacionAnexaGuardar.IdRelacionAnexaSolicitud)
                    
            dajax.add_data(relacionAnexaGuardar.IdRelacionAnexaSolicitud, 'mensajeRelAnexa')
        else:
            actualizarRelacionAnexa(formulario_deserializado, list_Contenidos)
     
    return dajax.json()


def actualizarRelacionAnexa(relacionAnexa,listContenidos): #Metodo para actualizar la relacion anexa y sus contenidos
    dajax = Dajax()   
           
    RelacionAnexaSolicitud.objects.filter(IdRelacionAnexaSolicitud = relacionAnexa.get('varIdRelacionAnexaSolicitud')).update(
                                          UbicacionBienLat = relacionAnexa.get('UbicacionBienLat'),UbicacionBienLng = relacionAnexa.get('UbicacionBienLng'), 
                                          CP = relacionAnexa.get('CP'),DescripcionBienAsegurado = relacionAnexa.get('DescripcionBienAsegurado').upper(),
                                          ObservacionesSolicitante = relacionAnexa.get('ObservacionesSolicitante').upper(),
                                          FechaRelacionAnexa = datetime.datetime.now())
    
    if listContenidos != '':
        for contenidos in listContenidos:      
            list_DescripcionContenidos = contenidos.split(',')
            if list_DescripcionContenidos[0] == '':  
                guardar_bienes_solicitados(contenidos, relacionAnexa.get('varIdRelacionAnexaSolicitud'))
    
    return dajax.json()    
    

def guardar_bienes_solicitados(contenidos,idRelacionAnexa): #Metodo para guardar la descripcion de los bienes de la relacion anexa a la solicitud de aseguramiento
    dajax = Dajax()
    
    listaBienes = contenidos.split(',')
    guardarBien = DescripcionDetalladaBienSolicitado(RelacionAnexaSolicitud_id = idRelacionAnexa, NombreEquipo = listaBienes[1], Marca = listaBienes[2],
                                                     Modelo = listaBienes[3], Serie = listaBienes[4], DocumentacionEvaluacion = codificarUTF8(listaBienes[5]), 
                                                     FechaBien = datetime.datetime.strptime(listaBienes[6],'%d/%m/%Y').strftime('%Y-%m-%d'), 
                                                     Cantidad = listaBienes[7], ValorUnitario = listaBienes[8])
        
    guardarBien.save()
    
    return dajax.json()

@dajaxice_register
def eliminar_descripcion_bien(request, idDescripcionBien, opcion): #Función que recibe el idDescripcionBien con el cual se buscara el registro en la base de datos y se eliminara
    dajax = Dajax()
    if opcion == 1: #opcion uno borra los bienes de la relacion anexa a la solicitus, la opcion 2 borra los bienes de la relacion anexa al acta de verificacion
        DescripcionDetalladaBienSolicitado.objects.filter(IdDescripcionDetalladaBienSolicitado = idDescripcionBien).delete()
    else:
        DescripcionBienActaVerificacion.objects.filter(IdDescripcionBienActaVerificacion = idDescripcionBien).delete()
    
    return dajax.json()

@dajaxice_register
def eliminar_medida_seguridad(request, idMedidaSeguridad): #funcion que recibe el id de la medida de seguridad para posteriormente eliminarla de la tabla
    dajax = Dajax()
    
    MedidaSeguridadActaVerificacion.objects.filter(IdMedidaSeguridad = idMedidaSeguridad).delete()
    
    return dajax.json()

def codificarUTF8(strDato): #Metodo para cambiar los caracteres especiales que vienen de javascript y ponerlos con acentos
    Utf = strDato.replace("\u00d1","Ñ")
    Utf = Utf.replace("\u00c1", "Á")
    Utf = Utf.replace("\u00c9", "É")
    Utf = Utf.replace("\u00cd", "Í")
    Utf = Utf.replace("\u00d3", "Ó")
    Utf = Utf.replace("\u00da", "Ú")
    
    return Utf

@dajaxice_register
def guardar_acta_verificacion(request,dictamenInspeccion,medidaSeguridad,idSolicitud,idActaVerificacionSolicitud): #Funcion para guardar el dictamen del acta de verificacion
    dajax = Dajax()
    
    array_convertido_string = simplejson.dumps(medidaSeguridad, separators=('|',','))
    list_MedidasSeguridad = array_convertido_string.replace('[', '').replace(']', '').replace('"', '').split(';')
    
    datos = {'DictamenInspeccion': dictamenInspeccion}

    formulario = ActaVerificacionSolicitudForm(datos)
        
    if formulario.is_valid():
        if idActaVerificacionSolicitud == '':
            fechaActaVerificacionPrellenada = datetime.datetime.now()
            guardarActaVerificacion = ActaVerificacionSolicitud(Solicitud_id = idSolicitud, DictamenInspeccion = dictamenInspeccion.upper(),FechaPrellenada = fechaActaVerificacionPrellenada)
            
            guardarActaVerificacion.save()
            
            if list_MedidasSeguridad != '':
                for medidasSeguridad in list_MedidasSeguridad:
                    guardar_medidas_seguridad(medidasSeguridad,guardarActaVerificacion.IdActaVerificacionSolicitud)
            
            dajax.add_data(guardarActaVerificacion.IdActaVerificacionSolicitud, 'mensajeActaVerificacion')
        
        else:
            actualizarActaVerificacion(dictamenInspeccion,list_MedidasSeguridad,idActaVerificacionSolicitud)
            
    return dajax.json()

def actualizarActaVerificacion(dictamenInspeccion,listMedidasSeguridad,idActaVerificacionSolicitud): #Metodo para actualizar el acta de verificacion junto con las medidas de seguridad
    dajax = Dajax()   
           
    ActaVerificacionSolicitud.objects.filter(IdActaVerificacionSolicitud = idActaVerificacionSolicitud).update(
                                    DictamenInspeccion = dictamenInspeccion.upper(),
                                    FechaPrellenada = datetime.datetime.now())
    
    if listMedidasSeguridad != '':
        for medidaSeguridad in listMedidasSeguridad:      
            list_MedidasSeguridad = medidaSeguridad.split(',')
            if list_MedidasSeguridad[0] == '':  
                guardar_medidas_seguridad(medidaSeguridad, idActaVerificacionSolicitud)
    
    return dajax.json()


def guardar_medidas_seguridad(medidasSeguridad,idActaVerificacion): #Guarda las medidas de seguridad del acta de verificacion
    dajax = Dajax()
    
    listaMedidasSeguridad = medidasSeguridad.split(',')
    guardarMedidasSeguridad = MedidaSeguridadActaVerificacion(ActaVerificacionSolicitud_id = idActaVerificacion, MedidasSeguridad = listaMedidasSeguridad[1])
        
    guardarMedidasSeguridad.save()
    
    return dajax.json()

@dajaxice_register
def dictaminar_solicitud(request,idSolicitud,idActaVerificacionSolicitud,dictamen): #Modifica la solicitud para guardar la fecha del dictamen  y si fue positivo o negativo
    dajax = Dajax()
    
    Solicitud.objects.filter(IdSolicitud = idSolicitud).update(Estatus = dictamen)
    ActaVerificacionSolicitud.objects.filter(IdActaVerificacionSolicitud = idActaVerificacionSolicitud).update(FechaCampo = datetime.datetime.now())
       
    return dajax.json()