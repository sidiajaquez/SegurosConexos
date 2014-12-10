from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from Cobranza.models import PagoEndosoDeclaracion, PagoEndosoTransporte, PagoConstancia, PagoEndosoADC, EndosoRehabilitacion, PagoPrimaDeposito, PagoEndosoCancelacion, CobroEndosoCancelacion
from Constancias.models import Constancia
from ConexosAgropecuarios.models import DatosFondo,Persona, ContratoFondo,ContratoReaseguro,Reaseguradora,PersonalApoyo,\
    Moneda
from Programas.models import Programa
from Solicitud.models import Solicitud, ActaVerificacionSolicitud, Beneficiario, RelacionAnexaActaVerificacion,\
    DescripcionBienActaVerificacion
from Solicitud import ajax
from Endoso.models import DeclaracionEndoso, DeclaracionTransporte, ControlEndoso, SolicitudEndoso, DescripcionBienEndosoAD,\
    Endoso, EndosoTransporte, EndosoCancelacion
from Programas.models import Cobertura, CoberturaPrograma
from Cotizador.models import CotizadorCobertura, Cotizador
from ConexosAgropecuarios.pdf import generar_pdf
from django.db import connections
import datetime

@login_required()
def listaRehabilitarConstanciasCanceladas(request): #Metodo para crear la lista de las constancias canceladas que esten dentro de los 5 dias posteriores a su cancelacion
    return render(request,'listarehabilitarconstanciascanceladas.html',{'usuario':request.user})

@login_required()
def listaCobroConstancias(request): #Funcion para generar el listado de las constancias pendientes de cobro
    return render(request,'listacobroconstancias.html',{'usuario':request.user})

class PagoConstanciaDetailView(DetailView): # Clase generica para la generacion del pago de constancia
    model = Constancia
    template_name = "recibopagoconstancia.html"
    context_object_name = "constancia"
        
    def get_context_data(self, **kwargs):
        objetoConstancia = self.get_object()
        context = super(PagoConstanciaDetailView,self).get_context_data(**kwargs)      
        listConstancia = list()
        informacionSolicitud = Solicitud.objects.filter(IdSolicitud = objetoConstancia.Solicitud_id)[0]
        informacionAsegurado = ajax.datosPersona(informacionSolicitud.PersonaAsegurada_id)
        informacionRelacionAnexaActaVerificacion = RelacionAnexaActaVerificacion.objects.filter(Solicitud_id = objetoConstancia.Solicitud_id)[0]
        listConstancia.append({'FolioSolicitud':informacionSolicitud.FolioSolicitud,'Asegurado':informacionAsegurado,'ConceptoDescripcion':informacionRelacionAnexaActaVerificacion.DescripcionBienAsegurado})
        folioRecibo = ''
        informacionPago = PagoConstancia.objects.filter(Constancia_id=objetoConstancia.IdConstancia)
        programa = Programa.objects.filter(IdPrograma = informacionSolicitud.Programa_id)[0]
        descripcionMoneda = Moneda.objects.using('catalogos').filter(IdMoneda = programa.IdTipoMoneda)[0]

        #Se verifica si la constancia va a ser un endoso de rehabilitacion
        FechaLimitePagoPeriodoGracia = objetoConstancia.VigenciaInicio + datetime.timedelta(days=30) #30 dias a partir de la vigencia inicial de la constancia
        FechaLimitePagoRehabilitacion = FechaLimitePagoPeriodoGracia + datetime.timedelta(days=5) #5 dias despues del periodo de gracia
        if datetime.datetime.now() >  FechaLimitePagoPeriodoGracia and datetime.datetime.now()<= FechaLimitePagoRehabilitacion and objetoConstancia.Estatus == None: #Si se encuentra dendro de los 5 dias de rehabilitacion y no tiene ningun Estatus
            rehabilitarConstancia = True
        else:
            rehabilitarConstancia = False
        if informacionPago:
            folioRecibo = informacionPago[0].FolioRecibo
        endosoRehabilitacion = EndosoRehabilitacion.objects.filter(Constancia = objetoConstancia.IdConstancia)
        if endosoRehabilitacion:
            context['Rehabilitada'] = True
        else:
            context['Rehabilitada'] = False
        context['Constancia'] = listConstancia
        context['FechaActual'] = datetime.datetime.now()
        context['FolioRecibo'] = folioRecibo
        context['Moneda'] = descripcionMoneda.Descripcion
        context['RehabilitarConstancia'] = rehabilitarConstancia
        context['usuario'] = self.request.user
        return context

pago_constancia_detail = login_required(PagoConstanciaDetailView.as_view())

@login_required()
def cartaConstancia(request, id_Constancia): # Vista para la generacion del pdf de la carta constancia
    informacionConstancia = get_object_or_404(Constancia, IdConstancia = id_Constancia)
    informacionSolicitud = Solicitud.objects.filter(IdSolicitud = informacionConstancia.Solicitud_id)[0]
    informacionAsegurado = ajax.datosPersona(informacionSolicitud.PersonaAsegurada_id)
    
    programa = Programa.objects.filter(IdPrograma = informacionSolicitud.Programa_id)[0]
    contrato = ContratoFondo.objects.filter(IdContratoFondo = programa.IdContratoFondo)[0]
    contratoReaseguro = ContratoReaseguro.objects.using('catalogos').filter(IdContratoReaseguro = contrato.IdContratoReaseguro)[0]
    reaseguradora = Reaseguradora.objects.using('catalogos').filter(IdReaseguradora=contrato.IdReaseguradora)[0]
        
    gerenteId = PersonalApoyo.objects.filter(CargoPersonaApoyo = "GERENTE")[0]
    datosGerente = ajax.datosPersona(gerenteId.Persona_id) 
    
    #Se obtiene el nombre del Fondo
    datosFondo = DatosFondo.objects.all()
    informacionFondo = ajax.datosPersona(datosFondo[0].Persona_id)
        
    html = render_to_string('cartaconstanciapdf.html', {'pagesize':'Letter', 'DatosFondo': informacionFondo, 
                                                        'InformacionConstancia':informacionConstancia,'InformacionSolicitud':informacionSolicitud,
                                                        'Asegurado':informacionAsegurado,'Contrato':contrato.NumeroContrato,'ContratoReaseguro':contratoReaseguro,
                                                        'Reaseguradora':reaseguradora.Descripcion,'FechaActual':datetime.datetime.now(),'DatosGerente':datosGerente,'usuario':request.user}, 
                                                        context_instance = RequestContext(request))
    return generar_pdf(html)

