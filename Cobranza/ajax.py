#encoding:utf-8
#from django.db import connection
from django.utils import simplejson
from django.db.models import Q
from dajaxice.decorators import dajaxice_register
from Cobranza.models import PagoConstancia, PagoEndosoDeclaracion, PagoEndosoTransporte, PagoEndosoADC,PagoPrimaDeposito, PagoEndosoCancelacion, CobroEndosoCancelacion, EndosoRehabilitacion
from ConexosAgropecuarios.models import Persona
from Constancias.models import Constancia
from Endoso.models import SolicitudEndoso, DeclaracionEndoso, DeclaracionTransporte, ControlEndoso, DescripcionBienEndosoAD
from Programas.models import Programa
from Solicitud.models import Solicitud
from dajax.core import Dajax
import datetime
from decimal import *
from django.db import connections

@dajaxice_register
def buscar_constancias_canceladas(request): #Funcion para traer todas las constancias que esten sobre los 5 dias para su rehabilitacion pasados los 30 dias de gracia del pago
    constanciasCanceladas = Constancia.objects.filter(Q(Estatus = None) | Q(Estatus = 3)).order_by("-IdConstancia") #Se obtienen las constancias que no tienen pago
    datosConstanciasCanceladas = list()
    for constanciaCancelada in constanciasCanceladas:
        FechaLimitePagoPeriodoGracia = constanciaCancelada.VigenciaInicio + datetime.timedelta(days=30) #30 dias a partir de la vigencia inicial de la constancia
        FechaLimitePagoRehabilitacion = FechaLimitePagoPeriodoGracia + datetime.timedelta(days=5) #5 dias despues del periodo de gracia
        if datetime.datetime.now() >  FechaLimitePagoPeriodoGracia and datetime.datetime.now()<= FechaLimitePagoRehabilitacion: #Si se encuentra dendro de los 5 dias de rehabilitacion
            solicitudConstancia = Solicitud.objects.filter(IdSolicitud = constanciaCancelada.Solicitud_id)[0]
            persona = Persona.objects.filter(IdPersona = solicitudConstancia.PersonaAsegurada_id)[0]
            if solicitudConstancia.DeclaracionSolicitud == 'ANUAL':
                descripcionPago = 'Cuota Total'
            else:
                descripcionPago = 'Prima en Deposito'            
            if persona.TipoPersona == 'F':
                Nombre = persona.PrimerNombre + " " + persona.SegundoNombre + " " + persona.ApellidoPaterno + " " + persona.ApellidoMaterno
            else:
                Nombre = persona.RazonSocial
            programa = Programa.objects.filter(IdPrograma = solicitudConstancia.Programa_id)[0]
            if programa.IdTipoMoneda == '1':
                descripcionMoneda = 'PESOS'
            else:
                descripcionMoneda = 'DOLARES'
                
            vigenciaConstancia = constanciaCancelada.VigenciaInicio.strftime("%d/%m/%Y") + " al " + constanciaCancelada.VigenciaFin.strftime("%d/%m/%Y")
            datosConstanciasCanceladas.append({'IdConstancia':constanciaCancelada.IdConstancia,'IdSolicitud':constanciaCancelada.Solicitud_id,'FolioConstancia':constanciaCancelada.FolioConstancia,
                                    'PersonaAsegurada':Nombre,'VigenciaConstancia':vigenciaConstancia,'Moneda':descripcionMoneda,'CuotaNeta':descripcionPago + ': $'+str('{:10,.4f}'.format(constanciaCancelada.CuotaNeta)),
                                    'SumaAsegurada':str('{:10,.4f}'.format(constanciaCancelada.SumaAsegurada)),'Estatus':constanciaCancelada.Estatus})

        
    return simplejson.dumps({'ConstanciasCanceladas':datosConstanciasCanceladas})
    
@dajaxice_register
def buscar_constancias(request): #Funcion para traer todas las constancias no pagadas
    constanciasAPagar = Constancia.objects.filter(VigenciaFin__gt=datetime.datetime.today()).order_by("-IdConstancia")
    datosConstancia = list()
    for constanciaAPagar in constanciasAPagar:
        FechaLimitePagoPeriodoGracia = constanciaAPagar.VigenciaInicio + datetime.timedelta(days=30) #30 dias a partir de la vigencia inicial de la constancia
        
        #Obtiene Constancias no pagadas pero que esten dentro del periodo de gracia y las constancias ya pagadas
        if ((datetime.datetime.now() <= FechaLimitePagoPeriodoGracia and constanciaAPagar.Estatus == None) or (constanciaAPagar.Estatus == 1)):
            solicitudConstancia = Solicitud.objects.filter(IdSolicitud = constanciaAPagar.Solicitud_id)[0]
            persona = Persona.objects.filter(IdPersona = solicitudConstancia.PersonaAsegurada_id)[0]
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
            
            vigenciaConstancia = constanciaAPagar.VigenciaInicio.strftime("%d/%m/%Y") + " al " + constanciaAPagar.VigenciaFin.strftime("%d/%m/%Y")
            datosConstancia.append({'IdConstancia':constanciaAPagar.IdConstancia,'IdSolicitud':constanciaAPagar.Solicitud_id,'FolioConstancia':constanciaAPagar.FolioConstancia,
                                    'PersonaAsegurada':nombre,'VigenciaConstancia':vigenciaConstancia,'Moneda':descripcionMoneda,'CuotaNeta':descripcionPago + ': $'+str('{:10,.4f}'.format(constanciaAPagar.CuotaNeta)),
                                    'SumaAsegurada':str('{:10,.4f}'.format(constanciaAPagar.SumaAsegurada)),'Estatus':constanciaAPagar.Estatus})

    return simplejson.dumps({'constancias':datosConstancia})

