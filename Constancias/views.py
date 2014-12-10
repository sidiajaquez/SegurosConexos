from django.shortcuts import render, get_object_or_404
from Solicitud.models import Solicitud, ActaVerificacionSolicitud, Beneficiario, RelacionAnexaActaVerificacion, DescripcionBienActaVerificacion
from Solicitud import ajax
from Programas.models import CoberturaPrograma, Cobertura, Programa
from Cotizador.models import CotizadorCobertura, Cotizador
from ConexosAgropecuarios.models import ContratoFondo
from Constancias.models import Constancia,ConstanciaCobertura
from django.contrib.auth.decorators import login_required

@login_required()
def listaConstancias(request): #Vista para la generacion de una lista con las solicitudes aprovadas para generarles su constancia
    return render(request, 'listaconstancias.html',{'usuario':request.user})

@login_required()
def reporteConstancia(request, id_Constancia): #Generacion de la constancia para su impresion
    informacionConstancia = get_object_or_404(Constancia, IdConstancia = id_Constancia)
    informacionSolicitud = Solicitud.objects.filter(IdSolicitud = informacionConstancia.Solicitud_id)[0]
    informacionAsegurado = ajax.datosPersona(informacionSolicitud.PersonaAsegurada_id)
    informacionContratante = ajax.datosPersona(informacionSolicitud.PersonaContratante_id)
    
    informacionBeneficiarios = Beneficiario.objects.filter(Solicitud_id = informacionConstancia.Solicitud_id)
    listBeneficiarios = list()
    for beneficiario in informacionBeneficiarios:
        datosBeneficiario = ajax.datosPersona(beneficiario.PersonaBeneficiario_id)
        listBeneficiarios.append({'NombrePersonaBeneficiario':datosBeneficiario[0]['NombrePersona'],'DomicilioPersonaBeneficiario':datosBeneficiario[0]['DireccionPersona'],
                                  'RfcPersonaBeneficiario':datosBeneficiario[0]['RfcPersona'],'IdBeneficiario':beneficiario.IdBeneficiario,'Porcentaje':beneficiario.Porcentaje})

    informacionRelacionAnexaActaVerificacion = RelacionAnexaActaVerificacion.objects.filter(Solicitud_id = informacionConstancia.Solicitud_id)[0]
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
    
    cotizador = Cotizador.objects.filter(Programa_id = informacionSolicitud.Programa_id)[0]
    coberturasConstancia = ConstanciaCobertura.objects.filter(Constancia_id = id_Constancia)
    listCoberturas = list()
    cuotaNeta = 0
    totalTarifa = 0
    totalTarifaFondo = 0
    totalTarifaReaseguro = 0
    for coberturaConstancia in coberturasConstancia:
        cuotaNeta = cuotaNeta + coberturaConstancia.CuotaFondo + coberturaConstancia.CuotaReaseguro
        totalTarifa = totalTarifa + coberturaConstancia.Tarifa
        totalTarifaFondo = totalTarifaFondo + coberturaConstancia.TarifaFondo
        totalTarifaReaseguro = totalTarifaReaseguro + coberturaConstancia.TarifaReaseguro
        coberturaCatalogo = Cobertura.objects.using('catalogos').filter(IdCobertura = coberturaConstancia.IdCobertura)[0]
        listCoberturas.append({'Descripcion':coberturaCatalogo.Descripcion,'Tarifa':coberturaConstancia.Tarifa,'TarifaFondo':coberturaConstancia.TarifaFondo,
                               'TarifaReaseguro':coberturaConstancia.TarifaReaseguro,'CuotaFondo':coberturaConstancia.CuotaFondo,'CuotaReaseguro':coberturaConstancia.CuotaReaseguro,
                               'SubTotal':coberturaConstancia.CuotaFondo + coberturaConstancia.CuotaReaseguro})
    
    programa = Programa.objects.filter(IdPrograma = informacionSolicitud.Programa_id)[0]
    contrato = ContratoFondo.objects.filter(IdContratoFondo = programa.IdContratoFondo)[0]
    if programa.IdTipoMoneda == "1":
        moneda = "PESOS"
    else:
        moneda = "DOLARES"
    
    return render(request, 'reporteconstancia.html',{'InformacionConstancia':informacionConstancia,'InformacionSolicitud':informacionSolicitud,
                                                     'Asegurado':informacionAsegurado,'Contratante':informacionContratante,'Beneficiarios':listBeneficiarios,
                                                     'DescripcionBienes':listDescripcionBienes,'Coberturas':listCoberturas, 'CuotaNeta':'{:10,.4f}'.format(cuotaNeta),
                                                     'NumeroContrato':contrato.NumeroContrato,'Moneda':moneda,'Cotizador':cotizador, 'TotalTarifa':totalTarifa,
                                                     'TotalTarifaFondo':totalTarifaFondo,'TotalTarifaReaseguro':totalTarifaReaseguro,'usuario':request.user})

