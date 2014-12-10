#encoding:utf-8
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from Solicitud.models import Solicitud
from Constancias.models import Constancia
from Cotizador.models import Cotizador
from dajaxice.utils import deserialize_form
from Endoso.models import DeclaracionEndoso, DeclaracionEndosoPorDia, Endoso, SolicitudEndoso, DeclaracionTransporte, DeclaracionTransportePorUnidad, EndosoTransporte, DescripcionBienEndosoAD, ControlEndoso,\
    EndosoCancelacion
import datetime
from ConexosAgropecuarios.models import Persona, Telefono
from Programas.models import Programa
from Direcciones.models import Direccion
from django.db.models import Q
from decimal import *
from Solicitud.views import solicitudes
from Endoso.forms import SolicitudEndosoForm
from django.db import connections

@dajaxice_register
def buscar_constancias_endoso(request,tipoEndoso): #Funcion para traer todas las constancias para la generacion de su endoso
    if tipoEndoso: #Se buscan las constancias dependiendo del tipo de endoso enviado como parametro, se muestran aquellas constancias que cuenten con una solicitud de endoso en proceso y que cuenten con vigencia
        constanciasEndoso = Constancia.objects.filter(Estatus=1,VigenciaFin__gt=datetime.datetime.today(),solicitudendoso__TipoEndoso=tipoEndoso,solicitudendoso__Utilizado=True).order_by("-IdConstancia")
    else: #Si no se envia el tipo de endoso es porque se va a utilizar en el listado de la solicitud de endoso
        constanciasEndoso = Constancia.objects.filter(Estatus=1,VigenciaFin__gt=datetime.datetime.today()).order_by("-IdConstancia")
    
    datosConstancia = list()
    for constanciaEndoso in constanciasEndoso:    
        solicitudConstancia = Solicitud.objects.filter(IdSolicitud = constanciaEndoso.Solicitud_id)[0]
        persona = Persona.objects.filter(IdPersona = solicitudConstancia.PersonaAsegurada_id)[0]
        idControlEndoso = ''
        try:
            informacionSolicitudEndoso = SolicitudEndoso.objects.filter(Constancia_id = constanciaEndoso.IdConstancia).order_by("-IdSolicitudEndoso")[0]
            if informacionSolicitudEndoso:
                idSolicitudEndoso = [informacionSolicitudEndoso.IdSolicitudEndoso,informacionSolicitudEndoso.TipoEndoso,informacionSolicitudEndoso.ReimprimirSolicitudEndoso]
                #Se adjunta el id del ControlEndoso para habilitar la impresion del endoso
                try:
                    informacionControlEndoso = ControlEndoso.objects.get(SolicitudEndoso_id = informacionSolicitudEndoso.IdSolicitudEndoso)
                    if informacionControlEndoso:
                        idControlEndoso = informacionControlEndoso.IdControlEndoso
                except:
                    idControlEndoso = ''
        except:
            idSolicitudEndoso = ''
            
        if persona.TipoPersona == 'F':
            nombre = persona.PrimerNombre + " " + persona.SegundoNombre + " " + persona.ApellidoPaterno + " " + persona.ApellidoMaterno
        else:
            nombre = persona.RazonSocial
        programa = Programa.objects.filter(IdPrograma = solicitudConstancia.Programa_id)[0]
        if programa.IdTipoMoneda == '1':
            descripcionMoneda = 'PESOS'
        else:
            descripcionMoneda = 'DOLARES'        
        if solicitudConstancia.DeclaracionSolicitud == 'ANUAL':
            descripcionPago = 'Cuota Total'
        else:
            descripcionPago = 'Prima en Deposito'
        
        vigenciaConstancia = constanciaEndoso.VigenciaInicio.strftime("%d/%m/%Y") + " al " + constanciaEndoso.VigenciaFin.strftime("%d/%m/%Y")
        datosConstancia.append({'IdConstancia':constanciaEndoso.IdConstancia,'IdSolicitud':constanciaEndoso.Solicitud_id,'FolioConstancia':constanciaEndoso.FolioConstancia,
                                'PersonaAsegurada':nombre,'VigenciaConstancia':vigenciaConstancia,'Moneda':descripcionMoneda,'CuotaNeta':descripcionPago + ': $'+str('{:10,.4f}'.format(constanciaEndoso.CuotaNeta)),
                                'SumaAsegurada':str('{:10,.4f}'.format(constanciaEndoso.SumaAsegurada)),'Estatus':constanciaEndoso.Estatus,'SolicitudEndoso':idSolicitudEndoso,'TieneEndoso':constanciaEndoso.Utilizado,
                                'IdControlEndoso':idControlEndoso})

    return simplejson.dumps({'constancias':datosConstancia})