@dajaxice_register
def guardar_pago_constancia(request, idConstancia, formaPago): #metodo para actualizar la constancia como pagada
    dajax = Dajax()
    #Se actualiza la constancia y se pone como pagada
    Constancia.objects.filter(IdConstancia = idConstancia).update(FechaPago = datetime.datetime.now(), Estatus = 1, FormaPago = formaPago)
    #Se guarda el pago en la tabla PagoConstancia
    FolioRecibo = 'R-'
    pagoConstancia = PagoConstancia(Constancia_id = idConstancia)
    pagoConstancia.save()
    #Se actualiza la tabla con el Folio segun el Id del pago
    folioReciboPago = PagoConstancia.objects.latest('IdPago') #Se obtiene el ultimo ID
    PagoConstancia.objects.filter(Constancia_id = idConstancia).update(FolioRecibo = FolioRecibo + str(folioReciboPago.IdPago))
    folioReciboPago = PagoConstancia.objects.latest('IdPago') #Despues de actualizado se obtiene el folio del recibo
    dajax.add_data(folioReciboPago.FolioRecibo, 'folioRecibo')
    return dajax.json()

@dajaxice_register
def obtener_declaraciones_endoso_traspaso(req): # Metodo que nos permite obtener las declaracones que no han sido pagadas
    dajax = Dajax()
    
    try:        
        cursor = connections['siobicx'].cursor()
        sql_string = 'SELECT IdDeclaracion, IdConstancia, FolioConstancia, FolioSolicitud, NombreCompleto, Rfc, PeriodoInicio, TipoEndoso, Importe FROM vlistapagoendosos'
        cursor.execute(sql_string)
        declaraciones = cursor.fetchall()
        
    except:
        return dajax.json()
    
    return simplejson.dumps({'declaraciones':declaraciones})

@dajaxice_register
def guardar_pago_declaracion(request, idDeclaracion, tipoEndoso, importeAPagar, formaPago): #Metodo que almacena el pago de los endosos.
    dajax = Dajax()
    
    importeTotalAPagar = str(importeAPagar).replace(',', '')
    
    if tipoEndoso == 'D':
        DeclaracionEndoso.objects.filter(IdDeclaracionEndoso = idDeclaracion).update(FechaPago = datetime.datetime.now().strftime("%Y-%m-%d"), IdStatusDeclaracion = 2, ImportePagado = float(importeTotalAPagar), FormaPago = formaPago)
        
        pagoEndosoDeclaracion = PagoEndosoDeclaracion(DeclaracionEndoso_id = idDeclaracion)
        pagoEndosoDeclaracion.save()
        idPago = pagoEndosoDeclaracion.IdPagoEndosoDeclaracion
        PagoEndosoDeclaracion.objects.filter(IdPagoEndosoDeclaracion = pagoEndosoDeclaracion.IdPagoEndosoDeclaracion).update(FolioRecibo = 'RD-'+ str(pagoEndosoDeclaracion.IdPagoEndosoDeclaracion))
    
    if tipoEndoso == 'T':
        DeclaracionTransporte.objects.filter(IdDeclaracionTransporte = idDeclaracion).update(FechaPago = datetime.datetime.now().strftime("%Y-%m-%d"), IdStatusDeclaracion = 2, ImportePagado = float(importeTotalAPagar), FormaPago = formaPago)
        
        pagoEndosoTransporte = PagoEndosoTransporte(DeclaracionTransporte_id = idDeclaracion)
        pagoEndosoTransporte.save()
        idPago = pagoEndosoTransporte.IdPagoEndosoTransporte
        PagoEndosoTransporte.objects.filter(IdPagoEndosoTransporte = pagoEndosoTransporte.IdPagoEndosoTransporte).update(FolioRecibo = 'RT-'+str(pagoEndosoTransporte.IdPagoEndosoTransporte))
    
    dajax.add_data(idPago, 'actualizarPagoEndoso')   
    
    return dajax.json()

