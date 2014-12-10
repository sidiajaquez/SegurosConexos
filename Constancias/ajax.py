#encoding:utf-8
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from Solicitud.models import RelacionAnexaActaVerificacion, Solicitud, Beneficiario
from ConexosAgropecuarios.models import Persona
from Programas.models import Programa,TipoSeguro,SubTipoSeguro
from Constancias.models import Constancia, ConstanciaCobertura
import datetime
from dajax.core import Dajax
from dajaxice.utils import deserialize_form

@dajaxice_register
def buscar_solicitudes(request): #Busca las solicitudes con relacion anexa al acta de verificacion significando que ya estan aprobadas para que se les pueda generar su constancia
    solicitudConRelacionAnexaActaVerificacion = RelacionAnexaActaVerificacion.objects.filter(FechaRelacionAnexaActaVerificacion__year = datetime.datetime.today().year).order_by("-IdRelacionAnexaActaVerificacion")
    datos = list()
    for relacionAnexaActaVerificacion in solicitudConRelacionAnexaActaVerificacion:
        solicitudObtenida = Solicitud.objects.filter(IdSolicitud = relacionAnexaActaVerificacion.Solicitud_id)[0]
        #Se verifica si la solicitud ya tiene constancia para adjuntar el boton de imprimir
        constanciaSolicitud = Constancia.objects.filter(Solicitud_id = solicitudObtenida.IdSolicitud)
        if constanciaSolicitud:
            imprimirConstancia = 1
            idConstancia = constanciaSolicitud[0].IdConstancia
        else:
            imprimirConstancia = 0
            idConstancia = ''
            
        persona = Persona.objects.filter(IdPersona = solicitudObtenida.PersonaAsegurada_id)[0]
       
        if persona.TipoPersona == 'F':
            nombre = persona.PrimerNombre + " " + persona.SegundoNombre + " " + persona.ApellidoPaterno + " " + persona.ApellidoMaterno
        else:
            nombre = persona.RazonSocial            
                    
        programa = Programa.objects.filter(IdPrograma = solicitudObtenida.Programa_id)[0]
        tipoSeguro = TipoSeguro.objects.using('catalogos').filter(IdTipoSeguro = programa.IdTipoSeguro)[0]    
        subTipoSeguro = SubTipoSeguro.objects.using('catalogos').filter(TipoSeguro_id = programa.IdTipoSeguro)[0] 
                    
        if programa.IdTipoMoneda == '1':
            descripcionMoneda = 'PESOS'
        else:
            descripcionMoneda = 'DOLARES'               
                    
        fecha = solicitudObtenida.FechaSolicitud.strftime("%d/%m/%Y")
        datos.append({'FolioSolicitud':solicitudObtenida.FolioSolicitud,'PersonaAsegurada':nombre,'FechaSolicitud':fecha, 'TipoSeguro': tipoSeguro.DescripcionTipoSeguro,
                      'SubTipoSeguro': subTipoSeguro.DescripcionSubTipoSeguro,'Moneda':descripcionMoneda,'IdSolicitud':solicitudObtenida.IdSolicitud,'Estatus':solicitudObtenida.Estatus,
                      'ImprimirConstancia':imprimirConstancia,'IdConstancia':idConstancia})          
    
    return simplejson.dumps({'solicitudes':datos})

@dajaxice_register
def guardar_constancia(request,frmConstancia,Coberturas,beneficiarioPorcentaje): #Recibe el formulario constancia, el porcentaje de los beneficiarios y las tarifas y cuotas de las coberturas
    dajax = Dajax()
    formulario_deserializado = deserialize_form(frmConstancia)
    fechaEmision = datetime.datetime.now()
    horaActual = datetime.datetime.strptime(fechaEmision.strftime('%H:%M:%S'),'%H:%M:%S').strftime('%H:%M:%S')
    folioConstancia = "C" + "-" + formulario_deserializado.get('varFolioSolicitud')

    arrayCoberturas_convertido_string = simplejson.dumps(Coberturas, separators=('|',','))
    list_Coberturas = arrayCoberturas_convertido_string.replace('[', '').replace(']', '').replace('"', '').split(';')

    arrayBeneficiariosPorcentaje_convertido_string = simplejson.dumps(beneficiarioPorcentaje, separators=('|',','))
    list_BeneficiariosPorcentaje = arrayBeneficiariosPorcentaje_convertido_string.replace('[', '').replace(']', '').replace('"', '').split(';')   
    
    constanciaGuardar = Constancia(Solicitud_id = formulario_deserializado.get('varIdSolicitud'), 
                                   VigenciaInicio = datetime.datetime.strptime(formulario_deserializado.get('VigenciaInicio')+' '+horaActual,'%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'),
                                   VigenciaFin = datetime.datetime.strptime(formulario_deserializado.get('VigenciaFinal')+' '+horaActual, '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'),
                                   FechaEmision = fechaEmision, FolioConstancia = folioConstancia, SumaAsegurada = formulario_deserializado.get('SumaAseguradaTotal'),
                                   CuotaNeta = formulario_deserializado.get('CuotaNeta'),Utilizado=0)
    constanciaGuardar.save()
    
    for cobertura in list_Coberturas:
        guardar_cobertura_constancia(cobertura,constanciaGuardar.IdConstancia)

    for porcentajeBeneficiario in list_BeneficiariosPorcentaje:
        actualizar_porcentaje_beneficiario(porcentajeBeneficiario)
    
    datosConstancia = [folioConstancia,constanciaGuardar.IdConstancia]
    dajax.add_data(datosConstancia, 'mensajeConstancia')
    return dajax.json()

def guardar_cobertura_constancia(cobertura,idConstancia): #guarda las coberturas con sus tarifas y cutoas para cada constancia
    listaCobertura = cobertura.split(',')
    guardarCobertura = ConstanciaCobertura(Constancia_id = idConstancia, IdCobertura = listaCobertura[0],Tarifa = listaCobertura[2],TarifaFondo = listaCobertura[3],
                                           TarifaReaseguro=listaCobertura[4],CuotaFondo=listaCobertura[5],CuotaReaseguro=listaCobertura[6])
    guardarCobertura.save()

def actualizar_porcentaje_beneficiario(porcentajeBeneficiario): #guarda el porcentaje para cada beneficiario una vez que se le haga la constancia
    listaPorcentajes = porcentajeBeneficiario.split(',')
    Beneficiario.objects.filter(IdBeneficiario = listaPorcentajes[0]).update(Porcentaje=listaPorcentajes[1])