@login_required()
def cartaNoSiniestro(request, id_Constancia): #Vista para la generacion de la carta de no siniestro en la rehabilitacion de la constancia formato Pdf
    informacionConstancia = get_object_or_404(Constancia, IdConstancia = id_Constancia)
    informacionEndosoRehabilitacion = EndosoRehabilitacion.objects.get(Constancia_id = id_Constancia)
    
    #Se obtiene los datos del fondo
    datosFondo = DatosFondo.objects.all()    
    informacionFondo = ajax.datosPersona(datosFondo[0].Persona_id)
    
    html = render_to_string('cartanosiniestropdf.html', {'pagesize':'Letter','InformacionConstancia':informacionConstancia,
                                                         'FechaEndoso':informacionEndosoRehabilitacion.FechaEndoso,'DatosFondo':informacionFondo},
                            context_instance = RequestContext(request))
    
    return generar_pdf(html)

@login_required()
def listaCobroEndosos(request): # Funcion para generar el listado de los endosos cerrados que se encuentran pendientes de cobro.    
    return render(request,'listacobroendosos.html',{'usuario':request.user})

@login_required()
def reporteReciboPagoEndoso(request, id_declaracion, tipo_endoso): # Vista para generar la informacion del reporte del recibo del pago de endoso.
    
    if tipo_endoso == 'D':
           
        informacionDeclaracion = DeclaracionEndoso.objects.filter(IdDeclaracionEndoso = id_declaracion)[0]
        informePago = PagoEndosoDeclaracion.objects.filter(DeclaracionEndoso_id = id_declaracion)[0]
        
    elif tipo_endoso == 'T':        
        informacionDeclaracion = DeclaracionTransporte.objects.filter(IdDeclaracionTransporte = id_declaracion)[0]
        informePago = PagoEndosoTransporte.objects.filter(DeclaracionTransporte_id = id_declaracion)[0]
        
    informacionConstancia = Constancia.objects.filter(IdConstancia = informacionDeclaracion.Constancia_id)[0]
    informacionSolicitud = Solicitud.objects.filter(IdSolicitud = informacionConstancia.Solicitud_id)[0]    
    informacionAsegurado = ajax.datosPersona(informacionSolicitud.PersonaAsegurada_id)
    
    importe = informacionDeclaracion.ImportePagado
        
    html = render_to_string('recibopagoendoso.html', {'pagesize':'Letter', 'idDeclaracion':id_declaracion, 'importe':importe, 'folioRecibo':informePago.FolioRecibo, 'informacionConstancia':informacionConstancia,
                                                        'informacionSolicitud':informacionSolicitud, 'asegurado':informacionAsegurado, 'fechaPago':informacionDeclaracion.FechaPago, 'usuario':request.user},
                                                         context_instance = RequestContext(request))
    return generar_pdf(html)