@dajaxice_register
def obtener_control_endoso(request): #Funcion para traer todos los registros del control de endoso
    
    controlendosos = ControlEndoso.objects.filter(Estatus__isnull=True, TipoEndoso = 'AUMENTO')
    
    datosEndoso = list()
    for controlendoso in controlendosos:
        constancia = Constancia.objects.filter(IdConstancia = controlendoso.Constancia_id)[0]
        solicitud = Solicitud.objects.filter(IdSolicitud = constancia.Solicitud_id)[0]
        programa = Programa.objects.filter(IdPrograma = solicitud.Programa_id)[0]
        persona = Persona.objects.filter(IdPersona = solicitud.PersonaAsegurada_id)[0]
        
        if persona.TipoPersona == 'F':
            nombre = persona.PrimerNombre + " " + persona.SegundoNombre + " " + persona.ApellidoPaterno + " " + persona.ApellidoMaterno
        else:
            nombre = persona.RazonSocial
    
        moneda = "Pesos"
        
        solicitudEndoso = SolicitudEndoso.objects.filter(Constancia_id = constancia.IdConstancia).order_by("-IdSolicitudEndoso")[0]
        
        descripciones = DescripcionBienEndosoAD.objects.filter(SolicitudEndoso_id = solicitudEndoso.IdSolicitudEndoso)
        
        montoAPagar = controlendoso.SumaAseguradaEndoso - controlendoso.SumaAseguradaAnterior
                
        datosEndoso.append({'Constancia':constancia.FolioConstancia,'Nombre':nombre,'Moneda':moneda,
                                'FolioEndoso':controlendoso.FolioEndoso,'FechaEndoso':controlendoso.FechaEndoso.strftime("%d/%m/%Y"),
                                'FolioSolicitudEndoso': solicitudEndoso.FolioSolicitudEndoso, 'IdControlEndoso':controlendoso.IdControlEndoso, 'Rfc':persona.Rfc,
                                'MontoAPagar':' $'+str('{:10,.4f}'.format(montoAPagar))})

    return simplejson.dumps({'endosos':datosEndoso})

@dajaxice_register
def guardar_pago_endoso_aumento(request, idConstancia, idSolicitud, montoAPagar, sumaAseguradaAumento, formaPago): # Metodo que almacena en la base de datos el pago de endoso ADC y libera la constancia.
    dajax = Dajax()
    
    monto = montoAPagar.replace(",", "")
    sumaAsegurada = sumaAseguradaAumento.replace(",", "")
    
    fechaPagoEndoso = datetime.datetime.now()
    pagoEndosoADC = PagoEndosoADC(Constancia_id = idConstancia, SolicitudEndoso_id = idSolicitud, MontoAPagar = Decimal(monto), FechaPago = fechaPagoEndoso, TipoEndoso = 'AUMENTO', SumaAseguradaAumento = Decimal(sumaAsegurada), FormaPago = formaPago)
    pagoEndosoADC.save()
    
    Constancia.objects.filter(IdConstancia = idConstancia).update(Utilizado = False)
    SolicitudEndoso.objects.filter(IdSolicitudEndoso = idSolicitud).update(Utilizado=False,ReimprimirSolicitudEndoso=False)
    ControlEndoso.objects.filter(SolicitudEndoso_id = idSolicitud).update(Estatus = 1)    
    PagoEndosoADC.objects.filter(IdPagoEndosoADC = pagoEndosoADC.IdPagoEndosoADC).update(FolioRecibo = 'REA-'+str(pagoEndosoADC.IdPagoEndosoADC))
    
    dajax.add_data(pagoEndosoADC.IdPagoEndosoADC, 'actualizarIdPago')
    
    return dajax.json()

@dajaxice_register
def obtener_constancias_pago_depsito(req): # Metodo que nos permite obtener las constancias que se encuentran listas para realizar el pago de la prima en deposito.
    dajax = Dajax()
    
    try:        
        cursor = connections['siobicx'].cursor()
        sql_string = 'SELECT * FROM vconstanciasprimadeposito'
        cursor.execute(sql_string)
        datosConstancia = cursor.fetchall()
        
    except:
        return dajax.json()
    
    return simplejson.dumps({'constancias':datosConstancia})