@dajaxice_register
def obtener_constancias(request, datosABuscar):# Método que obtiene las constancias de la base de datos.
    dajax = Dajax()
    try:
        
        cursor = connections['siobicx'].cursor()
        sql_string = "SELECT * FROM vconstanciadeclaracion WHERE FolioConstancia like '%" + datosABuscar + "%'" 
        cursor.execute(sql_string)
        result = cursor.fetchall()
                    
    except:
        return dajax.json()
    
    return simplejson.dumps({'constancias':result})

@dajaxice_register
def obtener_constancias_endoso_cancelacion(request):# Método que obtiene las constancias con solicitud de endosos para cancelación.
    dajax = Dajax()
    try:
                
        cursor = connections['siobicx'].cursor()
        sql_string = "SELECT * FROM vconstanciascancelacion"
        cursor.execute(sql_string)
        result = cursor.fetchall()
                    
    except:
        return dajax.json()
    
    return simplejson.dumps({'constancias':result})

@dajaxice_register
def guardar_declaracion_endoso(request, formulario, endosoPorDia, fechaPeriodoInicio, fechaPeriodoFin):# Método que recibe el formulario de endoso obtenido de endoso.html y lo deserializa para obtener la información de sus controles y lo valida con EndosoForm, si la información es valida guarda los datos y limpia los controles del formulario mediante una función de js.
    dajax = Dajax()
    
    if endosoPorDia == '':
        list_endoso = ''
    else:
        array_convertido_string = simplejson.dumps(endosoPorDia, separators=('|',','))
        list_endoso = array_convertido_string.replace('[', '').replace(']', '').replace('"', '').split(';')   
                      
    formulario_deserializado = deserialize_form(formulario)
     
    if formulario_deserializado.get('varIdEndoso') == '':
        
        fechaEndoso = datetime.datetime.now()
        endosoAGuardar = DeclaracionEndoso(FechaEndoso = fechaEndoso, ExistenciaInicial = formulario_deserializado.get('txtExistenciaInicial'),
                                TarifaMensual = formulario_deserializado.get('varTotalTarifa'), Constancia_id = formulario_deserializado.get('varIdConstancia'),
                                PeriodoInicio = datetime.datetime.strptime(fechaPeriodoInicio,'%d/%m/%Y').strftime('%Y-%m-%d'),
                                PeriodoFin = datetime.datetime.strptime(fechaPeriodoFin,'%d/%m/%Y').strftime('%Y-%m-%d'), CierreMes = 0,
                                Observaciones = formulario_deserializado.get('txtObservaciones').upper(), DeclaracionNueva = 0, IdStatusDeclaracion = 1)
        
        endosoAGuardar.save()
        
        Constancia.objects.filter(IdConstancia=formulario_deserializado.get('varIdConstancia')).update(UtilizadoDeclaracion=1)
        
        if str(formulario_deserializado.get('varIdDeclaracionEndosoAnterior')) != "":            
            DeclaracionEndoso.objects.filter(IdDeclaracionEndoso=formulario_deserializado.get('varIdDeclaracionEndosoAnterior')).update(DeclaracionNueva=1)   
        
        fechaInicio = datetime.datetime.strptime(fechaPeriodoInicio, "%d/%m/%Y")
        fechaFin = datetime.datetime.strptime(fechaPeriodoFin, "%d/%m/%Y")
        
        dias = (fechaFin - fechaInicio).days
        
        if len(list_endoso) == (dias + 1):
            DeclaracionEndoso.objects.filter(IdDeclaracionEndoso = endosoAGuardar.IdDeclaracionEndoso).update(CierreMes = 1)

        if list_endoso != '':
            for endoso in list_endoso:
                guardar_endoso_dia(endoso, endosoAGuardar.IdDeclaracionEndoso)     
                
        dajax.add_data(endosoAGuardar.IdDeclaracionEndoso, 'mensajeDeclaracionEndoso')
    
    else:
        actualizar_endoso(formulario_deserializado, list_endoso, fechaPeriodoInicio, fechaPeriodoFin) 
        
    return dajax.json()