@login_required()
def pagoEndoso(request,id_controlendoso): #Vista para la generacion del pago de endoso.
    
    informacionControlEndoso = ControlEndoso.objects.filter(IdControlEndoso = id_controlendoso)[0]
    
    if informacionControlEndoso:
    
        informacionConstancia = Constancia.objects.filter(IdConstancia = informacionControlEndoso.Constancia_id)[0]
        informacionSolicitud = Solicitud.objects.filter(IdSolicitud = informacionConstancia.Solicitud_id)[0]
        informacionAsegurado = ajax.datosPersona(informacionSolicitud.PersonaAsegurada_id)
        informacionContratante = ajax.datosPersona(informacionSolicitud.PersonaContratante_id)
        informacionBeneficiarios = Beneficiario.objects.filter(Solicitud_id = informacionSolicitud.IdSolicitud)
        informacionSolicitudEndoso = SolicitudEndoso.objects.filter(Constancia_id=informacionConstancia.IdConstancia, Utilizado=1)[0]
        
        listBeneficiarios = list()
        
        for beneficiario in informacionBeneficiarios:
            datosBeneficiario = ajax.datosPersona(beneficiario.PersonaBeneficiario_id)
            listBeneficiarios.append({'NombrePersonaBeneficiario':datosBeneficiario[0]['NombrePersona'],'DomicilioPersonaBeneficiario':datosBeneficiario[0]['DireccionPersona'],
                                      'RfcPersonaBeneficiario':datosBeneficiario[0]['RfcPersona'],'IdBeneficiario':beneficiario.IdBeneficiario,'Porcentaje':beneficiario.Porcentaje})   
        
        informacionActaVerificacion = ActaVerificacionSolicitud.objects.filter(Solicitud_id = informacionSolicitud.IdSolicitud)[0]
        vigenciaFinalYear = informacionActaVerificacion.FechaCampo.year+1
        vigenciaFinalDia = '{:02d}'.format(informacionActaVerificacion.FechaCampo.day)
        vigenciaFinalMes = '{:02d}'.format(informacionActaVerificacion.FechaCampo.month)
        if bisiesto(vigenciaFinalYear):
            if vigenciaFinalMes == '02' and vigenciaFinalDia == '29':
                vigenciaFinalDia = '28'
        vigenciaFinal = vigenciaFinalDia + '/' + vigenciaFinalMes + '/' + str(vigenciaFinalYear)
        
        programa = Programa.objects.filter(IdPrograma = informacionSolicitud.Programa_id)[0]
        contrato = ContratoFondo.objects.filter(IdContratoFondo = programa.IdContratoFondo)[0]
    
        informacionRelacionAnexaActaVerificacion = RelacionAnexaActaVerificacion.objects.filter(Solicitud_id = informacionSolicitud.IdSolicitud)[0]
        informacionDescripcionBienes = DescripcionBienEndosoAD.objects.filter(SolicitudEndoso_id=informacionSolicitudEndoso.IdSolicitudEndoso, Utilizado = 1)
        listDescripcionBienes = list()
        sumaAseguradaBienes = 0
        
        for bienes in informacionDescripcionBienes:
            valorUnitario = '{:10,.4f}'.format(bienes.ValorUnitario)
            sumaAsegurada = '{:10,.4f}'.format(bienes.Cantidad * bienes.ValorUnitario)
            sumaAseguradaBienes = sumaAseguradaBienes + (bienes.Cantidad * bienes.ValorUnitario)
            listDescripcionBienes.append({'IdBien':bienes.IdDescripcionBienEndosoAD,'NombreEquipo':bienes.NombreEquipo,'Marca':bienes.Marca,'Modelo':bienes.Modelo,'Serie':bienes.Serie, 'DocumentacionEvaluacion':bienes.DocumentacionEvaluacion,
                                      'FechaBien':bienes.FechaBien,'Cantidad':'{:,}'.format(bienes.Cantidad),'ValorUnitario':valorUnitario,'SumaAsegurada':sumaAsegurada,
                                      'CantidadOriginal':bienes.Cantidad,'ValorUnitarioOriginal':bienes.ValorUnitario})
        
        coberturasProgramas = CoberturaPrograma.objects.filter(Programa_id = informacionSolicitud.Programa_id)
        cotizador = Cotizador.objects.filter(Programa_id = informacionSolicitud.Programa_id)[0]
        listCoberturasProgramas = list()
        cuotaNeta = 0
        totalTarifa = 0
        totalTarifaFondo = 0
        totalTarifaReaseguro = 0
        totalTarifaFondoActualizada = 0
        totalTarifaReaseguroActualizada = 0
        totalTarifaActualizada = 0
        totalFondo = 0
        totalReaseguro = 0
            
        sumaAseguradaBienesAumento = informacionControlEndoso.SumaAseguradaEndoso - informacionControlEndoso.SumaAseguradaAnterior
        
        for coberturaPrograma in coberturasProgramas:
            coberturaCatalogo = Cobertura.objects.using('catalogos').filter(IdCobertura = coberturaPrograma.IdCobertura)[0]
            tarifas = CotizadorCobertura.objects.filter(CoberturaPrograma_id = coberturaPrograma.IdCoberturaPrograma)[0]
            totalTarifa = totalTarifa + tarifas.Tarifa
            
            diaFechaAnoFin = informacionConstancia.VigenciaFin.year+1
            diaFechaMesFin = informacionConstancia.VigenciaFin.month
            diaFechaDiaFin = informacionConstancia.VigenciaFin.day
            
            diaFechaAnoInicio = informacionSolicitudEndoso.FechaSolicitudEndoso.year+1
            diaFechaMesInicio = informacionSolicitudEndoso.FechaSolicitudEndoso.month
            diaFechaDiaInicio = informacionSolicitudEndoso.FechaSolicitudEndoso.day
            
            diasRestantes = datetime.date(int(diaFechaAnoFin),int(diaFechaMesFin),int(diaFechaDiaFin)) - datetime.date(int(diaFechaAnoInicio),int(diaFechaMesInicio),int(diaFechaDiaInicio))
            
            tarifaActualizada = (tarifas.Tarifa * diasRestantes.days) / 365
            totalTarifaActualizada = totalTarifaActualizada + tarifaActualizada
            tarifaFondoActualizada = (cotizador.PorcentajeFondo * tarifaActualizada) / 100
            tarifaReaseguroActualizada = (cotizador.PorcentajeReaseguro * tarifaActualizada) / 100
            
            #Se calculan las tarifas para el fondo y el reaseguro
            totalTarifaFondoActualizada = totalTarifaFondoActualizada + tarifaFondoActualizada
            totalTarifaReaseguroActualizada = totalTarifaReaseguroActualizada + tarifaReaseguroActualizada
            
            if coberturaPrograma.IdCobertura == 3: # Si la cobertura es remocion de escombros se calcula un % sobre la suma asegurada y se aplica la tarifa.
                sumaAsegurada = (sumaAseguradaBienesAumento*tarifas.Remocion)/100
            else:
                sumaAsegurada = sumaAseguradaBienesAumento
                
            if cotizador.Prima == 1:
                FondoCuotaActualizado = (sumaAsegurada*tarifaFondoActualizada)/1000
                ReaseguroCuotaActualizada = (sumaAsegurada*tarifaReaseguroActualizada)/1000
            else:
                FondoCuotaActualizado = (sumaAsegurada*tarifaFondoActualizada)/100
                ReaseguroCuotaActualizada = (sumaAsegurada*tarifaReaseguroActualizada)/100
                
            totalFondo = totalFondo + FondoCuotaActualizado
            totalReaseguro = totalReaseguro + ReaseguroCuotaActualizada
            cuotaNeta = cuotaNeta + FondoCuotaActualizado + ReaseguroCuotaActualizada
            listCoberturasProgramas.append({'Descripcion':coberturaCatalogo.Descripcion,'Tarifa':tarifas.Tarifa,'TarifaActualizada':'{:10,.4f}'.format(tarifaActualizada), 'Fondo':'{:10,.4f}'.format(FondoCuotaActualizado),
                                            'Reaseguro':'{:10,.4f}'.format(ReaseguroCuotaActualizada),'SubTotal':'{:10,.4f}'.format(FondoCuotaActualizado+ReaseguroCuotaActualizada),'IdCobertura':coberturaPrograma.IdCobertura,
                                            'TarifaFondo':'{:10,.4f}'.format(tarifaFondoActualizada),'TarifaReaseguro':'{:10,.4f}'.format(tarifaReaseguroActualizada),'FondoCuota':'{:10,.4f}'.format(FondoCuotaActualizado),
                                            'ReaseguroCuota':'{:10,.4f}'.format(ReaseguroCuotaActualizada)})
       
    return render(request, 'pagoendoso.html', {'InformacionSolicitud':informacionSolicitud,'Asegurado':informacionAsegurado,'Contratante':informacionContratante,
                                               'VigenciaInicio':informacionActaVerificacion.FechaCampo,'VigenciaFinal':vigenciaFinal,'Cotizador':cotizador,
                                               'Beneficiarios':listBeneficiarios,'Coberturas':listCoberturasProgramas,'NumeroContrato':contrato.NumeroContrato,
                                               'SumaAseguradaBienes':'{:10,.4f}'.format(sumaAseguradaBienes),'DescripcionBienes':listDescripcionBienes,'CuotaNeta':'{:10,.4f}'.format(cuotaNeta),
                                               'InformacionConstancia':informacionConstancia,'InformacionRelacionAnexaActaVerificacion':informacionRelacionAnexaActaVerificacion,'TotalTarifa':totalTarifa, 
                                               'TotalTarifaActualizada': '{:10,.4f}'.format(totalTarifaActualizada), 'TotalTarifaFondo':'{:10,.4f}'.format(totalTarifaFondoActualizada),
                                               'TotalTarifaReaseguro':'{:10,.4f}'.format(totalTarifaReaseguroActualizada), 'InformacionSolicitudEndoso':informacionSolicitudEndoso,
                                               'SumaAseguradaAumento':'{:10,.4f}'.format(sumaAseguradaBienesAumento), 'TotalFondo':'{:10,.4f}'.format(totalFondo), 'TotalReaseguro':'{:10,.4f}'.format(totalReaseguro), 'usuario':request.user})  