@dajaxice_register
def guardar_prima_deposito(request, idConstancia, montoAPagar): # Metodo que nos permite guardar el pago de la prima en deposito de las contancias canc
    dajax = Dajax()
    
    monto = montoAPagar.replace(",", "")
    fechaPago = datetime.datetime.now()
    
    pagoPrimaDeposito = PagoPrimaDeposito(Constancia_id = idConstancia, Monto = Decimal(monto), FechaPago = fechaPago)
    pagoPrimaDeposito.save()
            
    PagoPrimaDeposito.objects.filter(IdPagoPrimaDeposito = pagoPrimaDeposito.IdPagoPrimaDeposito).update(FolioRecibo = 'RPD-'+str(pagoPrimaDeposito.IdPagoPrimaDeposito))
    
    dajax.add_data(pagoPrimaDeposito.IdPagoPrimaDeposito, 'actualizarPagoPrima')
    
    return dajax.json()

@dajaxice_register
def obtener_constancias_canceladas_anual(req): # Metodo que nos permite obtener las constancias anuales que contienen un endoso de cancelacion para realizar el pago de la cancelacion.
    dajax = Dajax()
    
    try:        
        cursor = connections['siobicx'].cursor()
        sql_string = 'SELECT * FROM vendososcancelacionanual'
        cursor.execute(sql_string)
        datosConstancia = cursor.fetchall()
        
    except:
        return dajax.json()
    
    return simplejson.dumps({'constancias':datosConstancia})

@dajaxice_register
def guardar_pago_endoso_cancelacion(request, idConstancia, montoAPagar): # Metodo que permite guardar el pago del endoso de cancelacion de constancias anuales.
    dajax = Dajax()
    
    monto = montoAPagar.replace(",", "")
    fechaPago = datetime.datetime.now()
    
    pagoEndosoCancelacion = PagoEndosoCancelacion(Constancia_id = idConstancia, Monto = Decimal(monto), FechaPago = fechaPago)
    pagoEndosoCancelacion.save()
            
    PagoEndosoCancelacion.objects.filter(IdPagoEndosoCancelacion = pagoEndosoCancelacion.IdPagoEndosoCancelacion).update(FolioRecibo = 'RPEC-'+str(pagoEndosoCancelacion.IdPagoEndosoCancelacion))
    
    dajax.add_data(pagoEndosoCancelacion.IdPagoEndosoCancelacion, 'actualizarPagoEndoso')
    
    return dajax.json()

@dajaxice_register
def obtener_constancias_canceladas_declaracion(req): # Metodo que nos permite obtener las constancias a declaracion que contienen un endoso de cancelacion para realizar el cobro de la cancelacion.
    dajax = Dajax()
    
    try:        
        cursor = connections['siobicx'].cursor()
        sql_string = 'SELECT * FROM vendososcancelacionadeclaracion'
        cursor.execute(sql_string)
        datosConstancia = cursor.fetchall()
        
    except:
        return dajax.json()
    
    return simplejson.dumps({'constancias':datosConstancia})

@dajaxice_register
def guardar_cobro_endoso_cancelacion(request, idConstancia, montoAPagar): # Metodo que permite guardar el cobro del endoso de cancelacion de constancias a declaracion.
    dajax = Dajax()
    
    monto = montoAPagar.replace(",", "")
    fechaCobro = datetime.datetime.now()
    
    cobroEndosoCancelacion = CobroEndosoCancelacion(Constancia_id = idConstancia, Monto = Decimal(monto), FechaCobro = fechaCobro)
    cobroEndosoCancelacion.save()
            
    CobroEndosoCancelacion.objects.filter(IdCobroEndosoCancelacion = cobroEndosoCancelacion.IdCobroEndosoCancelacion).update(FolioRecibo = 'RCEC-'+str(cobroEndosoCancelacion.IdCobroEndosoCancelacion))
    
    dajax.add_data(cobroEndosoCancelacion.IdCobroEndosoCancelacion, 'actualizarCobroEndoso')
    
    return dajax.json()

@dajaxice_register
def rehabilitar_constancia(request, idConstancia, idSolicitud): #Metodo que actualiza la tabla Constancias para poner en el estatus 3 a la constancia (Rehabilitado) y duarda registro nuevo en la tabla EndosoRehabilitacion
    dajax = Dajax()
    #Generacion del folio del endoso
    folioEndoso = 'ER-'
    #se guarda en la tabla EndosoRehabilitacion el endoso generado
    rehabilitacion = EndosoRehabilitacion(Constancia_id = idConstancia, Solicitud_id = idSolicitud, FolioEndoso = folioEndoso, FechaEndoso = datetime.datetime.now())
    rehabilitacion.save()
    EndosoRehabilitacion.objects.filter(Constancia_id = idConstancia).update(FolioEndoso = folioEndoso + str(rehabilitacion.IdEndosoRehabilitacion))
    #Actualizacion al estado 3 en la tabla Constancia
    Constancia.objects.filter(IdConstancia = idConstancia).update(Estatus = 3)
    #mandar el folio generado en una funcion para mostrarlo
    dajax.add_data(folioEndoso + str(rehabilitacion.IdEndosoRehabilitacion), 'mensajeFolioRehabilitacion')
    return dajax.json()