@dajaxice_register
def guardar_declaracion_transporte(request, formulario, transportePorDia, fechaPeriodoInicio, fechaPeriodoFin):# Método que recibe el formulario de endoso obtenido de endoso.html y lo deserializa para obtener la información de sus controles y lo valida con EndosoForm, si la información es valida guarda los datos y limpia los controles del formulario mediante una función de js.
    dajax = Dajax()
        
    if transportePorDia == '':
        list_transporte = ''
    else:        
        array_convertido_string = simplejson.dumps(transportePorDia, separators=('|',','))
        list_transporte = array_convertido_string.replace('[', '').replace(']', '').replace('"', '').split(';')
                      
    formulario_deserializado = deserialize_form(formulario)
    
    if formulario_deserializado.get('varIdDeclaracionTransporte') == '':
                 
        fechaDeclaracionTransporte = datetime.datetime.now()
        declaracionTransporteGuardar = DeclaracionTransporte(Fecha = fechaDeclaracionTransporte, PeriodoInicio = datetime.datetime.strptime(fechaPeriodoInicio,'%d/%m/%Y').strftime('%Y-%m-%d'),
                                PeriodoFin = datetime.datetime.strptime(fechaPeriodoFin,'%d/%m/%Y').strftime('%Y-%m-%d'), 
                                DescripcionBienAsegurado = formulario_deserializado.get('txtDescripcionBienAsegurado').upper(), Observaciones = formulario_deserializado.get('txtObservaciones').upper(),
                                Constancia_id = formulario_deserializado.get('varIdConstancia'), CierreMes = 0, DeclaracionNueva = 0, IdStatusDeclaracion = 1)
        
        declaracionTransporteGuardar.save()   
        
        Constancia.objects.filter(IdConstancia=formulario_deserializado.get('varIdConstancia')).update(UtilizadoDeclaracion=1)
        
        if str(formulario_deserializado.get('varIdDeclaracionTransporteAnterior')) != "":            
            DeclaracionTransporte.objects.filter(IdDeclaracionTransporte=formulario_deserializado.get('varIdDeclaracionTransporteAnterior')).update(DeclaracionNueva=1)        
                    
        if list_transporte != '':
            guardar_declaracion_transporte_por_dia(list_transporte, declaracionTransporteGuardar.IdDeclaracionTransporte)     
                
        dajax.add_data(declaracionTransporteGuardar.IdDeclaracionTransporte, 'mensajeDeclaracionTransporte')
    
    else:
        actualizar_declaracion_transporte(formulario_deserializado, list_transporte, fechaPeriodoInicio, fechaPeriodoFin) 
         
    return dajax.json()

def actualizar_declaracion_transporte(formulario, list_transporte, fechaPeriodoInicio, fechaPeriodoFin): # Método que recibe el formulario y el listado de transporte por unidad.
    dajax = Dajax()
    
    DeclaracionTransporte.objects.filter(IdDeclaracionTransporte = formulario.get('varIdDeclaracionTransporte')).update(PeriodoInicio = datetime.datetime.strptime(fechaPeriodoInicio,'%d/%m/%Y').strftime('%Y-%m-%d'),
                                PeriodoFin = datetime.datetime.strptime(fechaPeriodoFin,'%d/%m/%Y').strftime('%Y-%m-%d'), 
                                DescripcionBienAsegurado = formulario.get('txtDescripcionBienAsegurado').upper(), Observaciones = formulario.get('txtObservaciones').upper(),
                                Constancia = formulario.get('varIdConstancia'))
    guardar_declaracion_transporte_por_dia(list_transporte, formulario.get('varIdDeclaracionTransporte'))
                
    return dajax.json()

@dajaxice_register
def actualizar_cierre_periodo_transporte(request, idDeclaracionTransporte): # Método que recibe el id de la declaración de transporte para actualizar el cierre del periodo. 
    dajax = Dajax()    
    DeclaracionTransporte.objects.filter(IdDeclaracionTransporte = idDeclaracionTransporte).update(CierreMes = 1)
                    
    return dajax.json()

@dajaxice_register
def cancelar_endoso(request, idConstancia, tieneEndoso, idSolicitudEndoso): #Cancela los endosos sin eliminarlos, solamente se actualiza el campo utilizado en la tabla de las constancias, solicitudendoso y descripcionbienendosoad
    dajax = Dajax()
    
    Constancia.objects.filter(IdConstancia = idConstancia).update(Utilizado = False)
    SolicitudEndoso.objects.filter(IdSolicitudEndoso = idSolicitudEndoso).update(Utilizado=False,ReimprimirSolicitudEndoso=False)
    
    #Si ya cuenta con endoso la constancia entonces se cancelan los bienes adjuntados a ese endoso
    if tieneEndoso:
        ControlEndoso.objects.filter(SolicitudEndoso_id = idSolicitudEndoso).update(Estatus = 2)
        DescripcionBienEndosoAD.objects.filter(SolicitudEndoso_id=idSolicitudEndoso).update(Utilizado=False)
    
    return dajax.json()

def guardar_declaracion_transporte_por_dia(list_transporte, idTransporte):# Metodo que recibe una entidad con la información de la declaración de transporte por dia para guardarla  a la base de datos.
    dajax = Dajax()
    
    endosoPorDiaGuardados = DeclaracionTransportePorUnidad.objects.filter(DeclaracionTransporte_id = idTransporte)

    for endosoPorDiaEliminar in endosoPorDiaGuardados:
        encontradoAEliminar = 1
        for endosoABuscar in list_transporte:
            list_endoso_por_dia = endosoABuscar.split(',')
            if str(list_endoso_por_dia[0]) == str(endosoPorDiaEliminar.IdDeclaracionTransportePorUnidad):
                encontradoAEliminar = 0
                break
            
        if encontradoAEliminar == 1:
            eliminar_transporte_por_dia(endosoPorDiaEliminar.IdDeclaracionTransportePorUnidad)
    
    for endoso in list_transporte:
        list_endoso_por_dia = endoso.split(',')
        if list_endoso_por_dia[0] == '':
            guardar_transporte_dia(endoso, idTransporte)
        else:
            actualizar_endoso_por_dia_db(list_endoso_por_dia)

    return dajax.json()