def bisiesto(year): #funcion para determinar si el anho es bisiesto
    if (year % 4 == 0 and not year % 100 == 0) or year % 400 == 0:
        return True
    else:
        return False

@login_required()
def listaPagoEndoso(request): #Funcion para generar el listado de las constancias pendientes de cobro
    return render(request,'listapagoendoso.html', {'usuario':request.user})

@login_required()
def reporteReciboPagoEndosoAumento(request, id_pagoendoso): # Vista para generar la informacion del reporte del recibo del pago de endoso de aumento.
    
    informacionPagoEndoso = PagoEndosoADC.objects.filter(IdPagoEndosoADC = id_pagoendoso)[0]
    
    informacionConstancia = ''
    informacionSolicitudEndoso = ''
    informacionSolicitud = ''
    informacionAsegurado = ''
    
    if informacionPagoEndoso:
                
        informacionConstancia = Constancia.objects.filter(IdConstancia = informacionPagoEndoso.Constancia_id)[0]
        informacionSolicitudEndoso = SolicitudEndoso.objects.filter(IdSolicitudEndoso = informacionPagoEndoso.SolicitudEndoso_id)[0]
        informacionSolicitud = Solicitud.objects.filter(IdSolicitud = informacionConstancia.Solicitud_id)[0]
        informacionAsegurado = ajax.datosPersona(informacionSolicitud.PersonaAsegurada_id)
        
    html = render_to_string('recibopagoendosoaumento.html', {'pagesize':'Letter', 'informacionConstancia':informacionConstancia, 'informacionPagoEndoso':informacionPagoEndoso,
                                                      'informacionSolicitud':informacionSolicitud, 'asegurado':informacionAsegurado,
                                                      'informacionSolicitudEndoso':informacionSolicitudEndoso, 'montoAPagar':'{:10,.4f}'.format(informacionPagoEndoso.MontoAPagar)},
                                                         context_instance = RequestContext(request))
    return generar_pdf(html)

@login_required()
def cobroEndosoTransporteDeclaracion(request, id_declaracion, tipo_declaracion): # Funcion que nos permite generar la platilla con la informacion necesaria para el cobro de endoso de transporte y declaracion.
        
    if tipo_declaracion == 'D':
        declaracion = DeclaracionEndoso.objects.filter(IdDeclaracionEndoso = id_declaracion)[0]
        endoso = Endoso.objects.filter(DeclaracionEndoso_id = id_declaracion)[0]
        tipo = 'DECLARACION'
    elif tipo_declaracion == 'T': 
        declaracion = DeclaracionTransporte.objects.filter(IdDeclaracionTransporte = id_declaracion)[0]
        endoso = EndosoTransporte.objects.filter(DeclaracionTransporte_id = id_declaracion)[0]
        tipo = 'TRANSPORTE'
    
    constancia = Constancia.objects.filter(IdConstancia = declaracion.Constancia_id)[0]
    solicitud = Solicitud.objects.filter(IdSolicitud = constancia.Solicitud_id)[0]
    
    informacionAsegurado = ajax.datosPersona(solicitud.PersonaAsegurada_id)   
    
    return render(request,'cobroendosotransportedeclaracion.html',{'fechaPago':datetime.datetime.now(), 'folioConstancia':constancia.FolioConstancia, 'folioEndoso':id_declaracion, 'tipoEndoso':tipo,
                                                                   'asegurado':informacionAsegurado, 'totalAPagar':'{:10,.4f}'.format(float(endoso.ImporteTotal)), 'tipoDeclaracion':tipo_declaracion, 'usuario':request.user})