@login_required()
def constancia(request,id_Solicitud): #Vista para la generacion de la constancia
    informacionSolicitud = get_object_or_404(Solicitud, IdSolicitud=id_Solicitud)
    informacionAsegurado = ajax.datosPersona(informacionSolicitud.PersonaAsegurada_id)
    informacionContratante = ajax.datosPersona(informacionSolicitud.PersonaContratante_id)
    informacionConstancia = Constancia.objects.filter(Solicitud_id = id_Solicitud)
    informacionBeneficiarios = Beneficiario.objects.filter(Solicitud_id = id_Solicitud)
    listBeneficiarios = list()
    for beneficiario in informacionBeneficiarios:
        datosBeneficiario = ajax.datosPersona(beneficiario.PersonaBeneficiario_id)
        listBeneficiarios.append({'NombrePersonaBeneficiario':datosBeneficiario[0]['NombrePersona'],'DomicilioPersonaBeneficiario':datosBeneficiario[0]['DireccionPersona'],
                                  'RfcPersonaBeneficiario':datosBeneficiario[0]['RfcPersona'],'IdBeneficiario':beneficiario.IdBeneficiario,'Porcentaje':beneficiario.Porcentaje})   
    
    informacionActaVerificacion = ActaVerificacionSolicitud.objects.filter(Solicitud_id=id_Solicitud)[0]
    vigenciaFinalYear = informacionActaVerificacion.FechaCampo.year+1
    vigenciaFinalDia = '{:02d}'.format(informacionActaVerificacion.FechaCampo.day)
    vigenciaFinalMes = '{:02d}'.format(informacionActaVerificacion.FechaCampo.month)
    if bisiesto(vigenciaFinalYear):
        if vigenciaFinalMes == '02' and vigenciaFinalDia == '29':
            vigenciaFinalDia = '28'    
    vigenciaFinal = vigenciaFinalDia + '/' + vigenciaFinalMes + '/' + str(vigenciaFinalYear)
    
    programa = Programa.objects.filter(IdPrograma = informacionSolicitud.Programa_id)[0]
    contrato = ContratoFondo.objects.filter(IdContratoFondo = programa.IdContratoFondo)[0]

    informacionRelacionAnexaActaVerificacion = RelacionAnexaActaVerificacion.objects.filter(Solicitud_id = id_Solicitud)[0]
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

    coberturasProgramas = CoberturaPrograma.objects.filter(Programa_id = informacionSolicitud.Programa_id)
    cotizador = Cotizador.objects.filter(Programa_id = informacionSolicitud.Programa_id)[0]
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

    
    return render(request, 'constancia.html', {'InformacionSolicitud':informacionSolicitud,'Asegurado':informacionAsegurado,'Contratante':informacionContratante,
                                               'VigenciaInicio':informacionActaVerificacion.FechaCampo,'VigenciaFinal':vigenciaFinal,'Cotizador':cotizador,
                                               'Beneficiarios':listBeneficiarios,'Coberturas':listCoberturasProgramas,'NumeroContrato':contrato.NumeroContrato,
                                               'SumaAseguradaBienes':'{:10,.2f}'.format(sumaAseguradaBienes),'DescripcionBienes':listDescripcionBienes,'CuotaNeta':'{:10,.2f}'.format(cuotaNeta),
                                               'InformacionConstancia':informacionConstancia,'InformacionRelacionAnexaActaVerificacion':informacionRelacionAnexaActaVerificacion,'TotalTarifa':totalTarifa,
                                               'TotalTarifaFondo':totalTarifaFondo,'TotalTarifaReaseguro':totalTarifaReaseguro,'usuario':request.user})

def bisiesto(year): #funcion para determinar si el anho es bisiesto
    if (year % 4 == 0 and not year % 100 == 0) or year % 400 == 0:
        return True
    else:
        return False