def actualizar_endoso_por_dia_db(bien): # Método que nos permite actualizar la informacion de un endoso de transporte declaración por dia.
    DeclaracionTransportePorUnidad.objects.filter(IdDeclaracionTransportePorUnidad = bien[0]).update(Romaneaje = bien[1], Fecha = datetime.datetime.strptime(bien[2],'%d/%m/%Y').strftime('%Y-%m-%d'), Cantidad = bien[3], SumaAseguradaUnitaria = bien[4], SumaAseguradaTotal = bien[5], Origen = bien[6], Destino = bien[7])

def guardar_transporte_dia(endosoTransporte, idTransporte): # Función que recibe una entidad con la información de la declaración de transporte por dia  y un id de transporte para almacenarlos en la base de datos.
    dajax = Dajax()
    list_endoso = endosoTransporte.split(',')
    endosoPorDia = DeclaracionTransportePorUnidad(DeclaracionTransporte_id = idTransporte, Romaneaje = list_endoso[1], Fecha = datetime.datetime.strptime(list_endoso[2],'%d/%m/%Y').strftime('%Y-%m-%d'), Cantidad = list_endoso[3], SumaAseguradaUnitaria = list_endoso[4], SumaAseguradaTotal = list_endoso[5], Origen = list_endoso[6], Destino = list_endoso[7])
    endosoPorDia.save()

    return dajax.json()

def eliminar_transporte_por_dia(idDeclaracionTransportePorDia): # Método que recibe el id de transporte por dia para eliminarlo de la base de datos. 
    dajax = Dajax()
    DeclaracionTransportePorUnidad.objects.filter(IdDeclaracionTransportePorUnidad = idDeclaracionTransportePorDia).delete()
    
    return dajax.json()

@dajaxice_register
def guardar_endoso(request, formulario, endoso):# Método que recibe el formulario de endoso obtenido de endosodeclaracion.html y lo deserializa para obtener la información de sus controles y lo valida con EndosoForm, si la información es valida guarda los datos y limpia los controles del formulario mediante una función de js.
    dajax = Dajax()
    
    if endoso == '':
        list_endoso = ''
    else:        
        array_convertido_string = simplejson.dumps(endoso, separators=('|',','))
        list_endoso = array_convertido_string.replace('[', '').replace(']', '').replace('"', '').split(';')
                      
    formulario_deserializado = deserialize_form(formulario)
    
    if list_endoso != '':
        
        endoso = list_endoso[0].split(',')
        endosoAGuardar = Endoso(BienesAsegurados = Decimal(endoso[0]), SumaAsegurada = Decimal(endoso[1]),
                                PorcentajeFondo = Decimal(endoso[2]), ImporteFondo = Decimal(endoso[3]),
                                PorcentajeReaseguro = Decimal(endoso[4]), ImporteReaseguro = Decimal(endoso[5]),
                                PorcentajeTotal = Decimal(endoso[6]), ImporteTotal = Decimal(endoso[7]), 
                                DeclaracionEndoso_id = formulario_deserializado.get('varIdDeclaracionEndoso'))
    
        endosoAGuardar.save()
        
        dajax.add_data(endosoAGuardar.IdEndoso, 'mensajeEndoso')
         
    return dajax.json()

def actualizar_endoso(formularioEndoso, endososPorDia, fechaPeriodoInicio, fechaPeriodoFin): # Método que permite actualizar los datos del endoso.
    dajax = Dajax()
    
    DeclaracionEndoso.objects.filter(IdDeclaracionEndoso = formularioEndoso.get('varIdEndoso')).update(ExistenciaInicial = formularioEndoso.get('txtExistenciaInicial'),
                                     TarifaMensual = formularioEndoso.get('varTotalTarifa'), Constancia = formularioEndoso.get('varIdConstancia'), Observaciones = formularioEndoso.get('txtObservaciones').upper())
    
    fechaInicio = datetime.datetime.strptime(fechaPeriodoInicio, "%d/%m/%Y")
    fechaFin = datetime.datetime.strptime(fechaPeriodoFin, "%d/%m/%Y")
    
    dias = (fechaFin - fechaInicio).days
    
    if len(endososPorDia) == (dias + 1):
        DeclaracionEndoso.objects.filter(IdDeclaracionEndoso = formularioEndoso.get('varIdEndoso')).update(CierreMes = 1)
    
    actualizar_endoso_por_dia(endososPorDia, formularioEndoso.get('varIdEndoso'))    
                
    return dajax.json()