@login_required()
def pagoPrimaDeposito(request, id_constancia): # Funcion que nos permite generar la informacion para el pago de la prima en deposito. 
    
    cursor = connections['siobicx'].cursor() # Se busca la constancia a para mostrar la informacion en el reporte del endoso de cancelacion.
    sql_string = 'SELECT * FROM vconstanciasprimadeposito Where IdConstancia = ' + id_constancia
    cursor.execute(sql_string)
    datosConstancia = cursor.fetchall()
    
    if datosConstancia:
        informacionAsegurado = ajax.datosPersona(datosConstancia[0][7])   
        
        informacionRelacionAnexaActaVerificacion = RelacionAnexaActaVerificacion.objects.filter(Solicitud_id = datosConstancia[0][8])[0]
        informacionDescripcionBienes = DescripcionBienActaVerificacion.objects.filter(RelacionAnexaActaVerificacion_id = informacionRelacionAnexaActaVerificacion.IdRelacionAnexaActaVerificacion)
        listDescripcionBienes = list()
        sumaAseguradaBienes = 0
        for bienes in informacionDescripcionBienes:
            valorUnitario = '{:10,.2f}'.format(bienes.ValorUnitario)
            sumaAsegurada = '{:10,.2f}'.format(bienes.Cantidad * bienes.ValorUnitario)
            sumaAseguradaBienes = sumaAseguradaBienes + (bienes.Cantidad * bienes.ValorUnitario)
            listDescripcionBienes.append({'IdBien':bienes.IdDescripcionBienActaVerificacion,'NombreEquipo':bienes.NombreEquipo,'Marca':bienes.Marca,'Modelo':bienes.Modelo,'Serie':bienes.Serie, 'DocumentacionEvaluacion':bienes.DocumentacionEvaluacion,
                                      'FechaBien':bienes.FechaBien,'Cantidad':'{:,}'.format(bienes.Cantidad),'ValorUnitario':valorUnitario,'SumaAsegurada':sumaAsegurada,
                                      'CantidadOriginal':bienes.Cantidad,'ValorUnitarioOriginal':bienes.ValorUnitario})
    
        coberturasProgramas = CoberturaPrograma.objects.filter(Programa_id = datosConstancia[0][9])
        cotizador = Cotizador.objects.filter(Programa_id = datosConstancia[0][9])[0]
        listCoberturasProgramas = list()
        cuotaNeta = 0
        totalTarifa = 0
        totalTarifaFondo = 0
        totalTarifaReaseguro = 0
        for coberturaPrograma in coberturasProgramas:
                coberturaCatalogo = Cobertura.objects.using('catalogos').filter(IdCobertura = coberturaPrograma.IdCobertura)[0]
                tarifas = CotizadorCobertura.objects.filter(CoberturaPrograma_id = coberturaPrograma.IdCoberturaPrograma)[0]
                totalTarifa = totalTarifa + tarifas.Tarifa
                #Se calculan las tarifas para el fondo y el reaseguro
                tarifaFondo = (cotizador.PorcentajeFondo * tarifas.Tarifa) / 100
                tarifaReaseguro = (cotizador.PorcentajeReaseguro * tarifas.Tarifa) / 100
                totalTarifaFondo = totalTarifaFondo + tarifaFondo
                totalTarifaReaseguro = totalTarifaReaseguro + tarifaReaseguro
                if coberturaPrograma.IdCobertura == 3: #Si la cobertura es remocion de escombros se calcula un % sobre la suma asegurada y se aplica la tarifa
                    sumaAsegurada = (sumaAseguradaBienes*tarifas.Remocion)/100
                else:
                    sumaAsegurada = sumaAseguradaBienes
                if cotizador.Prima == 1:
                    FondoCuota = (sumaAsegurada*tarifaFondo)/1000
                    ReaseguroCuota = (sumaAsegurada*tarifaReaseguro)/1000
                else:
                    FondoCuota = (sumaAsegurada*tarifaFondo)/100
                    ReaseguroCuota = (sumaAsegurada*tarifaReaseguro)/100
                cuotaNeta = cuotaNeta + FondoCuota + ReaseguroCuota
                listCoberturasProgramas.append({'Descripcion':coberturaCatalogo.Descripcion,'Tarifa':tarifas.Tarifa,'Fondo':'{:10,.2f}'.format(FondoCuota),
                                                'Reaseguro':'{:10,.2f}'.format(ReaseguroCuota),'SubTotal':'{:10,.2f}'.format(FondoCuota+ReaseguroCuota),'IdCobertura':coberturaPrograma.IdCobertura,
                                                'TarifaFondo':tarifaFondo,'TarifaReaseguro':tarifaReaseguro,'FondoCuota':FondoCuota,'ReaseguroCuota':ReaseguroCuota})

                                                             
    
    return render(request, 'pagoprimadeposito.html', {'Asegurado':informacionAsegurado, 'Coberturas':listCoberturasProgramas, 'SumaAseguradaBienes':'{:10,.2f}'.format(sumaAseguradaBienes),'DescripcionBienes':listDescripcionBienes,'CuotaNeta':'{:10,.2f}'.format(cuotaNeta),
                                               'datosConstancia':datosConstancia,'InformacionRelacionAnexaActaVerificacion':informacionRelacionAnexaActaVerificacion,'TotalTarifa':totalTarifa,
                                               'TotalTarifaFondo':totalTarifaFondo,'TotalTarifaReaseguro':totalTarifaReaseguro,'usuario':request.user})