def actualizar_endoso_por_dia(endososPorDia, idEndoso): # Método que permite actualizar los endosos por dia del endoso en la base de datos.
    dajax = Dajax()
    
    endosoPorDiaGuardados = DeclaracionEndosoPorDia.objects.filter(DeclaracionEndoso_id = idEndoso)
    
    for endosoPorDiaEliminar in endosoPorDiaGuardados:
        encontradoAEliminar = 1
        for endosoABuscar in endososPorDia:
            list_endoso_por_dia = endosoABuscar.split(',')
            
            if list_endoso_por_dia[0] == str(endosoPorDiaEliminar.IdDeclaracionEndosoPorDia):
                encontradoAEliminar = 0
                break
        if encontradoAEliminar == 1:
            eliminar_endoso_por_dia(endosoPorDiaEliminar.IdDeclaracionEndosoPorDia)
    
    for endoso in endososPorDia:
        list_endoso_por_dia = endoso.split(',')
        if list_endoso_por_dia[0] == '':
            guardar_endoso_dia(endoso, idEndoso)
        else:
            actualizar_tabla_endoso_por_dia(list_endoso_por_dia)
    
    return dajax.json()

def actualizar_tabla_endoso_por_dia(bien): # Método que nos permite actualizar la informacion de un endoso de declaracion por dia.
    DeclaracionEndosoPorDia.objects.filter(IdDeclaracionEndosoPorDia = bien[0]).update(Dia = bien[1], Entrada = bien[2], Salida = bien[3], Precio = bien[4], Existencia = bien[5], Valor = bien[6], TarifaMensual = bien[7], TarifaDiaria = bien[8], Cuota = bien[9])


def eliminar_endoso_por_dia(idEndosoPorDia): # Método que recibe el id cotizador cobertura para eliminarlo de la base de datos. 
    dajax = Dajax()
    DeclaracionEndosoPorDia.objects.filter(IdDeclaracionEndosoPorDia = idEndosoPorDia).delete()
    
    return dajax.json()
    
@dajaxice_register
def obtener_declaraciones_endoso(req): # Método que obtiene de la base de datos los endosos.
    dajax = Dajax()
    
    try:
        #cursor = connection.cursor()        
        cursor = connections['siobicx'].cursor()
        sql_string = 'SELECT IdDeclaracionEndoso, IdConstancia, FolioConstancia, FolioSolicitud, NombreCompleto, Rfc, PeriodoInicio, CierreMes, DeclaracionNueva, EndosoCreado FROM vlistadodeclaracionendoso'
        cursor.execute(sql_string)
        declaraciones = cursor.fetchall()
        
    except:
        return dajax.json()
    
    return simplejson.dumps({'declaracionendoso':declaraciones})

@dajaxice_register 
def obtener_declaraciones_transporte(req): # Método que obtiene de la base de datos las declaraciones de transporte.
    dajax = Dajax()
    
    try:
        #cursor = connection.cursor()        
        cursor = connections['siobicx'].cursor()
        sql_string = 'SELECT IdDeclaracionTransporte, IdConstancia, FolioConstancia, FolioSolicitud, NombreCompleto, Rfc, PeriodoInicio, CierreMes, DeclaracionNueva, EndosoCreado FROM vlistadodeclaraciontransporte'
        cursor.execute(sql_string)
        declaraciones = cursor.fetchall()
        
    except:
        return dajax.json()
    
    return simplejson.dumps({'declaraciontransporte':declaraciones})

def guardar_endoso_dia(endoso, idEndoso): # Función que recibe una entidad con la información del endoso por dia  y un id de endoso para almacenarlos en la base de datos.
    dajax = Dajax()
    
    list_endoso = endoso.split(',')
    endosoPorDia = DeclaracionEndosoPorDia(DeclaracionEndoso_id = idEndoso, Dia = list_endoso[1], Entrada = list_endoso[2], Salida = list_endoso[3], Existencia = list_endoso[4], Precio = list_endoso[5], Valor = list_endoso[6], TarifaMensual = list_endoso[7], TarifaDiaria = list_endoso[8], Cuota = list_endoso[9])
    endosoPorDia.save()
        
    return dajax.json()

@dajaxice_register
def eliminar_declaracion_endoso(request, idDeclaracion): # Función que permite eliminar la declaración del endoso seleccionado de la base de datos.
    dajax = Dajax()
    DeclaracionEndoso.objects.filter(IdDeclaracionEndoso = idDeclaracion).delete()
    
    return dajax.json()

@dajaxice_register
def obtener_constancias_transporte(request, datosABuscar):  # Método que obtiene la información en la vista vconstanciastransporte de la base de datos.
    
    dajax = Dajax()
    try:  
        cursor = connections['siobicx'].cursor()
        sql_string = "SELECT * FROM vconstanciastransporte WHERE FolioConstancia like '%" + datosABuscar + "%'" 
        cursor.execute(sql_string)
        result = cursor.fetchall()
                    
    except:
        return dajax.json()
    
    return simplejson.dumps({'constancias':result})