@login_required()
def listaPagoPrimaDeposito(request): #Funcion para generar el listado de las constancias pendientes de cobro
    return render(request,'listapagoprimadeposito.html', {'usuario':request.user})

@login_required()
def reciboPagoPrimaDeposito(request, id_pago): # Vista que obtiene la informacion necesaria para generar el recibo del pago de la prima en deposito.
    
    pagoPrimaDeposito = PagoPrimaDeposito.objects.filter(IdPagoPrimaDeposito = id_pago)[0]
    
    informacionConstancia = ''
    informacionSolicitudEndoso = ''
    informacionSolicitud = ''
    informacionAsegurado = ''
    
    if pagoPrimaDeposito:
                
        constancia = Constancia.objects.filter(IdConstancia = pagoPrimaDeposito.Constancia_id)[0]
        informacionSolicitud = Solicitud.objects.filter(IdSolicitud = str(constancia.Solicitud_id))[0]
        informacionPrograma = Programa.objects.filter(IdPrograma = informacionSolicitud.Programa_id)[0]
        informacionAsegurado = ajax.datosPersona(informacionSolicitud.PersonaAsegurada_id)
        informacionMoneda = Moneda.objects.using('catalogos').filter(IdMoneda = informacionPrograma.IdTipoMoneda)[0]
        
    html = render_to_string('recibopagoprimadeposito.html', {'pagesize':'Letter', 'informacionConstancia':constancia, 'informacionPago':pagoPrimaDeposito,
                                                      'informacionSolicitud':informacionSolicitud, 'asegurado':informacionAsegurado,'informacionMoneda':informacionMoneda,
                                                      'montoAPagar':'{:10,.4f}'.format(pagoPrimaDeposito.Monto)},
                                                         context_instance = RequestContext(request))
    return generar_pdf(html)

@login_required()
def listaPagoEndosoCancelacionAnual(request): #Funcion para generar el listado de las constancias anuales canceladas para el pago de monto no devengado.
    return render(request,'listapagoendosocancelacion.html', {'usuario':request.user})

@login_required()
def pagoEndosoCancelacionAnual(request, id_endoso): # Funcion que nos permite generar la informacion para el pago de los endosos de cancelacion de las constancias anuales pasando el endoso de cancelacion. 
    
    cursor = connections['siobicx'].cursor() # Se busca la constancia a para mostrar la informacion en el reporte del endoso de cancelacion.
    sql_string = 'SELECT * FROM vendososcancelacionanual Where IdEndosoCancelacion = ' + id_endoso
    cursor.execute(sql_string)
    datosEndoso = cursor.fetchall()
    
    if datosEndoso:
        informacionAsegurado = ajax.datosPersona(datosEndoso[0][15])   
        
        informacionRelacionAnexaActaVerificacion = RelacionAnexaActaVerificacion.objects.filter(Solicitud_id = datosEndoso[0][17])[0]
        informacionDescripcionBienes = DescripcionBienActaVerificacion.objects.filter(RelacionAnexaActaVerificacion_id = informacionRelacionAnexaActaVerificacion.IdRelacionAnexaActaVerificacion)
        listDescripcionBienes = list()
        sumaAseguradaBienes = 0
        for bienes in informacionDescripcionBienes:
            valorUnitario = '{:10,.2f}'.format(bienes.ValorUnitario)
            sumaAsegurada = '{:10,.2f}'.format(bienes.Cantidad * bienes.ValorUnitario)
            sumaAseguradaBienes = sumaAseguradaBienes + (bienes.Cantidad * bienes.ValorUnitario)
            listDescripcionBienes.append({'IdBien':bienes.IdDescripcionBienActaVerificacion,'NombreEquipo':bienes.NombreEquipo,'Marca':bienes.Marca,'Modelo':bienes.Modelo,'Serie':bienes.Serie, 'DocumentacionEvaluacion':bienes.DocumentacionEvaluacion,
                                      'FechaBien':bienes.FechaBien,'Cantidad':'{:,}'.format(bienes.Cantidad),'ValorUnitario':valorUnitario,'SumaAsegurada':sumaAsegurada,
                                      'CantidadOriginal':bienes.Cantidad,'ValorUnitarioOriginal':bienes.ValorUnitario})
    
        coberturasProgramas = CoberturaPrograma.objects.filter(Programa_id = datosEndoso[0][16])
        cotizador = Cotizador.objects.filter(Programa_id = datosEndoso[0][16])[0]
        listCoberturasProgramas = list()
        cuotaNeta = 0
        totalTarifa = 0
        totalTarifaFondo = 0
        totalTarifaReaseguro = 0
        
        for coberturaPrograma in coberturasProgramas:
                coberturaCatalogo = Cobertura.objects.using('catalogos').filter(IdCobertura = coberturaPrograma.IdCobertura)[0]
                tarifas = CotizadorCobertura.objects.filter(CoberturaPrograma_id = coberturaPrograma.IdCoberturaPrograma)[0]
                totalTarifa = totalTarifa + tarifas.Tarifa
                #Se calculan las tarifas para el fondo y el reaseguro
                tarifaFondo = (cotizador.PorcentajeFondo * tarifas.Tarifa) / 100
                tarifaReaseguro = (cotizador.PorcentajeReaseguro * tarifas.Tarifa) / 100
                totalTarifaFondo = totalTarifaFondo + tarifaFondo
                totalTarifaReaseguro = totalTarifaReaseguro + tarifaReaseguro
                if coberturaPrograma.IdCobertura == 3: #Si la cobertura es remocion de escombros se calcula un % sobre la suma asegurada y se aplica la tarifa
                    sumaAsegurada = (sumaAseguradaBienes*tarifas.Remocion)/100
                else:
                    sumaAsegurada = sumaAseguradaBienes
                if cotizador.Prima == 1:
                    FondoCuota = (sumaAsegurada*tarifaFondo)/1000
                    ReaseguroCuota = (sumaAsegurada*tarifaReaseguro)/1000
                else:
                    FondoCuota = (sumaAsegurada*tarifaFondo)/100
                    ReaseguroCuota = (sumaAsegurada*tarifaReaseguro)/100
                cuotaNeta = cuotaNeta + FondoCuota + ReaseguroCuota
                listCoberturasProgramas.append({'Descripcion':coberturaCatalogo.Descripcion,'Tarifa':tarifas.Tarifa,'Fondo':'{:10,.2f}'.format(FondoCuota),
                                                'Reaseguro':'{:10,.2f}'.format(ReaseguroCuota),'SubTotal':'{:10,.2f}'.format(FondoCuota+ReaseguroCuota),'IdCobertura':coberturaPrograma.IdCobertura,
                                                'TarifaFondo':tarifaFondo,'TarifaReaseguro':tarifaReaseguro,'FondoCuota':FondoCuota,'ReaseguroCuota':ReaseguroCuota})                                                             
    
    return render(request, 'pagoendosocancelacion.html', {'Asegurado':informacionAsegurado, 'Coberturas':listCoberturasProgramas, 'SumaAseguradaBienes':'{:10,.2f}'.format(sumaAseguradaBienes),'DescripcionBienes':listDescripcionBienes,'CuotaNeta':'{:10,.2f}'.format(cuotaNeta),
                                               'datosEndoso':datosEndoso,'InformacionRelacionAnexaActaVerificacion':informacionRelacionAnexaActaVerificacion,'TotalTarifa':totalTarifa,
                                               'TotalTarifaFondo':totalTarifaFondo,'TotalTarifaReaseguro':totalTarifaReaseguro, 'MontoAPagar':'{:10,.2f}'.format(datosEndoso[0][10]),'usuario':request.user})
    