@dajaxice_register
def guardar_solicitud_endoso(request,frmSolicitudEndoso): #Metodo que permite guardar la solicitud de endoso
    dajax = Dajax()
    formulario_deserializado = deserialize_form(frmSolicitudEndoso)
    
    folioSolicitudEndoso = ''
    if formulario_deserializado.get('TipoEndoso') == 'AUMENTO':
        folioSolicitudEndoso = 'SEA-'
    elif formulario_deserializado.get('TipoEndoso') == 'CANCELACIÓN':
        folioSolicitudEndoso = 'SEC-'
    elif formulario_deserializado.get('TipoEndoso') == 'DISMINUCIÓN':
        folioSolicitudEndoso = 'SED-'
    elif formulario_deserializado.get('TipoEndoso') == 'MODIFICACIÓN':  
        folioSolicitudEndoso = 'SEM-'
    
    datos = {'TipoEndoso':formulario_deserializado.get('TipoEndoso'),
             'FechaSolicitudEndoso':datetime.datetime.strptime(formulario_deserializado.get('FechaSolicitudEndoso'),'%d/%m/%Y').strftime('%Y-%m-%d'),
             'Observaciones':formulario_deserializado.get('Observaciones')}

    formulario = SolicitudEndosoForm(datos)
    
    if formulario.is_valid():
        # Se cambia el indicador de utilizado a su ultimo endoso
        SolicitudEndoso.objects.filter(Constancia_id = formulario_deserializado.get('varIdConstancia')).update(Utilizado=False)
        
        solicitudAGuardar = SolicitudEndoso(Constancia_id = formulario_deserializado.get('varIdConstancia'),TipoEndoso=formulario_deserializado.get('TipoEndoso'),
                                            FechaSolicitudEndoso=datetime.datetime.strptime(formulario_deserializado.get('FechaSolicitudEndoso'),'%d/%m/%Y').strftime('%Y-%m-%d'),
                                            Observaciones=formulario_deserializado.get('Observaciones').upper(),Utilizado=True)
        solicitudAGuardar.save()
        folioSolicitud = folioSolicitudEndoso + str(solicitudAGuardar.IdSolicitudEndoso)
        SolicitudEndoso.objects.filter(IdSolicitudEndoso = solicitudAGuardar.IdSolicitudEndoso).update(FolioSolicitudEndoso = folioSolicitud)
        informacionSolicitudEndoso = [folioSolicitud,solicitudAGuardar.IdSolicitudEndoso]
        dajax.add_data(informacionSolicitudEndoso, 'mensajeSolicitud')
    else:
        dajax.alert('No se pudo guardar la información')
    
    return dajax.json()

@dajaxice_register
def guardar_endoso_transporte(request, idDeclaracionTransporte, endoso):# Método que recibe el formulario de endoso transporte obtenido de endosotransporte.html y lo deserializa para obtener la información de sus controles y lo valida con EndosoForm, si la información es valida guarda los datos y limpia los controles del formulario mediante una función de js.
    dajax = Dajax()
    
    if endoso == '':
        list_endoso = ''
    else:
        array_convertido_string = simplejson.dumps(endoso, separators=('|',','))
        list_endoso = array_convertido_string.replace('[', '').replace(']', '').replace('"', '').split(';')
    
    if list_endoso != '':
        
        endoso = list_endoso[0].split(',')
        endosoAGuardar = EndosoTransporte(BienesAsegurados = Decimal(endoso[0]), SumaAsegurada = Decimal(endoso[1]),
                                PorcentajeFondo = Decimal(endoso[2]), ImporteFondo = Decimal(endoso[3]),
                                PorcentajeReaseguro = Decimal(endoso[4]), ImporteReaseguro = Decimal(endoso[5]),
                                PorcentajeTotal = Decimal(endoso[6]), ImporteTotal = Decimal(endoso[7]), 
                                DeclaracionTransporte_id = idDeclaracionTransporte)    
        endosoAGuardar.save()
        
        dajax.add_data(endosoAGuardar.IdEndosoTransporte, 'mensajeEndoso')
         
    return dajax.json()

@dajaxice_register
def guardar_endoso_ad(request,contenidos,datosEndoso):
    dajax = Dajax()
    #Guardar el endoso en la tabla ControlEndoso
    guardarControlEndoso = ControlEndoso(Constancia_id = datosEndoso["idConstancia"],FechaEndoso = datetime.datetime.now(),TipoEndoso = datosEndoso["TipoEndoso"],
                                         SumaAseguradaAnterior = datosEndoso["SumaAseguradaAnterior"],SumaAseguradaEndoso = datosEndoso["SumaAseguradaEndoso"],
                                         SumaAseguradaActual = datosEndoso["SumaAseguradaActual"],SolicitudEndoso_id= datosEndoso["idSolicitudEndoso"])
     
    guardarControlEndoso.save()
    #Se crea el Folio dependiendo del tipo
    folioEndoso = "E" + datosEndoso["TipoEndoso"][0] + "-" + str(guardarControlEndoso.IdControlEndoso)
    ControlEndoso.objects.filter(IdControlEndoso = guardarControlEndoso.IdControlEndoso).update(FolioEndoso = folioEndoso)
    informacionMensaje = [folioEndoso, guardarControlEndoso.IdControlEndoso]
    dajax.add_data(informacionMensaje, 'mensajeSolicitud')
    #Se pone ocupada la constancia para el endoso
    Constancia.objects.filter(IdConstancia = datosEndoso["idConstancia"]).update(Utilizado=True)
    array_convertido_string = simplejson.dumps(contenidos, separators=('|',','))
    list_Contenidos = array_convertido_string.replace('[', '').replace(']', '').replace('"', '').split(';')
    
    if list_Contenidos != '':
        #antes de guardar los nuevos bienes se berifica que los anteriores dejen de estar utilizados
        DescripcionBienEndosoAD.objects.filter(Constancia_id = datosEndoso["idConstancia"]).update(Utilizado=False)
        for contenidos in list_Contenidos:
            guardar_bienes_endoso_ad(contenidos, datosEndoso["idConstancia"],datosEndoso["idSolicitudEndoso"])
                
    return dajax.json()

def guardar_bienes_endoso_ad(contenidos,idConstancia,idSolicitudEndoso): #Metodo para guardar la descripcion de los bienes de la relacion anexa al acta de verificacion
    listaBienes = contenidos.split(',')
    guardarBien = DescripcionBienEndosoAD(Constancia_id = idConstancia, NombreEquipo = listaBienes[1], Marca = listaBienes[2],
                                                     Modelo = listaBienes[3], Serie = listaBienes[4], DocumentacionEvaluacion = codificarUTF8(listaBienes[5]), 
                                                     FechaBien = datetime.datetime.strptime(listaBienes[6],'%d/%m/%Y').strftime('%Y-%m-%d'), 
                                                     Cantidad = listaBienes[7], ValorUnitario = listaBienes[8],SolicitudEndoso_id=idSolicitudEndoso,Utilizado=True)
        
    guardarBien.save()
    
def codificarUTF8(strDato): #Metodo para cambiar los caracteres especiales que vienen de javascript y ponerlos con acentos
    Utf = strDato.replace("\u00d1","Ñ")
    Utf = Utf.replace("\u00c1", "Á")
    Utf = Utf.replace("\u00c9", "É")
    Utf = Utf.replace("\u00cd", "Í")
    Utf = Utf.replace("\u00d3", "Ó")
    Utf = Utf.replace("\u00da", "Ú")
    
    return Utf

@dajaxice_register
def obtener_declaracionendoso_por_dia(request, idDeclaracionEndoso):  # Método que obtiene las declaraciones por dia de la base de datos mediante el id de la declaración de endoso.
    
    dajax = Dajax()
    try:            
        
        declaracionesEndosoPorDia = DeclaracionEndosoPorDia.objects.filter(DeclaracionEndoso_id = idDeclaracionEndoso)      
        
        datos = list()
        
        for declaracion in declaracionesEndosoPorDia:   
            datos.append({'IdDeclaracionEndosoPorDia':declaracion.IdDeclaracionEndosoPorDia,'Dia':declaracion.Dia,'Entrada':str(declaracion.Entrada),'Salida':str(declaracion.Salida),'Precio':str(declaracion.Precio),'Existencia':str(declaracion.Existencia),'Valor':str(declaracion.Valor),'TarifaMensual':str(declaracion.TarifaMensual),'TarifaDiaria':str(declaracion.TarifaDiaria),'Cuota':str(declaracion.Cuota)})
   
                   
    except:
        return dajax.json()
    
    return simplejson.dumps({'declaracionesEndosoPorDia':datos})

@dajaxice_register
def obtener_declaraciontransporte_por_unidad(request, idDeclaracionTransporte):  # Método que obtiene las declaraciones de transporte por unidad de la base de datos mediante el id de la declaración de transporte.
    
    dajax = Dajax()

    try:                    
        declaracionesTransportePorUnidad = DeclaracionTransportePorUnidad.objects.filter(DeclaracionTransporte_id = idDeclaracionTransporte)      
        
        datos = list()
        
        for declaracion in declaracionesTransportePorUnidad:   
            datos.append({'IdDeclaracionTransportePorUnidad':declaracion.IdDeclaracionTransportePorUnidad,'Romaneaje':declaracion.Romaneaje,'Fecha':declaracion.Fecha.strftime('%d/%m/%Y'),'Cantidad':declaracion.Cantidad,'SumaAseguradaUnitaria':str(declaracion.SumaAseguradaUnitaria),'SumaAseguradaTotal':str(declaracion.SumaAseguradaTotal),'Origen':declaracion.Origen,'Destino':declaracion.Destino})
                       
    except:
        return dajax.json()
    
    return simplejson.dumps({'declaracionesTransportePorUnidad':datos})