@login_required()
def reciboPagoEndosoCancelacion(request, id_pago): # Vista que obtiene la informacion necesaria para generar el recibo del pago del endoso de cancelacion de las constancias anuales.
    
    pagoEndosoCancelacion = PagoEndosoCancelacion.objects.filter(IdPagoEndosoCancelacion = id_pago)[0]
    
    informacionConstancia = ''
    informacionEndoso = ''
    informacionSolicitud = ''
    informacionAsegurado = ''
    
    if pagoEndosoCancelacion:
                
        constancia = Constancia.objects.filter(IdConstancia = pagoEndosoCancelacion.Constancia_id)[0]
        informacionEndoso = EndosoCancelacion.objects.filter(Constancia_id = constancia.IdConstancia)[0]
        informacionSolicitud = Solicitud.objects.filter(IdSolicitud = str(constancia.Solicitud_id))[0]
        informacionPrograma = Programa.objects.filter(IdPrograma = informacionSolicitud.Programa_id)[0]
        informacionAsegurado = ajax.datosPersona(informacionSolicitud.PersonaAsegurada_id)
        informacionMoneda = Moneda.objects.using('catalogos').filter(IdMoneda = informacionPrograma.IdTipoMoneda)[0]
        
    html = render_to_string('recibopagoendosocancelacion.html', {'pagesize':'Letter', 'informacionConstancia':constancia, 'informacionPago':pagoEndosoCancelacion,
                                                      'informacionSolicitud':informacionSolicitud, 'asegurado':informacionAsegurado,'informacionMoneda':informacionMoneda,
                                                      'informacionEndoso':informacionEndoso,'montoAPagar':'{:10,.4f}'.format(pagoEndosoCancelacion.Monto)},
                                                         context_instance = RequestContext(request))
    return generar_pdf(html)

@login_required()
def listaCobroEndosoCancelacionADeclaracion(request): #Funcion para generar el listado de las constancias a declaracion canceladas para el pago de monto devengado.
    return render(request,'listacobroendosocancelacion.html', {'usuario':request.user})


@login_required()
def cobroEndosoCancelacion(request, id_endoso): # Funcion que nos permite generar la informacion para el cobro de los endosos de cancelacion de las constancias a declaracion pasando el endoso de cancelacion. 
    
    cursor = connections['siobicx'].cursor() # Se busca la constancia a para mostrar la informacion en el reporte del endoso de cancelacion.
    sql_string = 'SELECT * FROM vendososcancelacionadeclaracion Where IdEndosoCancelacion = ' + id_endoso
    cursor.execute(sql_string)
    datosEndoso = cursor.fetchall()
    
    if datosEndoso:
        informacionAsegurado = ajax.datosPersona(datosEndoso[0][15])   
        
        informacionRelacionAnexaActaVerificacion = RelacionAnexaActaVerificacion.objects.filter(Solicitud_id = datosEndoso[0][17])[0]
        informacionDescripcionBienes = DescripcionBienActaVerificacion.objects.filter(RelacionAnexaActaVerificacion_id = informacionRelacionAnexaActaVerificacion.IdRelacionAnexaActaVerificacion)
        listDescripcionBienes = list()
        sumaAseguradaBienes = 0
        for bienes in informacionDescripcionBienes:
            valorUnitario = '{:10,.2f}'.format(bienes.ValorUnitario)
            sumaAsegurada = '{:10,.2f}'.format(bienes.Cantidad * bienes.ValorUnitario)
            sumaAseguradaBienes = sumaAseguradaBienes + (bienes.Cantidad * bienes.ValorUnitario)
            listDescripcionBienes.append({'IdBien':bienes.IdDescripcionBienActaVerificacion,'NombreEquipo':bienes.NombreEquipo,'Marca':bienes.Marca,'Modelo':bienes.Modelo,'Serie':bienes.Serie, 'DocumentacionEvaluacion':bienes.DocumentacionEvaluacion,
                                      'FechaBien':bienes.FechaBien,'Cantidad':'{:,}'.format(bienes.Cantidad),'ValorUnitario':valorUnitario,'SumaAsegurada':sumaAsegurada,
                                      'CantidadOriginal':bienes.Cantidad,'ValorUnitarioOriginal':bienes.ValorUnitario})
    
        coberturasProgramas = CoberturaPrograma.objects.filter(Programa_id = datosEndoso[0][16])
        cotizador = Cotizador.objects.filter(Programa_id = datosEndoso[0][16])[0]
        listCoberturasProgramas = list()
        cuotaNeta = 0
        totalTarifa = 0
        totalTarifaFondo = 0
        totalTarifaReaseguro = 0
        
        for coberturaPrograma in coberturasProgramas:
                coberturaCatalogo = Cobertura.objects.using('catalogos').filter(IdCobertura = coberturaPrograma.IdCobertura)[0]
                tarifas = CotizadorCobertura.objects.filter(CoberturaPrograma_id = coberturaPrograma.IdCoberturaPrograma)[0]
                totalTarifa = totalTarifa + tarifas.Tarifa
                #Se calculan las tarifas para el fondo y el reaseguro
                tarifaFondo = (cotizador.PorcentajeFondo * tarifas.Tarifa) / 100
                tarifaReaseguro = (cotizador.PorcentajeReaseguro * tarifas.Tarifa) / 100
                totalTarifaFondo = totalTarifaFondo + tarifaFondo
                totalTarifaReaseguro = totalTarifaReaseguro + tarifaReaseguro
                if coberturaPrograma.IdCobertura == 3: #Si la cobertura es remocion de escombros se calcula un % sobre la suma asegurada y se aplica la tarifa
                    sumaAsegurada = (sumaAseguradaBienes*tarifas.Remocion)/100
                else:
                    sumaAsegurada = sumaAseguradaBienes
                if cotizador.Prima == 1:
                    FondoCuota = (sumaAsegurada*tarifaFondo)/1000
                    ReaseguroCuota = (sumaAsegurada*tarifaReaseguro)/1000
                else:
                    FondoCuota = (sumaAsegurada*tarifaFondo)/100
                    ReaseguroCuota = (sumaAsegurada*tarifaReaseguro)/100
                cuotaNeta = cuotaNeta + FondoCuota + ReaseguroCuota
                listCoberturasProgramas.append({'Descripcion':coberturaCatalogo.Descripcion,'Tarifa':tarifas.Tarifa,'Fondo':'{:10,.2f}'.format(FondoCuota),
                                                'Reaseguro':'{:10,.2f}'.format(ReaseguroCuota),'SubTotal':'{:10,.2f}'.format(FondoCuota+ReaseguroCuota),'IdCobertura':coberturaPrograma.IdCobertura,
                                                'TarifaFondo':tarifaFondo,'TarifaReaseguro':tarifaReaseguro,'FondoCuota':FondoCuota,'ReaseguroCuota':ReaseguroCuota})                                                             
    
    return render(request, 'cobroendosocancelacion.html', {'Asegurado':informacionAsegurado, 'Coberturas':listCoberturasProgramas, 'SumaAseguradaBienes':'{:10,.2f}'.format(sumaAseguradaBienes),'DescripcionBienes':listDescripcionBienes,'CuotaNeta':'{:10,.2f}'.format(cuotaNeta),
                                               'datosEndoso':datosEndoso,'InformacionRelacionAnexaActaVerificacion':informacionRelacionAnexaActaVerificacion,'TotalTarifa':totalTarifa,
                                               'TotalTarifaFondo':totalTarifaFondo,'TotalTarifaReaseguro':totalTarifaReaseguro, 'MontoAPagar':'{:10,.2f}'.format(datosEndoso[0][10]),'usuario':request.user})



@login_required()
def reciboCobroEndosoCancelacion(request, id_cobro): # Vista que obtiene la informacion necesaria para generar el recibo del cobro del endoso de cancelacion a delcaracion.
    
    cobroEndosoCancelacion = CobroEndosoCancelacion.objects.filter(IdCobroEndosoCancelacion = id_cobro)[0]
    
    constancia = ''
    informacionSolicitud = ''
    informacionAsegurado = ''
    
    if cobroEndosoCancelacion:
                
        constancia = Constancia.objects.filter(IdConstancia = cobroEndosoCancelacion.Constancia_id)[0]
        informacionEndoso = EndosoCancelacion.objects.filter(Constancia_id = constancia.IdConstancia)[0]
        informacionSolicitud = Solicitud.objects.filter(IdSolicitud = str(constancia.Solicitud_id))[0]
        informacionPrograma = Programa.objects.filter(IdPrograma = informacionSolicitud.Programa_id)[0]
        informacionAsegurado = ajax.datosPersona(informacionSolicitud.PersonaAsegurada_id)
        informacionMoneda = Moneda.objects.using('catalogos').filter(IdMoneda = informacionPrograma.IdTipoMoneda)[0]
        
    html = render_to_string('recibocobroendosocancelacion.html', {'pagesize':'Letter', 'informacionConstancia':constancia, 'informacionPago':cobroEndosoCancelacion,
                                                      'informacionSolicitud':informacionSolicitud, 'asegurado':informacionAsegurado,'informacionMoneda':informacionMoneda,
                                                       'informacionEndoso':informacionEndoso,'montoAPagar':'{:10,.4f}'.format(cobroEndosoCancelacion.Monto)},
                                                         context_instance = RequestContext(request))
    return generar_pdf(html)