@dajaxice_register
def obtener_constancia_idconstancia(req, idConstancia): # Método que obtiene la información de una constancia por medio del id de la constancia para el buscador del hitorial del endoso de declaración.
    dajax = Dajax()
    
    try:
        #cursor = connection.cursor()        
        cursor = connections['siobicx'].cursor()
        sql_string = "SELECT IdConstancia, FolioConstancia, FolioSolicitud, Moneda, Ejercicio, VigenciaInicio, VigenciaFin FROM vconstanciasconendoso Where FolioConstancia like '%%" + idConstancia.upper() + "%%'"
        cursor.execute(sql_string)
        constancias = cursor.fetchall()
        
    except:
        return dajax.json()
    
    return simplejson.dumps({'constancias':constancias})

@dajaxice_register
def obtener_constancia_idconstancia_transporte(req, idConstancia): # Método que obtiene la información de una constancia por medio del id de la constancia para el buscardor del historial del endoso de transporte.
    dajax = Dajax()
    
    try:        
        cursor = connections['siobicx'].cursor()
        sql_string = "SELECT IdConstancia, FolioConstancia, FolioSolicitud, Moneda, Ejercicio, VigenciaInicio, VigenciaFin FROM vconstanciahistorialtransporte Where FolioConstancia like '%%" + idConstancia.upper() + "%%'"
        cursor.execute(sql_string)
        constancias = cursor.fetchall()
        
    except:
        return dajax.json()
    
    return simplejson.dumps({'constancias':constancias})

@dajaxice_register
def obtener_declaraciones_endoso_idconstancia(req, idConstancia): # Metodo que obtiene las declaraciones de endoso de la base de datos en base al id de la constancia.
    dajax = Dajax()
    
    try:        
        cursor = connections['siobicx'].cursor()
        sql_string = 'SELECT IdDeclaracionEndoso, IdConstancia, FolioConstancia, FolioSolicitud, NombreCompleto, Rfc, PeriodoInicio, CierreMes, DeclaracionNueva, EndosoCreado FROM vlistadodeclaracionendoso Where IdConstancia = ' + idConstancia + ' Order by IdDeclaracionEndoso desc'
        cursor.execute(sql_string)
        declaraciones = cursor.fetchall()
        
    except:
        return dajax.json()
    
    return simplejson.dumps({'declaracionendoso':declaraciones})

@dajaxice_register
def obtener_declaraciones_transporte_idconstancia(req, idConstancia): # Metodo que obtiene las declaraciones de transporte de la base de datos en base al id de la constancia.
    dajax = Dajax()
    
    try:
        cursor = connections['siobicx'].cursor()
        sql_string = 'SELECT IdDeclaracionTransporte, IdConstancia, FolioConstancia, FolioSolicitud, NombreCompleto, Rfc, PeriodoInicio, CierreMes, DeclaracionNueva, EndosoCreado FROM vlistadodeclaraciontransporte Where IdConstancia = ' + idConstancia + ' Order by IdDeclaracionTransporte desc'
        cursor.execute(sql_string)
        declaraciones = cursor.fetchall()
        
    except:
        return dajax.json()
    
    return simplejson.dumps({'declaraciontransporte':declaraciones})

@dajaxice_register
def guardar_endoso_cancelacion(request, idConstancia, idSolicitudEndoso, monto, tipoEndoso):# Metodo que nos permite guardar el endoso de cancelacion de una constancia, el cual recibe el id de la constancia, solicitud de endoso, el monto a pagar y el tipo de endoso.
    dajax = Dajax()
    
    sumaMonto = monto.replace(",", "")
    
    endosoCancelacion = EndosoCancelacion(Constancia_id = idConstancia, SolicitudEndoso_id = idSolicitudEndoso, Monto = Decimal(sumaMonto), FechaCancelacion = datetime.datetime.now(), TipoEndoso = tipoEndoso)
    endosoCancelacion.save()
    
    folioEndosoCancelacion = 'EC' + '-' + str(endosoCancelacion.IdEndosoCancelacion)
    EndosoCancelacion.objects.filter(IdEndosoCancelacion = endosoCancelacion.IdEndosoCancelacion).update(FolioEndosoCancelacion = folioEndosoCancelacion)
    Constancia.objects.filter(IdConstancia = idConstancia).update(Estatus = 2)
    dajax.add_data(endosoCancelacion.IdEndosoCancelacion, 'mensajeEndosoGuardar')
         
    return dajax.json()
