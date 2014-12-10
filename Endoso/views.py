#encoding:utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from datetime import datetime
from Solicitud import ajax
from ConexosAgropecuarios.models import Moneda, Persona, DatosFondo
from Endoso.models import DeclaracionEndoso, DeclaracionEndosoPorDia, Endoso, DeclaracionTransporte, DeclaracionTransportePorUnidad, EndosoTransporte, SolicitudEndoso, DescripcionBienEndosoAD, ControlEndoso,\
    PeriodoPagoCuotaAnual, EndosoCancelacion
from Endoso.forms import SolicitudEndosoForm
from Solicitud.models import Solicitud, ActaVerificacionSolicitud, RelacionAnexaActaVerificacion, DescripcionBienActaVerificacion
from Solicitud.forms import DescripcionDetalladaBienSolicitadoForm
from Endoso.forms import DeclaracionEndosoForm
from Constancias.models import Constancia, ConstanciaCobertura
from Programas.models import Programa    
from Cotizador.models import Cotizador
from Programas.models import TipoSeguro, SubTipoSeguro
from decimal import Decimal
#from django.db import connection
from django.template import RequestContext
from django.template.loader import render_to_string
from ConexosAgropecuarios.pdf import generar_pdf
from django.contrib.auth.decorators import login_required
from django.db import connections
from django.db.models import Q

@login_required()
def EndosoAumentoDisminucionPdf(request,id_ControlEndoso): #Metodo para la generacion en pdf del endoso de aumento y disminucion de una constancia
    informacionControlEndoso = get_object_or_404(ControlEndoso,IdControlEndoso = id_ControlEndoso)
    informacionConstancia = Constancia.objects.get(IdConstancia = informacionControlEndoso.Constancia_id)

    #Se buscan los bienes del endoso de aumento/disminucion
    informacionDescripcionBienesEndoso = DescripcionBienEndosoAD.objects.filter(SolicitudEndoso_id = informacionControlEndoso.SolicitudEndoso_id)
    listDescripcionBienes = descripcionBienes(informacionDescripcionBienesEndoso)
        
    #Se obtiene el nombre del Fondo
    datosFondo = DatosFondo.objects.all()
    for datoFondo in datosFondo:
        informacionGeneralFondo = Persona.objects.filter(IdPersona = datoFondo.Persona_id)[0]
            
    html = render_to_string ('endosoaumentodisminucionpdf.html',{'pagesize':'Letter','NombreFondo':informacionGeneralFondo.RazonSocial,'Constancia':informacionConstancia,
                                                                 'ControlEndoso':informacionControlEndoso,'DescripcionBienes':listDescripcionBienes},
                             context_instance = RequestContext(request))
    
    return generar_pdf(html)

def descripcionBienes(informacionDescripcionBienes): #Metodo para regresar una lista con los bienes estructurados de una constancia
    listDescripcionBienes = list()
    for bienes in informacionDescripcionBienes:
        valorUnitario = '{:10,.2f}'.format(bienes.ValorUnitario)
        sumaAsegurada = '{:10,.2f}'.format(bienes.Cantidad * bienes.ValorUnitario)
        listDescripcionBienes.append({'IdBien':bienes,'NombreEquipo':bienes.NombreEquipo,'Marca':bienes.Marca,'Modelo':bienes.Modelo,'Serie':bienes.Serie, 'DocumentacionEvaluacion':bienes.DocumentacionEvaluacion,
                                  'FechaBien':bienes.FechaBien,'Cantidad':'{:,}'.format(bienes.Cantidad),'ValorUnitario':valorUnitario,'SumaAsegurada':sumaAsegurada,
                                  'CantidadOriginal':bienes.Cantidad,'ValorUnitarioOriginal':bienes.ValorUnitario})
    
    return listDescripcionBienes    

class EndosoAumentoDisminucionDetailView(DetailView): #Vista generica para la generacion de los endosos de aumento y disminucion
    model = Constancia
    template_name = "endosoaumentodisminucion.html"
    context_object_name = "Constancia"
    tipoEndoso = None
    
    def get(self, request, *args,**kwargs):
        objetoConstancia = self.get_object()
        tieneEndoso = ''
        if not objetoConstancia.Utilizado: #Si la Constancia todavia no tiene adjuntado el endoso de aumento en los bienes se verifica que tenga una solicitud de endoso
            #Validamos que la constancia cuente con un endoso de aumento o disminucion
            tieneEndoso = SolicitudEndoso.objects.filter(Constancia_id = objetoConstancia,TipoEndoso = self.tipoEndoso, Utilizado = True)
        
        if not tieneEndoso:
            if self.tipoEndoso == "AUMENTO":
                return HttpResponseRedirect('/ListadoAumentoEndoso/')
            elif self.tipoEndoso == "DISMINUCIÓN":
                return HttpResponseRedirect('/ListadoDisminucionEndoso/')
        else:
            return super(EndosoAumentoDisminucionDetailView, self).get(request, *args, **kwargs)
    
    def get_context_data(self,**kwargs):
        objetoConstancia = self.get_object()
        context = super(EndosoAumentoDisminucionDetailView,self).get_context_data(**kwargs)
        informacionSolicitudEndoso  = SolicitudEndoso.objects.filter(Constancia_id = objetoConstancia,Utilizado=1)[0]
        informacionConstancia = Constancia.objects.get(IdConstancia = informacionSolicitudEndoso.Constancia_id)
        programaConstancia = Solicitud.objects.select_related().get(IdSolicitud = informacionConstancia.Solicitud_id)
        informacionAsegurado = ajax.datosPersona(programaConstancia.PersonaAsegurada_id)
        tipoMoneda = Moneda.objects.using('catalogos').get(IdMoneda = programaConstancia.Programa.IdTipoMoneda)
        informacionActaVerificacionSolicitud = ActaVerificacionSolicitud.objects.get(Solicitud_id = informacionConstancia.Solicitud_id)
        #Verifica si tiene nuevos Bienes Endosados
        informacionDescripcionBienes = DescripcionBienEndosoAD.objects.filter(Constancia_id = objetoConstancia,Utilizado=True)
        if not informacionDescripcionBienes: #si no cuenta con endosos, entonces se muestran los bienes que se tengan en la acta de verificacion       
            informacionRelacionAnexa = RelacionAnexaActaVerificacion.objects.filter(Solicitud_id = informacionConstancia.Solicitud_id)[0]
            informacionDescripcionBienes = DescripcionBienActaVerificacion.objects.filter(RelacionAnexaActaVerificacion_id = informacionRelacionAnexa.IdRelacionAnexaActaVerificacion)

        listDescripcionBienes = descripcionBienes(informacionDescripcionBienes)
        sumaAseguradaBienes = 0
        for bienes in informacionDescripcionBienes:
            sumaAseguradaBienes = sumaAseguradaBienes + (bienes.Cantidad * bienes.ValorUnitario)
        
        context['TipoEndoso']=self.tipoEndoso
        context['SolicitudEndoso'] = informacionSolicitudEndoso
        context['Moneda']=tipoMoneda.Descripcion
        context['ActaVerificacion'] = informacionActaVerificacionSolicitud.IdActaVerificacionSolicitud
        context['Asegurado'] = informacionAsegurado
        context['DescripcionBienes'] = listDescripcionBienes
        context['SumaAseguradaBienes'] = '{:10,.2f}'.format(sumaAseguradaBienes)
        context['formulario_descripcion_bien'] = DescripcionDetalladaBienSolicitadoForm(auto_id='%s')
        context['usuario'] = self.request.user
        return context

endoso_aumento_detail = login_required(EndosoAumentoDisminucionDetailView.as_view(tipoEndoso="AUMENTO")) #Variable para direccionar la vista generica de un endoso de aumento
endoso_disminucion_detail = login_required(EndosoAumentoDisminucionDetailView.as_view(tipoEndoso="DISMINUCIÓN")) #Variable para direccionar la vista generica de un endoso de disminucion

@login_required()
def SolicitudEndosoImpresion(request, id_SolicitudEndoso): #Metodo para la generacion en pdf de la impresion de la solicitud de endoso
    informacionSolicitudEndoso = get_object_or_404(SolicitudEndoso,IdSolicitudEndoso = id_SolicitudEndoso)
    informacionConstancia = Constancia.objects.get(IdConstancia = informacionSolicitudEndoso.Constancia_id)
    programaConstancia = Solicitud.objects.select_related().get(IdSolicitud = informacionConstancia.Solicitud_id)
    informacionAsegurado = ajax.datosPersona(programaConstancia.PersonaAsegurada_id)
    tipoMoneda = Moneda.objects.using('catalogos').get(IdMoneda = programaConstancia.Programa.IdTipoMoneda)
    informacionActaVerificacionSolicitud = ActaVerificacionSolicitud.objects.get(Solicitud_id = informacionConstancia.Solicitud_id)
    
    #Se obtienen los bienes de la constancia
    informacionRelacionAnexa = RelacionAnexaActaVerificacion.objects.filter(Solicitud_id = informacionConstancia.Solicitud_id)[0]
    informacionDescripcionBienes = DescripcionBienActaVerificacion.objects.filter(RelacionAnexaActaVerificacion_id = informacionRelacionAnexa.IdRelacionAnexaActaVerificacion)
    listDescripcionBienes = descripcionBienes(informacionDescripcionBienes)
    
    #Se obtiene el nombre del Fondo
    datosFondo = DatosFondo.objects.all()
    for datoFondo in datosFondo:
        informacionGeneralFondo = Persona.objects.filter(IdPersona = datoFondo.Persona_id)[0]
    
    html = render_to_string('solicitudendosopdf.html',{'pagesize':'Letter','SolicitudEndoso':informacionSolicitudEndoso,'NombreFondo': informacionGeneralFondo.RazonSocial,
                                                       'Asegurado':informacionAsegurado,'Constancia':informacionConstancia,'Moneda':tipoMoneda.Descripcion,
                                                       'ActaVerificacion':informacionActaVerificacionSolicitud.IdActaVerificacionSolicitud,'DescripcionBienes':listDescripcionBienes},
                            context_instance = RequestContext(request))
    
    return generar_pdf(html)

class SolicitudEndosoDetailView(DetailView): # Vista generica para el despliegue de los datos de la constancia y el formulario que genera la solicitud de endoso
    model = Constancia
    template_name = "solicitudendoso.html"
    context_object_name = "Constancia"
    
    def get_context_data(self, **kwargs):
        objetoConstancia = self.get_object()
        context = super(SolicitudEndosoDetailView,self).get_context_data(**kwargs)
        programaConstancia = Solicitud.objects.select_related().get(IdSolicitud = objetoConstancia.Solicitud_id)
        tipoMoneda = Moneda.objects.using('catalogos').get(IdMoneda = programaConstancia.Programa.IdTipoMoneda)
        informacionAsegurado = ajax.datosPersona(programaConstancia.PersonaAsegurada_id)
        informacionActaVerificacionSolicitud = ActaVerificacionSolicitud.objects.get(Solicitud_id = objetoConstancia.Solicitud_id)
        context['Moneda'] = tipoMoneda.Descripcion
        context['Formulario'] = SolicitudEndosoForm(auto_id='%s')
        context['Asegurado'] = informacionAsegurado
        context['ActaVerificacion'] = informacionActaVerificacionSolicitud.IdActaVerificacionSolicitud
        context['DeclaracionConstancia'] = Solicitud.objects.get(IdSolicitud = objetoConstancia.Solicitud_id)
        context['usuario'] = self.request.user
        return context
    
solicitud_endoso_detail = login_required(SolicitudEndosoDetailView.as_view())

@login_required()
def listadoAumentoEndoso(request): #Vista para la generacion del listado con constancias de solicitud de endoso de aumento
    return render(request, 'listadoaumentoendoso.html',{'usuario':request.user})

@login_required()
def listadoDisminucionEndoso(request): #Vista para la generacion del listado con constancias de solicitud de endoso de disminucion
    return render(request, 'listadodisminucionendoso.html',{'usuario':request.user})

@login_required()
def listadoSolicitudEndoso(request): #Vista para la generacion del listado de constancias que requieran una solicitud de endoso
    return render(request, 'listadosolicitudendoso.html',{'usuario':request.user})

@login_required()
def listadoDeclaracionEndoso(request): # Vista que nos permite llamar la plantilla para visualizar el listado de declaraciones.
    return render(request, 'listadodeclaracionendosos.html',{'usuario':request.user})

@login_required()
def listadoDeclaracionTransporte(request): # Vista que llama a la platilla para visualizar el listado de declaracion de transporte.
    return render(request, 'listadodeclaraciontransporte.html',{'usuario':request.user})

@login_required()
def endosoDeclaracion(request, id_declaracion): # Vista que genera la informacion necesaria para el reporte de endoso de declaracion.
    
    informacionDeclaracionEndoso = DeclaracionEndoso.objects.filter(IdDeclaracionEndoso = id_declaracion)[0]
    
    constanciaBienesAsegurado = 0
    constanciaFondoPorcentaje = 0
    constanciaFondoImporte = 0
    constanciaReaseguroPorcentaje = 0
    constanciaReaseguroImporte = 0
    constanciaTotalPorcentaje = 0
    constanciaTotalImporte = 0
    
    endosoBienesAsegurados = 0
    endosoSumaAsegurada = 0
    endosoFondoImporte = 0
    endosoReaseguroImporte = 0
    endosoTotalImporte = 0
    idEndoso = ""
    informacionEndosos = list()
    
    if informacionDeclaracionEndoso:
        constanciaDeclaracion = Constancia.objects.filter(IdConstancia = informacionDeclaracionEndoso.Constancia_id)[0]
        solicitudDeclaracion = Solicitud.objects.filter(IdSolicitud = constanciaDeclaracion.Solicitud_id)[0]
        programaDeclaracion = Programa.objects.filter(IdPrograma = solicitudDeclaracion.Programa_id)[0]
        tipoSeguro = TipoSeguro.objects.using('catalogos').filter(IdTipoSeguro = programaDeclaracion.IdTipoSeguro)[0]    
        subTipoSeguro = SubTipoSeguro.objects.using('catalogos').filter(TipoSeguro_id = programaDeclaracion.IdTipoSeguro)[0]         
        declaracionesPorDia = DeclaracionEndosoPorDia.objects.filter(DeclaracionEndoso_id = informacionDeclaracionEndoso.IdDeclaracionEndoso)
        informacionSolicitante = ajax.datosPersona(solicitudDeclaracion.PersonaSolicitante_id)[0]
        
        declaracionesEndosoConstancia = DeclaracionEndoso.objects.filter(~Q(IdDeclaracionEndoso = informacionDeclaracionEndoso.IdDeclaracionEndoso), Constancia_id = constanciaDeclaracion.IdConstancia, )
        
        for declaracionEndoso in declaracionesEndosoConstancia:
            
            endosoEncontrado = Endoso.objects.filter(DeclaracionEndoso_id = declaracionEndoso.IdDeclaracionEndoso)
            
            if endosoEncontrado:
                informacionEndosos.append({'IdEndoso':endosoEncontrado[0].IdEndoso, 'DeclaracionEndoso_id':endosoEncontrado[0].DeclaracionEndoso_id, 'BienesAsegurados':'{:10,.4f}'.format(endosoEncontrado[0].BienesAsegurados), 
                                           'SumaAsegurada':'{:10,.4f}'.format(endosoEncontrado[0].SumaAsegurada), 'PorcentajeFondo':'{:10,.4f}'.format(endosoEncontrado[0].PorcentajeFondo),
                                           'ImporteFondo':'{:10,.4f}'.format(endosoEncontrado[0].ImporteFondo), 'PorcentajeReaseguro':'{:10,.4f}'.format(endosoEncontrado[0].PorcentajeFondo),
                                           'ImporteReaseguro':'{:10,.4f}'.format(endosoEncontrado[0].ImporteReaseguro), 'PorcentajeTotal':'{:10,.4f}'.format(endosoEncontrado[0].PorcentajeFondo),
                                           'ImporteTotal':'{:10,.4f}'.format(endosoEncontrado[0].ImporteTotal)})             
        
        endososGuardado = Endoso.objects.filter(DeclaracionEndoso_id = informacionDeclaracionEndoso.IdDeclaracionEndoso)
        
        endosoGuardado = ""
        
        if endososGuardado:
            endosoGuardado = endososGuardado[0] 
        
        if endosoGuardado:
            idEndoso = endosoGuardado.IdEndoso
      
        if declaracionesPorDia:
            for declaracionPorDia in declaracionesPorDia:
                endosoSumaAsegurada = endosoSumaAsegurada + int(declaracionPorDia.Valor)
                endosoBienesAsegurados = endosoBienesAsegurados + 1
        
        if constanciaDeclaracion:
            constanciasCobertura = ConstanciaCobertura.objects.filter(Constancia_id = constanciaDeclaracion.IdConstancia)
            
            for constanciaCobertura in constanciasCobertura:                                
                constanciaBienesAsegurado = constanciaBienesAsegurado + 1
                constanciaFondoPorcentaje = constanciaFondoPorcentaje + Decimal(constanciaCobertura.TarifaFondo)
                constanciaFondoImporte = constanciaFondoImporte + Decimal(constanciaCobertura.CuotaFondo)
                constanciaReaseguroPorcentaje = constanciaReaseguroPorcentaje + Decimal(constanciaCobertura.TarifaReaseguro)
                constanciaReaseguroImporte = constanciaReaseguroImporte + Decimal(constanciaCobertura.CuotaReaseguro)
                constanciaTotalPorcentaje = constanciaTotalPorcentaje + constanciaFondoPorcentaje + constanciaReaseguroPorcentaje
                constanciaTotalImporte = constanciaTotalImporte + constanciaFondoImporte + constanciaReaseguroImporte
                
        if programaDeclaracion.IdTipoMoneda == '1':
            descripcionMoneda = 'PESOS'
        else:
            descripcionMoneda = 'DOLARES'
    else:
        informacionDeclaracionEndoso = ""
        constanciaDeclaracion = ""
        solicitudDeclaracion = ""
        programaDeclaracion = ""
        descripcionMoneda = ""
        informacionEndosos = ""
    
    endosoFondoImporte = (endosoSumaAsegurada * constanciaFondoPorcentaje) / 100
    endosoReaseguroImporte = (endosoSumaAsegurada * constanciaReaseguroPorcentaje) / 100
    endosoTotalImporte = endosoFondoImporte + endosoReaseguroImporte 
        
    return render(request, 'endosodeclaracion.html', {'informacionEndoso':informacionDeclaracionEndoso, 'informacionConstancia':constanciaDeclaracion, 'informacionSolicitud':solicitudDeclaracion,
                                                      'informacionPrograma':programaDeclaracion, 'descripcionMoneda':descripcionMoneda, 'tipoSeguro': tipoSeguro.DescripcionTipoSeguro,
                                                      'subTipoSeguro':subTipoSeguro.DescripcionSubTipoSeguro,'socio':informacionSolicitante, 'constanciaBienesAsegurados':'{:10,.4f}'.format(constanciaBienesAsegurado),
                                                      'constanciaFondoPorcentaje':'{:10,.4f}'.format(constanciaFondoPorcentaje/constanciaBienesAsegurado), 'constanciaFondoImporte':'{:10,.4f}'.format(constanciaFondoImporte/constanciaBienesAsegurado),
                                                      'constanciaReaseguroPorcentaje':'{:10,.4f}'.format(constanciaReaseguroPorcentaje), 'constanciaReaseguroImporte':'{:10,.4f}'.format(constanciaReaseguroImporte), 
                                                      'constanciaTotalPorcentaje':'{:10,.4f}'.format(constanciaTotalPorcentaje), 'constanciaTotalImporte':'{:10,.4f}'.format(constanciaTotalImporte), 'endosoFondoImporte':'{:10,.4f}'.format(endosoFondoImporte),
                                                      'endosoReaseguroImporte': '{:10,.4f}'.format(endosoReaseguroImporte),'endosoTotalImporte':'{:10,.4f}'.format(endosoTotalImporte), 'endosoBienesAsegurados':'{:10,.4f}'.format(endosoBienesAsegurados), 'endosoSumaAsegurada':'{:10,.4f}'.format(endosoSumaAsegurada),
                                                      'informacionEndosos':informacionEndosos, 'idEndoso':idEndoso,'constanciaSumaAsegurada':'{:10,.4f}'.format(constanciaDeclaracion.SumaAsegurada), 'usuario':request.user})

@login_required()
def declaracionEndoso(request, id_endoso): # Vista que genera la informacion necesaria para cargargar la plantilla de declaracion de endoso mediante el id del endoso.
    date = datetime.now()
        
    informacionDeclaracionEndoso = DeclaracionEndoso.objects.filter(IdDeclaracionEndoso = id_endoso)[0]
    
    sumaPromedioDiario = 0
    sumaPrecio = 0
    sumaValor = 0
    sumaCuotaMensual = 0
    sumaCuotaPeriodo1 = 0
    sumaCuotaPeriodo2 = 0
    totalDias = 0
    totalExistencia = 0
    ultimoDiaIngresado = 0
    existenciaInicial = 0
    periodoInicio = ''
    periodoFin = ''
    idEndosoAnterior = ''
    informacionDeclaracionPorDia = list()
    
    if not informacionDeclaracionEndoso:
        informacionSolicitud = ''
        informacionSolicitante = ''
        informacionConstancia = ''
        descripcionMoneda = ''
        informacionEndosoPorDia = ''
        informacionCotizador = ''
    else:
        existenciaInicial = informacionDeclaracionEndoso.ExistenciaInicial
        periodoInicio = informacionDeclaracionEndoso.PeriodoInicio
        periodoFin = informacionDeclaracionEndoso.PeriodoFin
        informacionConstancia = Constancia.objects.filter(IdConstancia = informacionDeclaracionEndoso.Constancia_id)[0]
        informacionSolicitud = Solicitud.objects.filter(IdSolicitud = informacionConstancia.Solicitud_id)[0]
        informacionPrograma = Programa.objects.filter(IdPrograma = informacionSolicitud.Programa_id)[0]
        informacionSolicitante = ajax.datosPersona(informacionSolicitud.PersonaSolicitante_id)[0] 
        
        if informacionPrograma.IdTipoMoneda == '1':
            descripcionMoneda = 'PESOS'
        else:
            descripcionMoneda = 'DOLARES'
            
        informacionEndosoPorDia = DeclaracionEndosoPorDia.objects.filter(DeclaracionEndoso_id = informacionDeclaracionEndoso.IdDeclaracionEndoso)
        informacionCotizador = Cotizador.objects.filter(Programa_id =  informacionPrograma.IdPrograma)[0]
            
        for endosoPorDia in informacionEndosoPorDia:
            informacionDeclaracionPorDia.append({'IdEndosoPorDia':endosoPorDia.IdDeclaracionEndosoPorDia,'Dia':endosoPorDia.Dia,'Entrada':"{:10,.4f}".format(endosoPorDia.Entrada),'Salida':"{:10,.4f}".format(endosoPorDia.Salida),'Existencia':"{:10,.4f}".format(endosoPorDia.Existencia),
                                                     'Precio':"{:10,.4f}".format(endosoPorDia.Precio),'Valor':"{:10,.4f}".format(endosoPorDia.Valor),'TarifaMensual':"{:10,.4f}".format(endosoPorDia.TarifaMensual), 'TarifaDiaria':"{:10,.4f}".format(endosoPorDia.TarifaDiaria), 'Cuota':"{:10,.4f}".format(endosoPorDia.Cuota)})
            
            
        informacionDeclaracionEndosoAnterior = DeclaracionEndoso.objects.filter(Constancia_id = informacionConstancia.IdConstancia).exclude(IdDeclaracionEndoso = informacionDeclaracionEndoso.IdDeclaracionEndoso).order_by("-IdDeclaracionEndoso")
        
        if informacionDeclaracionEndosoAnterior:
            idEndosoAnterior = informacionDeclaracionEndoso.IdDeclaracionEndoso    
    
        if not informacionEndosoPorDia:
        
            sumaPromedioDiario = 0
            sumaPrecio = 0
            sumaValor =  0
            sumaCuotaMensual = 0
            sumaCuotaPeriodo1 = 0
            sumaCuotaPeriodo2 = 0
            totalDias = 0
            totalExistencia = 0
            ultimoDiaIngresado = 0
                    
        else:
            for endosoPorDia in informacionEndosoPorDia:
                sumaPromedioDiario = sumaPromedioDiario + endosoPorDia.Existencia
                sumaPrecio = sumaPrecio + endosoPorDia.Precio
                sumaValor =  sumaValor + endosoPorDia.Valor
                sumaCuotaMensual = sumaCuotaMensual + endosoPorDia.TarifaMensual
                sumaCuotaPeriodo1 = sumaCuotaPeriodo1 + endosoPorDia.TarifaDiaria
                sumaCuotaPeriodo2 = sumaCuotaPeriodo2 + endosoPorDia.Cuota
                totalDias = totalDias + 1
                totalExistencia = endosoPorDia.Existencia
                ultimoDiaIngresado = endosoPorDia.Dia
            
            sumaPromedioDiario = sumaPromedioDiario / totalDias
            sumaPrecio = sumaPrecio / totalDias
            sumaValor =  sumaValor / totalDias
            sumaCuotaMensual = sumaCuotaMensual / totalDias
            sumaCuotaPeriodo1 = sumaCuotaPeriodo1 / totalDias
            sumaCuotaPeriodo2 = sumaCuotaPeriodo2 / totalDias
       
    return render(request, 'declaracionendoso.html', {'informacionConstancia':informacionConstancia, 'informacionSolicitud':informacionSolicitud,'Solicitante':informacionSolicitante,
                                           'formulario_endoso':DeclaracionEndosoForm(auto_id='%s'),'informacionEndoso':informacionDeclaracionEndoso,
                                           'FechaActual':date, 'informacionPrograma':informacionPrograma, 'Moneda':descripcionMoneda, 
                                           'informacionEndosoPorDia':informacionDeclaracionPorDia, 'promedioDiario':"{:10,.4f}".format(sumaPromedioDiario), 'promedioPrecio':"{:10,.4f}".format(sumaPrecio), 
                                           'promedioValor':"{:10,.4f}".format(sumaValor), 'promedioCuotaMensual':"{:10,.4f}".format(sumaCuotaMensual), 'promedioCuota1':"{:10,.4f}".format(sumaCuotaPeriodo1),
                                           'promedioCuota2':"{:10,.4f}".format(sumaCuotaPeriodo2),'informacionCotizador':informacionCotizador, 'totalDias':totalDias,
                                           'totalExistencia':totalExistencia, 'ultimoDiaIngresado':ultimoDiaIngresado, 'existenciaInicial':existenciaInicial,
                                           'periodoInicio':periodoInicio, 'periodoFin':periodoFin, 'idDeclaracionEndosoAnterior':idEndosoAnterior,'usuario':request.user})

@login_required()
def declaracion_Endoso_Sin_Id(request): # Vista que se refiere al endoso cuando es nuevo.
    return render(request, 'declaracionendoso.html',{'usuario':request.user})

@login_required()
def declaracionEndoso_Id_Constancia(request, id_constancia): # Vista que genera la informacion para cargar un endoso nuevo.
    date = datetime.now()
    
    informacionConstancia = Constancia.objects.filter(IdConstancia = id_constancia).order_by()[0]    
    
    sumaPromedioDiario = 0
    sumaPrecio = 0
    sumaValor = 0
    sumaCuotaMensual = 0
    sumaCuotaPeriodo1 = 0
    sumaCuotaPeriodo2 = 0
    totalDias = 0
    totalExistencia = 0
    ultimoDiaIngresado = 0
    existenciaInicial = 0
    idEndosoAnterior = ""
    periodoInicio = ""
    periodoFin = ""
    
    if not informacionConstancia:
        informacionSolicitud = ''
        informacionSolicitante = ''
        informacionConstancia = ''
        descripcionMoneda = ''
        informacionEndosoPorDia = ''
        informacionCotizador = ''
    else:        
        informacionDeclaracionEndoso = DeclaracionEndoso.objects.filter(Constancia_id = informacionConstancia.IdConstancia).order_by("-IdDeclaracionEndoso")[0]
        idEndosoAnterior = informacionDeclaracionEndoso.IdDeclaracionEndoso
        
        dateInicio = informacionDeclaracionEndoso.PeriodoInicio
        
        if dateInicio.month == 12:
            mes = 1
            ano = dateInicio.year + 1
        else:
            mes = dateInicio.month + 1
            ano = dateInicio.year
            
        periodoInicio = "01" + '/' + str(mes) + '/' + str(ano)
        periodoFin = str(last_day_of_month(ano, mes).day) + '/' + str(mes) + '/' + str(ano)
        
        if informacionDeclaracionEndoso:    
            declaracionEndosoPorDia = DeclaracionEndosoPorDia.objects.filter(DeclaracionEndoso_id = informacionDeclaracionEndoso.IdDeclaracionEndoso).order_by('-IdDeclaracionEndosoPorDia')[0]                            
                    
            if declaracionEndosoPorDia != None:                        
                existenciaInicial = declaracionEndosoPorDia.Existencia        
        
        informacionSolicitud = Solicitud.objects.filter(IdSolicitud = informacionConstancia.Solicitud_id)[0]
        informacionPrograma = Programa.objects.filter(IdPrograma = informacionSolicitud.Programa_id)[0]
        informacionSolicitante = ajax.datosPersona(informacionSolicitud.PersonaSolicitante_id)[0] 
        
        if informacionPrograma.IdTipoMoneda == '1':
            descripcionMoneda = 'PESOS'
        else:
            descripcionMoneda = 'DOLARES'
            
        informacionEndosoPorDia = DeclaracionEndosoPorDia.objects.filter(DeclaracionEndoso_id = informacionDeclaracionEndoso.IdDeclaracionEndoso)
        informacionCotizador = Cotizador.objects.filter(Programa_id =  informacionPrograma.IdPrograma)[0]
        
        sumaPromedioDiario = 0
        sumaPrecio = 0
        sumaValor = 0
        sumaCuotaMensual = 0
        sumaCuotaPeriodo1 = 0
        sumaCuotaPeriodo2 = 0
        totalDias = 0
        totalExistencia = 0
        ultimoDiaIngresado = 0
       
        informacionDeclaracionEndoso = ""
        informacionEndosoPorDia = ""
       
    return render(request, 'declaracionendoso.html', {'informacionConstancia':informacionConstancia, 'informacionSolicitud':informacionSolicitud,'Solicitante':informacionSolicitante,
                                           'formulario_endoso':DeclaracionEndosoForm(auto_id='%s'),'informacionEndoso':informacionDeclaracionEndoso,
                                           'FechaActual':date, 'informacionPrograma':informacionPrograma, 'Moneda':descripcionMoneda, 
                                           'informacionEndosoPorDia':informacionEndosoPorDia, 'promedioDiario':sumaPromedioDiario, 'promedioPrecio':sumaPrecio, 
                                           'promedioValor':sumaValor, 'promedioCuotaMensual':sumaCuotaMensual, 'promedioCuota1':sumaCuotaPeriodo1,
                                           'promedioCuota2':sumaCuotaPeriodo2,'informacionCotizador':informacionCotizador, 'totalDias':totalDias,   
                                           'totalExistencia':totalExistencia, 'ultimoDiaIngresado':ultimoDiaIngresado,
                                           'existenciaInicial':existenciaInicial, 
                                           'periodoInicio':datetime.strptime(periodoInicio , '%d/%m/%Y'),
                                           'periodoFin':datetime.strptime(periodoFin , '%d/%m/%Y'),
                                           'idDeclaracionEndosoAnterior':idEndosoAnterior,'usuario':request.user})
    
def last_day_of_month(year, month): # Funcion que obtiene el ultimo dia de un mes recibiendo la fecha a comparar.
        last_days = [31, 30, 29, 28, 27]
        for i in last_days:
                try:
                        end = datetime(year, month, i)
                except ValueError:
                        continue
                else:
                        return end.date()
        return None

@login_required()
def declaracionTransporte(request): # Vista que nos permite llamar la plantilla para visualizar el listado de declaraciones.
    return render(request, 'declaraciontransporte.html',{'usuario':request.user})

def formatCantidadConComas(x):
    if type(x) not in [type(0), type(0L)]:
        raise TypeError("Parameter must be an integer.")
    if x < 0:
        return '-' + formatCantidadConComas(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (x, result)

@login_required()
def declaracionEndoso_id_declaracion_transporte(request, id_declaracion_transporte): # Vista que genera la informacion para crear un nuevo endoso de transporte.
    
    declaracionTransporte = DeclaracionTransporte.objects.filter(IdDeclaracionTransporte = id_declaracion_transporte)[0]     
    ultimaFechaIngresada = ''
    declaracionTransporteDiaACargar = list()  
    
    if declaracionTransporte:
        
        cursor = connections['siobicx'].cursor()
        sql_string = 'SELECT IdSolicitud, FolioSolicitud, IdTipoMoneda, Ejercicio, IdConstancia, FolioConstancia, TotalTarifa, Prima, VigenciaInicio, VigenciaFin, PersonaSolicitante_id, NombreCompleto, Rfc, Direccion, Telefono FROM vconstancias WHERE IdConstancia = ' + str(declaracionTransporte.Constancia_id)
        cursor.execute(sql_string)
        declaraciones = cursor.fetchall()
        
        if declaraciones:
            if declaraciones[0][2] == 1:
                moneda = "PESO MEXICANO"
            else:
                moneda = "DOLARES"
                
        cantidadfletes = 0
        sumaAseguradaUnitaria = 0
        sumaAseguradaTotal = 0
        importeCuota = 0

        if declaraciones[0][7] == 1:
            prima = 1000
        else:
            prima = 100

        declaracionesTransportePorDia = DeclaracionTransportePorUnidad.objects.filter(DeclaracionTransporte_id = id_declaracion_transporte)
        
        if declaracionesTransportePorDia:
            for transportePorDia in declaracionesTransportePorDia:
                cantidadfletes = cantidadfletes + 1
                sumaAseguradaUnitaria = sumaAseguradaUnitaria + transportePorDia.SumaAseguradaUnitaria
                sumaAseguradaTotal = sumaAseguradaTotal + transportePorDia.SumaAseguradaTotal
                ultimaFechaIngresada = transportePorDia.Fecha
                
                declaracionTransporteDiaACargar.append({'IdDeclaracionTransportePorUnidad':transportePorDia.IdDeclaracionTransportePorUnidad, 'DeclaracionTransporte_id':transportePorDia.DeclaracionTransporte_id,
                                                        'Romaneaje':"{:,}".format(transportePorDia.Romaneaje), 'Fecha':transportePorDia.Fecha,'Cantidad':"{:,}".format(transportePorDia.Cantidad),
                                                        'SumaAseguradaUnitaria':'{:10,.4f}'.format(transportePorDia.SumaAseguradaUnitaria), 'SumaAseguradaTotal':'{:10,.4f}'.format(transportePorDia.SumaAseguradaTotal),
                                                        'Origen':transportePorDia.Origen, 'Destino':transportePorDia.Destino})
                
        
        if cantidadfletes > 0:
            sumaAseguradaUnitaria = sumaAseguradaUnitaria / cantidadfletes
            
        importeCuota = (sumaAseguradaTotal * declaraciones[0][6]) / prima
                
    return render(request, 'declaraciontransporte.html', {'declaraciontransporte':declaracionTransporte, 'datosconstancia':declaraciones, 'declaracionestransportepordia':declaracionTransporteDiaACargar, 'moneda':moneda,
                                                          'cantidadfletes':"{:,}".format(cantidadfletes), 'sumaaseguradaunitaria':'{:10,.4f}'.format(sumaAseguradaUnitaria), 'sumaaseguradatotal':'{:10,.4f}'.format(sumaAseguradaTotal),
                                                          'importecuota':'{:10,.4f}'.format(importeCuota), 'periodoInicio':declaracionTransporte.PeriodoInicio, 'periodoFin':declaracionTransporte.PeriodoFin,
                                                          'ultimaFechaIngresada':ultimaFechaIngresada,'usuario':request.user})

@login_required()
def declaracionTransporte_Id_Constancia(request, id_constancia): # genera una nueva declaracion en base a un id de constancia.
        
    cursor = connections['siobicx'].cursor()
    sql_string = 'SELECT IdSolicitud, FolioSolicitud, IdTipoMoneda, Ejercicio, IdConstancia, FolioConstancia, TotalTarifa, Prima, VigenciaInicio, VigenciaFin, PersonaSolicitante_id, NombreCompleto, Rfc, Direccion, Telefono FROM vconstancias where IdConstancia = ' + id_constancia
    cursor.execute(sql_string)
    datosconstancia = cursor.fetchall() 
    
    moneda = ""
    periodoInicio = ""
    
    if datosconstancia:
        if datosconstancia[0][2] == 1:
            moneda = "PESO MEXICANO"
        else:
            moneda = "DOLARES"
            
        informacionDeclaracionTransporte = DeclaracionTransporte.objects.filter(Constancia_id = datosconstancia[0][4]).order_by("-IdDeclaracionTransporte")[0]
        dateInicio = informacionDeclaracionTransporte.PeriodoInicio
        idEndosoAnterior = informacionDeclaracionTransporte.IdDeclaracionTransporte
        
        if dateInicio.month == 12:
            mes = 1
            ano = dateInicio.year + 1
        else:
            mes = dateInicio.month + 1
            ano = dateInicio.year
            
        periodoInicio = "01" + '/' + str(mes) + '/' + str(ano)
        periodoFin = str(last_day_of_month(ano, mes).day) + '/' + str(mes) + '/' + str(ano)
       
    return render(request, 'declaraciontransporte.html', {'datosconstancia':datosconstancia, 'moneda':moneda, 'periodoInicio':datetime.strptime(periodoInicio , '%d/%m/%Y'), 'periodoFin':datetime.strptime(periodoFin , '%d/%m/%Y'), 'idEndosoAnterior':idEndosoAnterior,
                                                          'usuario':request.user})

@login_required()
def endosoTransporte(request, id_declaracion): # Vista que genera la informacion necesaria para el endoso de transporte.
    
    informacionDeclaracionTransporte = DeclaracionTransporte.objects.filter(IdDeclaracionTransporte = id_declaracion)[0]
    
    constanciaBienesAsegurado = 0
    constanciaFondoPorcentaje = 0
    constanciaFondoImporte = 0
    constanciaReaseguroPorcentaje = 0
    constanciaReaseguroImporte = 0
    constanciaTotalPorcentaje = 0
    constanciaTotalImporte = 0
    
    endosoBienesAsegurados = 0
    endosoSumaAsegurada = 0
    informacionEndosoTransporte = ""
    informacionEndosos = list()
    
    idEndosoTransporte = ""
    
    if informacionDeclaracionTransporte:
        informacionEndosoTransportes = EndosoTransporte.objects.filter(DeclaracionTransporte_id = id_declaracion)
        
        if informacionEndosoTransportes:
            informacionEndosoTransporte = informacionEndosoTransportes[0]
            
        constanciaDeclaracion = Constancia.objects.filter(IdConstancia = informacionDeclaracionTransporte.Constancia_id)[0]
        solicitudDeclaracion = Solicitud.objects.filter(IdSolicitud = constanciaDeclaracion.Solicitud_id)[0]
        programaDeclaracion = Programa.objects.filter(IdPrograma = solicitudDeclaracion.Programa_id)[0]
        tipoSeguro = TipoSeguro.objects.using('catalogos').filter(IdTipoSeguro = programaDeclaracion.IdTipoSeguro)[0]
        subTipoSeguro = SubTipoSeguro.objects.using('catalogos').filter(TipoSeguro_id = programaDeclaracion.IdTipoSeguro)[0]         
        declaracionesPorUnidad = DeclaracionTransportePorUnidad.objects.filter(DeclaracionTransporte_id = informacionDeclaracionTransporte.IdDeclaracionTransporte)
        informacionSolicitante = ajax.datosPersona(solicitudDeclaracion.PersonaSolicitante_id)[0]
        
        transporteEndosoConstancia = DeclaracionTransporte.objects.filter(~Q(IdDeclaracionTransporte = informacionDeclaracionTransporte.IdDeclaracionTransporte), Constancia_id = constanciaDeclaracion.IdConstancia )
        
        for transporteEndoso in transporteEndosoConstancia:
            
            endosoEncontrado = EndosoTransporte.objects.filter(DeclaracionTransporte_id = transporteEndoso.IdDeclaracionTransporte)
            
            if endosoEncontrado:
                informacionEndosos.append({'IdEndosoTransporte':endosoEncontrado[0].IdEndosoTransporte, 'DeclaracionTransporte_id':endosoEncontrado[0].DeclaracionTransporte_id,
                                           'BienesAsegurados':'{:,}'.format(endosoEncontrado[0].BienesAsegurados), 
                                           'SumaAsegurada':'{:10,.4f}'.format(endosoEncontrado[0].SumaAsegurada), 'PorcentajeFondo':'{:10,.4f}'.format(endosoEncontrado[0].PorcentajeFondo),
                                           'ImporteFondo':'{:10,.4f}'.format(endosoEncontrado[0].ImporteFondo), 'PorcentajeReaseguro':'{:10,.4f}'.format(endosoEncontrado[0].PorcentajeFondo),
                                           'ImporteReaseguro':'{:10,.4f}'.format(endosoEncontrado[0].ImporteReaseguro), 'PorcentajeTotal':'{:10,.4f}'.format(endosoEncontrado[0].PorcentajeFondo),
                                           'ImporteTotal':'{:10,.4f}'.format(endosoEncontrado[0].ImporteTotal)})        
        
                
        if informacionEndosoTransporte:
            idEndosoTransporte = informacionEndosoTransporte.IdEndosoTransporte
      
        if declaracionesPorUnidad:
            for declaracionPorUnidad in declaracionesPorUnidad:
                endosoSumaAsegurada = endosoSumaAsegurada + int(declaracionPorUnidad.SumaAseguradaTotal)
                endosoBienesAsegurados = endosoBienesAsegurados + 1
        
        if constanciaDeclaracion:
            constanciasCobertura = ConstanciaCobertura.objects.filter(Constancia_id = constanciaDeclaracion.IdConstancia)
            
            for constanciaCobertura in constanciasCobertura:                                
                constanciaBienesAsegurado = constanciaBienesAsegurado + 1
                constanciaFondoPorcentaje = constanciaFondoPorcentaje + Decimal(constanciaCobertura.TarifaFondo)
                constanciaFondoImporte = constanciaFondoImporte + Decimal(constanciaCobertura.CuotaFondo)
                constanciaReaseguroPorcentaje = constanciaReaseguroPorcentaje + Decimal(constanciaCobertura.TarifaReaseguro)
                constanciaReaseguroImporte = constanciaReaseguroImporte + Decimal(constanciaCobertura.CuotaReaseguro)
                constanciaTotalPorcentaje = constanciaTotalPorcentaje + constanciaFondoPorcentaje + constanciaReaseguroPorcentaje
                constanciaTotalImporte = constanciaTotalImporte + constanciaFondoImporte + constanciaReaseguroImporte
            
        if programaDeclaracion.IdTipoMoneda == '1':
            descripcionMoneda = 'PESOS'
        else:
            descripcionMoneda = 'DOLARES'
    else:
        informacionDeclaracionTransporte = ""
        informacionEndosoTransporte = ""
        constanciaDeclaracion = ""
        solicitudDeclaracion = ""
        programaDeclaracion = ""
        descripcionMoneda = ""
    
    endosoFondoImporte = (endosoSumaAsegurada * constanciaFondoPorcentaje) / 100
    endosoReaseguroImporte = (endosoSumaAsegurada * constanciaReaseguroPorcentaje) / 100
    endosoTotalImporte = endosoFondoImporte + endosoReaseguroImporte
    
    return render(request, 'endosotransporte.html', {'informacionTrasporte':informacionDeclaracionTransporte, 'informacionConstancia':constanciaDeclaracion, 'informacionSolicitud':solicitudDeclaracion,
                                                      'informacionPrograma':programaDeclaracion, 'descripcionMoneda':descripcionMoneda, 'tipoSeguro': tipoSeguro.DescripcionTipoSeguro,
                                                      'subTipoSeguro':subTipoSeguro.DescripcionSubTipoSeguro,'socio':informacionSolicitante, 'constanciaBienesAsegurados':constanciaBienesAsegurado,
                                                      'constanciaFondoPorcentaje':'{:10,.4f}'.format(constanciaFondoPorcentaje/constanciaBienesAsegurado), 'constanciaFondoImporte':'{:10,.4f}'.format(constanciaFondoImporte/constanciaBienesAsegurado),
                                                      'constanciaReaseguroPorcentaje':'{:10,.4f}'.format(constanciaReaseguroPorcentaje), 'constanciaReaseguroImporte':'{:10,.4f}'.format(constanciaReaseguroImporte), 
                                                      'constanciaTotalPorcentaje':'{:10,.4f}'.format(constanciaTotalPorcentaje), 'constanciaTotalImporte':'{:10,.4f}'.format(constanciaTotalImporte), 'endosoFondoImporte':'{:10,.4f}'.format(endosoFondoImporte),
                                                      'endosoReaseguroImporte': '{:10,.4f}'.format(endosoReaseguroImporte),'endosoTotalImporte':'{:10,.4f}'.format(endosoTotalImporte), 'endosoBienesAsegurados':endosoBienesAsegurados, 'endosoSumaAsegurada':'{:10,.4f}'.format(endosoSumaAsegurada),
                                                      'informacionTransportes':informacionEndosos,'constanciaSumaAsegurada': '{:10,.4f}'.format(constanciaDeclaracion.SumaAsegurada), 'idEndosoTransporte':idEndosoTransporte,'usuario':request.user})

@login_required()
def declaracion_Endoso_Impresion(request, id_declaracion): # Vista que genera la informacion necesaria para la impresion de la declaracion de endoso.
    
    cursor = connections['siobicx'].cursor()
    sql_string = 'SELECT Endoso, Constancia, Solicitud, Ejercicio, NombreAsegurado, DireccionAsegurado, PeriodoDeclaracion, Moneda, TelefonoAsegurado, Producto, ExistenciaInicial, Observaciones FROM vreportedeclaracionendoso Where Endoso = ' + id_declaracion
    cursor.execute(sql_string)
    datosReporteDeclaracion = cursor.fetchall() 
    
    totalDias = 0
    sumaPeriodoDiario = 0
    sumaValorExistenciaPeriodo = 0
    sumaCuotaPeriodo = 0
    precio = 0
    promedioDiario = 0
    cuota = 0
    promedioValorExistencia = 0
    tarifaMensual = 0
    promedioPrecio = 0
    fechaActual = datetime.now().date()
    declaracionEndosoPorDiaFormato = list()
    
    if datosReporteDeclaracion:
        declaracionEndosoPorDia = DeclaracionEndosoPorDia.objects.filter(DeclaracionEndoso_id = datosReporteDeclaracion[0][0])
        
        for declaracion in declaracionEndosoPorDia:
            
            totalDias = totalDias + 1
            sumaPeriodoDiario = sumaPeriodoDiario + declaracion.Existencia
            precio = precio + declaracion.Precio
            sumaValorExistenciaPeriodo = sumaValorExistenciaPeriodo + declaracion.Valor
            sumaCuotaPeriodo = sumaCuotaPeriodo + declaracion.TarifaDiaria 
            cuota = cuota + declaracion.Cuota
            tarifaMensual = declaracion.TarifaMensual
            
            declaracionEndosoPorDiaFormato.append({'Dia':declaracion.Dia,'Entrada':"{:10,.4f}".format(declaracion.Entrada),'Salida':"{:10,.4f}".format(declaracion.Salida),'Precio':"{:10,.4f}".format(declaracion.Precio),
                                                   'Existencia':"{:10,.4f}".format(declaracion.Existencia),'Valor':"{:10,.4f}".format(declaracion.Valor),'TarifaMensual':"{:10,.4f}".format(declaracion.TarifaMensual),
                                                   'TarifaDiaria':"{:10,.4f}".format(declaracion.TarifaDiaria),'Cuota':"{:10,.4f}".format(declaracion.Cuota)})
            

        if datosReporteDeclaracion[0][7] == 1:
            moneda = "PESO MEXICANO"
        else:
            moneda = "DOLARES"
    else:
        datosReporteDeclaracion = ""
        declaracionEndosoPorDia = ""
        moneda = ""
        
    if totalDias > 0:
        promedioDiario = sumaPeriodoDiario / totalDias
        promedioValorExistencia = sumaValorExistenciaPeriodo / totalDias        
        promedioPrecio = precio / totalDias
    
    html = render_to_string('declaracionendosopdf.html',{'pagesize':'Letter', 'datosReporte': datosReporteDeclaracion, 'Moneda':moneda, 
                                                         'declaracionEndosoPorDia': declaracionEndosoPorDiaFormato, 'promedioDiario':'{:10,.4f}'.format(promedioDiario), 'promedioPrecio':'{:10,.4f}'.format(promedioPrecio),
                                                         'promedioValorExistencia':'{:10,.4f}'.format(promedioValorExistencia), 'tarifaMensual':'{:10,.4f}'.format(tarifaMensual), 'sumaCuotaPeriodo':'{:10,.4f}'.format(sumaCuotaPeriodo),
                                                         'cuota':'{:10,.4f}'.format(cuota), 'fechaActual':fechaActual}, context_instance = RequestContext(request))
    return generar_pdf(html)

@login_required()
def declaracion_Transporte_Impresion(request, id_declaracion): # Vista que genera la informacion para la impresion de la declaracion de transporte.
        
    cursor = connections['siobicx'].cursor()
    sql_string = 'SELECT Transporte, Constancia, Solicitud, Ejercicio, NombreAsegurado, DireccionAsegurado, PeriodoDeclaracion, Moneda, TelefonoAsegurado, Producto, Observaciones, DescripcionBienAsegurado, TotalTarifa, Prima FROM vreportedeclaraciontransporte Where Transporte = ' + id_declaracion
    cursor.execute(sql_string)
    datosReporteDeclaracion = cursor.fetchall()     
                
    cantidadfletes = 0
    sumaAseguradaUnitaria = 0
    sumaAseguradaTotal = 0
    importeCuota = 0
    declaracionTransportePorUnidadACargar = list()
    
    if datosReporteDeclaracion:
        
        declaracionTransportePorUnidad = DeclaracionTransportePorUnidad.objects.filter(DeclaracionTransporte_id = id_declaracion)
        
        if datosReporteDeclaracion[0][7] == 1:
            moneda = "PESO MEXICANO"
        else:
            moneda = "DOLARES"
        
        if declaracionTransportePorUnidad:
            for transportePorUnidad in declaracionTransportePorUnidad:
                cantidadfletes = cantidadfletes + 1
                sumaAseguradaUnitaria = sumaAseguradaUnitaria + transportePorUnidad.SumaAseguradaUnitaria
                sumaAseguradaTotal = sumaAseguradaTotal + transportePorUnidad.SumaAseguradaTotal
                
                declaracionTransportePorUnidadACargar.append({'IdDeclaracionTransportePorUnidad':transportePorUnidad.IdDeclaracionTransportePorUnidad,'Romaneaje':"{:,}".format(transportePorUnidad.Romaneaje),'Fecha':transportePorUnidad.Fecha,
                                                       'Cantidad':"{:,}".format(transportePorUnidad.Cantidad), 'SumaAseguradaUnitaria':"{:10,.4f}".format(transportePorUnidad.SumaAseguradaUnitaria),
                                                       'SumaAseguradaTotal':"{:10,.4f}".format(transportePorUnidad.SumaAseguradaTotal),'Origen':transportePorUnidad.Origen,'Destino':transportePorUnidad.Destino})
        
        if cantidadfletes > 0:
            sumaAseguradaUnitaria = sumaAseguradaUnitaria / cantidadfletes
            
        if datosReporteDeclaracion[0][13] == 1:
            prima = 1000
        else:
            prima = 100
            
        importeCuota = (sumaAseguradaTotal * datosReporteDeclaracion[0][12]) / prima
        
    else:
        moneda = ""
        
    html = render_to_string('declaraciontransportepdf.html',{'pagesize':'Letter', 'datosReporteDeclaracion':datosReporteDeclaracion, 'moneda':moneda, 'declaracionTransportePorUnidad':declaracionTransportePorUnidadACargar,
                                                             'cantidadFletes':'{:10,.4f}'.format(cantidadfletes), 'sumaAseguradaUnitaria':'{:10,.4f}'.format(sumaAseguradaUnitaria), 'sumaAseguradaTotal':'{:10,.4f}'.format(sumaAseguradaTotal), 'importeCuota':'{:10,.4f}'.format(importeCuota)}
                                                             , context_instance = RequestContext(request))
    return generar_pdf(html)

@login_required()
def endoso_Declaracion_Impresion(request, id_declaracion): # Vista que genera la informacion necesaria para la impresion del endoso de declaracion.
    
    date = datetime.now()
    
    informacionDeclaracionEndoso = DeclaracionEndoso.objects.filter(IdDeclaracionEndoso = id_declaracion)[0]
    
    constanciaBienesAsegurado = 0
    constanciaFondoPorcentaje = 0
    constanciaFondoImporte = 0
    constanciaReaseguroPorcentaje = 0
    constanciaReaseguroImporte = 0
    constanciaTotalPorcentaje = 0
    constanciaTotalImporte = 0
    
    endosoBienesAsegurados = 0
    endosoSumaAsegurada = 0
    endosoFondoImporte = 0
    endosoReaseguroImporte = 0
    endosoTotalImporte = 0
    idEndoso = ""
    informacionEndosos = list()
    
    if informacionDeclaracionEndoso:
        constanciaDeclaracion = Constancia.objects.filter(IdConstancia = informacionDeclaracionEndoso.Constancia_id)[0]
        solicitudDeclaracion = Solicitud.objects.filter(IdSolicitud = constanciaDeclaracion.Solicitud_id)[0]
        programaDeclaracion = Programa.objects.filter(IdPrograma = solicitudDeclaracion.Programa_id)[0]
        tipoSeguro = TipoSeguro.objects.using('catalogos').filter(IdTipoSeguro = programaDeclaracion.IdTipoSeguro)[0]    
        subTipoSeguro = SubTipoSeguro.objects.using('catalogos').filter(TipoSeguro_id = programaDeclaracion.IdTipoSeguro)[0]         
        declaracionesPorDia = DeclaracionEndosoPorDia.objects.filter(DeclaracionEndoso_id = informacionDeclaracionEndoso.IdDeclaracionEndoso)
        informacionSolicitante = ajax.datosPersona(solicitudDeclaracion.PersonaSolicitante_id)[0] 
        
        declaracionesEndosoConstancia = DeclaracionEndoso.objects.filter(~Q(IdDeclaracionEndoso = informacionDeclaracionEndoso.IdDeclaracionEndoso), Constancia_id = constanciaDeclaracion.IdConstancia, )
        
        for declaracionEndoso in declaracionesEndosoConstancia:
            
            endosoEncontrado = Endoso.objects.filter(DeclaracionEndoso_id = declaracionEndoso.IdDeclaracionEndoso)
            
            if endosoEncontrado:
                informacionEndosos.append({'IdEndoso':endosoEncontrado[0].IdEndoso, 'DeclaracionEndoso_id':endosoEncontrado[0].DeclaracionEndoso_id, 'BienesAsegurados':'{:10,.4f}'.format(endosoEncontrado[0].BienesAsegurados), 
                                           'SumaAsegurada':'{:10,.4f}'.format(endosoEncontrado[0].SumaAsegurada), 'PorcentajeFondo':'{:10,.4f}'.format(endosoEncontrado[0].PorcentajeFondo),
                                           'ImporteFondo':'{:10,.4f}'.format(endosoEncontrado[0].ImporteFondo), 'PorcentajeReaseguro':'{:10,.4f}'.format(endosoEncontrado[0].PorcentajeFondo),
                                           'ImporteReaseguro':'{:10,.4f}'.format(endosoEncontrado[0].ImporteReaseguro), 'PorcentajeTotal':'{:10,.4f}'.format(endosoEncontrado[0].PorcentajeFondo),
                                           'ImporteTotal':'{:10,.4f}'.format(endosoEncontrado[0].ImporteTotal)})   
        
        endososGuardado = Endoso.objects.filter(DeclaracionEndoso_id = informacionDeclaracionEndoso.IdDeclaracionEndoso)
        
        endosoGuardado = ""
        
        if endososGuardado:
            endosoGuardado = endososGuardado[0]
        
        if endosoGuardado:
            idEndoso = endosoGuardado.IdEndoso
      
        if declaracionesPorDia:
            for declaracionPorDia in declaracionesPorDia:
                endosoSumaAsegurada = endosoSumaAsegurada + int(declaracionPorDia.Valor)
                endosoBienesAsegurados = endosoBienesAsegurados + 1
        
        if constanciaDeclaracion:
            constanciasCobertura = ConstanciaCobertura.objects.filter(Constancia_id = constanciaDeclaracion.IdConstancia)
            
            for constanciaCobertura in constanciasCobertura:                                
                constanciaBienesAsegurado = constanciaBienesAsegurado + 1
                constanciaFondoPorcentaje = constanciaFondoPorcentaje + Decimal(constanciaCobertura.TarifaFondo)
                constanciaFondoImporte = constanciaFondoImporte + Decimal(constanciaCobertura.CuotaFondo)
                constanciaReaseguroPorcentaje = constanciaReaseguroPorcentaje + Decimal(constanciaCobertura.TarifaReaseguro)
                constanciaReaseguroImporte = constanciaReaseguroImporte + Decimal(constanciaCobertura.CuotaReaseguro)
                constanciaTotalPorcentaje = constanciaTotalPorcentaje + constanciaFondoPorcentaje + constanciaReaseguroPorcentaje
                constanciaTotalImporte = constanciaTotalImporte + constanciaFondoImporte + constanciaReaseguroImporte
                
        if programaDeclaracion.IdTipoMoneda == '1':
            descripcionMoneda = 'PESOS'
        else:
            descripcionMoneda = 'DOLARES'
    else:

        informacionDeclaracionEndoso = ""
        constanciaDeclaracion = ""
        solicitudDeclaracion = ""
        programaDeclaracion = ""
        descripcionMoneda = ""
        informacionEndosos = ""
    
    endosoFondoImporte = (endosoSumaAsegurada * constanciaFondoPorcentaje) / 100
    endosoReaseguroImporte = (endosoSumaAsegurada * constanciaReaseguroPorcentaje) / 100
    endosoTotalImporte = endosoFondoImporte + endosoReaseguroImporte
       
    html = render_to_string('endosodeclaracionpdf.html',{'pagesize':'Letter', 'informacionEndoso':informacionDeclaracionEndoso, 'informacionConstancia':constanciaDeclaracion, 'informacionSolicitud':solicitudDeclaracion,
                                                      'informacionPrograma':programaDeclaracion, 'descripcionMoneda':descripcionMoneda, 'tipoSeguro': tipoSeguro.DescripcionTipoSeguro,
                                                      'subTipoSeguro':subTipoSeguro.DescripcionSubTipoSeguro,'socio':informacionSolicitante, 'constanciaBienesAsegurados':'{:10,.4f}'.format(constanciaBienesAsegurado),
                                                      'constanciaFondoPorcentaje':'{:10,.4f}'.format(constanciaFondoPorcentaje/constanciaBienesAsegurado), 'constanciaFondoImporte':'{:10,.4f}'.format(constanciaFondoImporte/constanciaBienesAsegurado),
                                                      'constanciaReaseguroPorcentaje':'{:10,.4f}'.format(constanciaReaseguroPorcentaje), 'constanciaReaseguroImporte':'{:10,.4f}'.format(constanciaReaseguroImporte), 
                                                      'constanciaTotalPorcentaje':'{:10,.4f}'.format(constanciaTotalPorcentaje), 'constanciaTotalImporte':'{:10,.4f}'.format(constanciaTotalImporte), 'endosoFondoImporte':'{:10,.4f}'.format(endosoFondoImporte),
                                                      'endosoReaseguroImporte':'{:10,.4f}'.format(endosoReaseguroImporte),'endosoTotalImporte':'{:10,.4f}'.format(endosoTotalImporte), 'endosoBienesAsegurados':'{:10,.4f}'.format(endosoBienesAsegurados), 'endosoSumaAsegurada':'{:10,.4f}'.format(endosoSumaAsegurada),
                                                      'informacionEndosos':informacionEndosos, 'idEndoso':idEndoso, 'fechaActual':date,'constanciaSumaAsegurada':'{:10,.4f}'.format(constanciaDeclaracion.SumaAsegurada)}, context_instance = RequestContext(request))   
        
    return generar_pdf(html)

@login_required()
def endoso_Transporte_Impresion(request, id_declaracion): # Vista que genera la informacion necesaria para la impresion del endoso de transporte.
    
    date = datetime.now()
    
    informacionDeclaracionTransporte = DeclaracionTransporte.objects.filter(IdDeclaracionTransporte = id_declaracion)[0]
    
    constanciaBienesAsegurado = 0
    constanciaFondoPorcentaje = 0
    constanciaFondoImporte = 0
    constanciaReaseguroPorcentaje = 0
    constanciaReaseguroImporte = 0
    constanciaTotalPorcentaje = 0
    constanciaTotalImporte = 0
    
    endosoBienesAsegurados = 0
    endosoSumaAsegurada = 0
    informacionEndosoTransporte = ""
    informacionEndosos = list()
    
    idEndosoTransporte = ""
    
    if informacionDeclaracionTransporte:
        informacionEndosoTransportes = EndosoTransporte.objects.filter(DeclaracionTransporte_id = id_declaracion)
        
        if informacionEndosoTransportes:
            informacionEndosoTransporte = informacionEndosoTransportes[0]
            
        constanciaDeclaracion = Constancia.objects.filter(IdConstancia = informacionDeclaracionTransporte.Constancia_id)[0]
        solicitudDeclaracion = Solicitud.objects.filter(IdSolicitud = constanciaDeclaracion.Solicitud_id)[0]
        programaDeclaracion = Programa.objects.filter(IdPrograma = solicitudDeclaracion.Programa_id)[0]
        tipoSeguro = TipoSeguro.objects.using('catalogos').filter(IdTipoSeguro = programaDeclaracion.IdTipoSeguro)[0]
        subTipoSeguro = SubTipoSeguro.objects.using('catalogos').filter(TipoSeguro_id = programaDeclaracion.IdTipoSeguro)[0]         
        declaracionesPorUnidad = DeclaracionTransportePorUnidad.objects.filter(DeclaracionTransporte_id = informacionDeclaracionTransporte.IdDeclaracionTransporte)
        informacionSolicitante = ajax.datosPersona(solicitudDeclaracion.PersonaSolicitante_id)[0]
        
        transporteEndosoConstancia = DeclaracionTransporte.objects.filter(~Q(IdDeclaracionTransporte = informacionDeclaracionTransporte.IdDeclaracionTransporte), Constancia_id = constanciaDeclaracion.IdConstancia )
        
        for transporteEndoso in transporteEndosoConstancia:
            
            endosoEncontrado = EndosoTransporte.objects.filter(DeclaracionTransporte_id = transporteEndoso.IdDeclaracionTransporte)
            
            if endosoEncontrado:
                informacionEndosos.append({'IdEndosoTransporte':endosoEncontrado[0].IdEndosoTransporte, 'DeclaracionTransporte_id':endosoEncontrado[0].DeclaracionTransporte_id,
                                           'BienesAsegurados':'{:,}'.format(endosoEncontrado[0].BienesAsegurados), 
                                           'SumaAsegurada':'{:10,.4f}'.format(endosoEncontrado[0].SumaAsegurada), 'PorcentajeFondo':'{:10,.4f}'.format(endosoEncontrado[0].PorcentajeFondo),
                                           'ImporteFondo':'{:10,.4f}'.format(endosoEncontrado[0].ImporteFondo), 'PorcentajeReaseguro':'{:10,.4f}'.format(endosoEncontrado[0].PorcentajeFondo),
                                           'ImporteReaseguro':'{:10,.4f}'.format(endosoEncontrado[0].ImporteReaseguro), 'PorcentajeTotal':'{:10,.4f}'.format(endosoEncontrado[0].PorcentajeFondo),
                                           'ImporteTotal':'{:10,.4f}'.format(endosoEncontrado[0].ImporteTotal)})    
        
        if informacionEndosoTransporte:
            idEndosoTransporte = informacionEndosoTransporte.IdEndosoTransporte
      
        if declaracionesPorUnidad:
            for declaracionPorUnidad in declaracionesPorUnidad:
                endosoSumaAsegurada = endosoSumaAsegurada + int(declaracionPorUnidad.SumaAseguradaTotal)
                endosoBienesAsegurados = endosoBienesAsegurados + 1
        
        if constanciaDeclaracion:
            constanciasCobertura = ConstanciaCobertura.objects.filter(Constancia_id = constanciaDeclaracion.IdConstancia)
            
            for constanciaCobertura in constanciasCobertura:                                
                constanciaBienesAsegurado = constanciaBienesAsegurado + 1
                constanciaFondoPorcentaje = constanciaFondoPorcentaje + Decimal(constanciaCobertura.TarifaFondo)
                constanciaFondoImporte = constanciaFondoImporte + Decimal(constanciaCobertura.CuotaFondo)
                constanciaReaseguroPorcentaje = constanciaReaseguroPorcentaje + Decimal(constanciaCobertura.TarifaReaseguro)
                constanciaReaseguroImporte = constanciaReaseguroImporte + Decimal(constanciaCobertura.CuotaReaseguro)
                constanciaTotalPorcentaje = constanciaTotalPorcentaje + constanciaFondoPorcentaje + constanciaReaseguroPorcentaje
                constanciaTotalImporte = constanciaTotalImporte + constanciaFondoImporte + constanciaReaseguroImporte
                
        if programaDeclaracion.IdTipoMoneda == '1':
            descripcionMoneda = 'PESOS'
        else:
            descripcionMoneda = 'DOLARES'
    else:
        informacionDeclaracionTransporte = ""
        informacionEndosoTransporte = ""
        constanciaDeclaracion = ""
        solicitudDeclaracion = ""
        programaDeclaracion = ""
        descripcionMoneda = ""
    
    endosoFondoImporte = (endosoSumaAsegurada * constanciaFondoPorcentaje) / 100
    endosoReaseguroImporte = (endosoSumaAsegurada * constanciaReaseguroPorcentaje) / 100
    endosoTotalImporte = endosoFondoImporte + endosoReaseguroImporte
        
    
    html = render_to_string('endosotransportepdf.html',{'pagesize':'Letter', 'informacionTrasporte':informacionDeclaracionTransporte, 'informacionConstancia':constanciaDeclaracion, 'informacionSolicitud':solicitudDeclaracion,
                                                      'informacionPrograma':programaDeclaracion, 'descripcionMoneda':descripcionMoneda, 'tipoSeguro': tipoSeguro.DescripcionTipoSeguro,
                                                      'subTipoSeguro':subTipoSeguro.DescripcionSubTipoSeguro,'socio':informacionSolicitante, 'constanciaBienesAsegurados':constanciaBienesAsegurado,
                                                      'constanciaFondoPorcentaje':'{:10,.4f}'.format(constanciaFondoPorcentaje/constanciaBienesAsegurado), 'constanciaFondoImporte':'{:10,.4f}'.format(constanciaFondoImporte/constanciaBienesAsegurado),
                                                      'constanciaReaseguroPorcentaje':'{:10,.4f}'.format(constanciaReaseguroPorcentaje), 'constanciaReaseguroImporte':'{:10,.4f}'.format(constanciaReaseguroImporte), 
                                                      'constanciaTotalPorcentaje':'{:10,.4f}'.format(constanciaTotalPorcentaje), 'constanciaTotalImporte':'{:10,.4f}'.format(constanciaTotalImporte), 'endosoFondoImporte':'{:10,.4f}'.format(endosoFondoImporte),
                                                      'endosoReaseguroImporte': '{:10,.4f}'.format(endosoReaseguroImporte),'endosoTotalImporte':'{:10,.4f}'.format(endosoTotalImporte), 'endosoBienesAsegurados':endosoBienesAsegurados, 'endosoSumaAsegurada':'{:10,.4f}'.format(endosoSumaAsegurada),
                                                      'informacionTransportes':informacionEndosos, 'constanciaSumaAsegurada':'{:10,.4f}'.format(constanciaDeclaracion.SumaAsegurada),'idEndosoTransporte':idEndosoTransporte, 'fechaActual':date}, context_instance = RequestContext(request))   
        
    return generar_pdf(html)

@login_required()
def historial_declaracion_endoso(request): #Vista para la generacion del listado que contenga todas las declaraciones de endoso de una constancia.
    return render(request, 'listadohistorialdeclaracionendoso.html',{'usuario':request.user})

@login_required()
def historial_declaracion_transporte(request): #Vista para la generacion del listado que contenga todas las declaraciones de transporte de una constancia.
    return render(request, 'listadohistorialdeclaraciontransporte.html',{'usuario':request.user})

@login_required()
def listado_endosos_cancelacion(request): #Vista para mostrar las constancias que contienen una solicitud de endoso para cancelacion.
    return render(request, 'listadoendosocancelacion.html',{'usuario':request.user})

@login_required()
def endoso_cancelacion(request, id_constancia): #Vista para la generacion del endoso de cancelacion.
    sumaAseguradaBienes = 0
    montoAPagar = 0
    countRow = 0
    sumaAsegurada = 0
    listDescripcionBien = list()
    tipoEndoso = ''
    
    # Variables para mostrar los totales del endoso de transporte.
    varCantidadFletes = 0
    varSumaUnitaria = 0
    sumaAseguradaPorDia = 0
    
    # Variables para mostrar los totales del endoso declaracion.
    varPromedioDiario = 0
    varPrecio = 0
    varExistencia = 0
    varTarifaMensual = 0
    varCuota = 0
    
    # Variables para constancias anuales.
    varCuotaAnual = 0
    diasDevengados = 0
    diasTotales = 0
    porcentaje = 0
     
    cursor = connections['siobicx'].cursor() # Se busca la constancia a cancelar.
    sql_string = 'SELECT * FROM vconstanciascancelacion Where NoConstancia = ' + id_constancia
    cursor.execute(sql_string)
    datosConstancia = cursor.fetchall()
    
    if datosConstancia:
        informacionAsegurado = ajax.datosPersona(datosConstancia[0][11])
        solicitudEndoso = SolicitudEndoso.objects.filter(Constancia_id = datosConstancia[0][0])[0]        
        descripcionBien = DescripcionBienEndosoAD.objects.filter(Constancia_id = datosConstancia[0][0])
        
        if not descripcionBien:
            relacionanexa = RelacionAnexaActaVerificacion.objects.filter(Solicitud_id = datosConstancia[0][12])[0]
            descripcionBien = DescripcionBienActaVerificacion.objects.filter(RelacionAnexaActaVerificacion_id = relacionanexa.IdRelacionAnexaActaVerificacion)   
            
    for bienes in descripcionBien:
        valorUnitario = '{:10,.4f}'.format(bienes.ValorUnitario)
        sumaAsegurada = bienes.Cantidad * bienes.ValorUnitario
        sumaAseguradaBienes = sumaAseguradaBienes + (bienes.Cantidad * bienes.ValorUnitario)
        listDescripcionBien.append({'NombreEquipo':bienes.NombreEquipo,'Marca':bienes.Marca,'Modelo':bienes.Modelo,'Serie':bienes.Serie, 'DocumentacionEvaluacion':bienes.DocumentacionEvaluacion,
                                  'FechaBien':bienes.FechaBien,'Cantidad':'{:,}'.format(bienes.Cantidad),'ValorUnitario':valorUnitario,'SumaAsegurada':'{:10,.4f}'.format(sumaAsegurada)})
       
    if datosConstancia[0][13] == 'A DECLARACIÓN': # Se busca si la constancia es a declaración.
        varEndosoDeclaracion = DeclaracionEndoso.objects.filter(Constancia_id = datosConstancia[0][0]).order_by('-IdDeclaracionEndoso')
                
        if varEndosoDeclaracion: # Checa si la constancia es a endoso de declaracion.
            varEndosoDeclaracionPorDia = DeclaracionEndosoPorDia.objects.filter(DeclaracionEndoso_id = varEndosoDeclaracion[0].IdDeclaracionEndoso)
               
            for endosoPorDia in varEndosoDeclaracionPorDia:
                varPromedioDiario = varPromedioDiario + endosoPorDia.Existencia
                varPrecio = varPrecio + endosoPorDia.Precio
                varExistencia = varExistencia + endosoPorDia.Valor
                varTarifaMensual = varTarifaMensual + endosoPorDia.TarifaMensual
                varCuota = varCuota + endosoPorDia.TarifaDiaria
                countRow = countRow + 1
            
            varPromedioDiario = varPromedioDiario / countRow
            varPrecio = varPrecio / countRow
            varExistencia = varExistencia / countRow
            varTarifaMensual = varTarifaMensual / countRow
            varCuota = varCuota / countRow
            
            if datosConstancia[0][14] == 1:
                prima = 1000
            else:
                prima = 100
            
            montoAPagar = (varExistencia * varCuota) / prima
            tipoEndoso = 'DD'    
                
        else: # Si la constancia no es a endoso de declaracion entonces es a endoso de transporte.
            montoAPagar = 0
            countRow = 0
            varEndosoTransporte = DeclaracionTransporte.objects.filter(Constancia_id = datosConstancia[0][0]).order_by('-IdDeclaracionTransporte')   
            
            if varEndosoTransporte:
                varEndosoTransportePorDia = DeclaracionTransportePorUnidad.objects.filter(DeclaracionTransporte_id = varEndosoTransporte[0].IdDeclaracionTransporte)                
            
                if datosConstancia[0][14] == 1:
                    prima = 1000
                else:
                    prima = 100
                
                for endosoPorDia in varEndosoTransportePorDia:
                    varCantidadFletes = varCantidadFletes + endosoPorDia.Cantidad
                    varSumaUnitaria = varSumaUnitaria + endosoPorDia.SumaAseguradaUnitaria
                    sumaAseguradaPorDia = sumaAseguradaPorDia + endosoPorDia.SumaAseguradaTotal
                    countRow = countRow + 1
                    
                tipoEndoso = 'DT'
                varSumaUnitaria = varSumaUnitaria / countRow
                montoAPagar = (Decimal(sumaAseguradaPorDia) * Decimal(datosConstancia[0][15])) / prima
    else:
        
        periodoPago = PeriodoPagoCuotaAnual.objects.all()
        
        tipoEndoso = 'CA'
        vigenciaInicio = datetime.strptime(datosConstancia[0][5], '%d/%m/%Y')
        vigenciaFin = datetime.strptime(datosConstancia[0][6], '%d/%m/%Y')
        fechaActual = datetime.now()
        diasDevengados = (fechaActual - vigenciaInicio).days + 1
        diasTotales = (vigenciaFin - vigenciaInicio).days
        varCuotaAnual = datosConstancia[0][16]
        
        if periodoPago:
            
            for periodo in periodoPago:
                if diasDevengados >= periodo.DiasDesde and diasDevengados <= periodo.DiasHasta:
                    porcentaje = periodo.Porcentaje
                    break;
                
            montoAPagar = (float(varCuotaAnual) * int(porcentaje)) / 100
        else:
            montoAPagar = 0
            
    return render(request, 'endosocancelacion.html',{'datosConstancia':datosConstancia, 'Asegurado':informacionAsegurado, 'observaciones':solicitudEndoso.Observaciones, 'descripcionBienes':listDescripcionBien,
                                                      'SumaAseguradaBienes':'{:10,.4f}'.format(sumaAseguradaBienes), 'montoAPagar':'{:10,.4f}'.format(montoAPagar), 'TipoEndoso':tipoEndoso,
                                                      'CantidadFletes':varCantidadFletes, 'SumaAseguradaUnitaria':'{:10,.4f}'.format(varSumaUnitaria), 'SumaAseguradaTotal':'{:10,.4f}'.format(sumaAseguradaPorDia),
                                                      'PromedioDiario':'{:,}'.format(varPromedioDiario), 'Precio':'{:,}'.format(varPrecio), 'Valor':'{:,}'.format(varExistencia), 
                                                      'TarifaMensual':'{:,}'.format(varTarifaMensual), 'Cuota':'{:10,.4f}'.format(varCuota), 'CuotaAnual':varCuotaAnual, 'DiasDevengados':diasDevengados,
                                                      'DiasTotales':diasTotales,'Porcentaje':(str(int(porcentaje)) + ' %'), 'usuario':request.user}, context_instance = RequestContext(request))

@login_required()
def reporte_endoso_cancelacion(request, id_endoso): #Vista que genera la informacion para mostrar el reporte del endoso de cancelacion pasando el id del endoso de cancelacion.
    
    sumaAseguradaBienes = 0
    montoAPagar = 0
    countRow = 0
    sumaAsegurada = 0
    listDescripcionBien = list()
    tipoEndoso = ''
    
    # Variables para mostrar los totales del endoso de transporte.
    varCantidadFletes = 0
    varSumaUnitaria = 0
    sumaAseguradaPorDia = 0
    
    # Variables para mostrar los totales del endoso declaracion.
    varPromedioDiario = 0
    varPrecio = 0
    varExistencia = 0
    varTarifaMensual = 0
    varCuota = 0
    
    # Variables para constancias anuales.
    varCuotaAnual = 0
    diasDevengados = 0
    diasTotales = 0
    porcentaje = 0
    
    endosoCancelacion = EndosoCancelacion.objects.filter(IdEndosoCancelacion = id_endoso)[0]
    
    if endosoCancelacion:
         
        cursor = connections['siobicx'].cursor() # Se busca la constancia a para mostrar la informacion en el reporte del endoso de cancelacion.
        sql_string = 'SELECT * FROM vconstanciascanceladas Where NoConstancia = ' + str(endosoCancelacion.Constancia_id)
        cursor.execute(sql_string)
        datosConstancia = cursor.fetchall()
        
        if datosConstancia:
            informacionAsegurado = ajax.datosPersona(datosConstancia[0][11])      
            descripcionBien = DescripcionBienEndosoAD.objects.filter(Constancia_id = datosConstancia[0][0])
            
            if not descripcionBien:
                    relacionanexa = RelacionAnexaActaVerificacion.objects.filter(Solicitud_id = datosConstancia[0][12])[0]
                    descripcionBien = DescripcionBienActaVerificacion.objects.filter(RelacionAnexaActaVerificacion_id = relacionanexa.IdRelacionAnexaActaVerificacion)   
                    
            for bienes in descripcionBien:
                valorUnitario = '{:10,.4f}'.format(bienes.ValorUnitario)
                sumaAsegurada = bienes.Cantidad * bienes.ValorUnitario
                sumaAseguradaBienes = sumaAseguradaBienes + (bienes.Cantidad * bienes.ValorUnitario)
                listDescripcionBien.append({'NombreEquipo':bienes.NombreEquipo,'Marca':bienes.Marca,'Modelo':bienes.Modelo,'Serie':bienes.Serie, 'DocumentacionEvaluacion':bienes.DocumentacionEvaluacion,
                                          'FechaBien':bienes.FechaBien,'Cantidad':'{:,}'.format(bienes.Cantidad),'ValorUnitario':valorUnitario,'SumaAsegurada':'{:10,.4f}'.format(sumaAsegurada)})
               
            if datosConstancia[0][13] == 'A DECLARACIÓN': # Se busca si la constancia es a declaración.
                varEndosoDeclaracion = DeclaracionEndoso.objects.filter(Constancia_id = datosConstancia[0][0]).order_by('-IdDeclaracionEndoso')
                        
                if varEndosoDeclaracion: # Checa si la constancia es a endoso de declaracion.
                    varEndosoDeclaracionPorDia = DeclaracionEndosoPorDia.objects.filter(DeclaracionEndoso_id = varEndosoDeclaracion[0].IdDeclaracionEndoso)
                       
                    for endosoPorDia in varEndosoDeclaracionPorDia:
                        varPromedioDiario = varPromedioDiario + endosoPorDia.Existencia
                        varPrecio = varPrecio + endosoPorDia.Precio
                        varExistencia = varExistencia + endosoPorDia.Valor
                        varTarifaMensual = varTarifaMensual + endosoPorDia.TarifaMensual
                        varCuota = varCuota + endosoPorDia.TarifaDiaria
                        countRow = countRow + 1
                    
                    varPromedioDiario = varPromedioDiario / countRow
                    varPrecio = varPrecio / countRow
                    varExistencia = varExistencia / countRow
                    varTarifaMensual = varTarifaMensual / countRow
                    varCuota = varCuota / countRow
                    
                    if datosConstancia[0][14] == 1:
                        prima = 1000
                    else:
                        prima = 100
                    
                    montoAPagar = (varExistencia * varCuota) / prima
                    tipoEndoso = 'DD'    
                        
                else: # Si la constancia no es a endoso de declaracion entonces es a endoso de transporte.
                    montoAPagar = 0
                    countRow = 0
                    varEndosoTransporte = DeclaracionTransporte.objects.filter(Constancia_id = datosConstancia[0][0]).order_by('-IdDeclaracionTransporte')   
                    
                    if varEndosoTransporte:
                        varEndosoTransportePorDia = DeclaracionTransportePorUnidad.objects.filter(DeclaracionTransporte_id = varEndosoTransporte[0].IdDeclaracionTransporte)                
                    
                        if datosConstancia[0][14] == 1:
                            prima = 1000
                        else:
                            prima = 100
                        
                        for endosoPorDia in varEndosoTransportePorDia:
                            varCantidadFletes = varCantidadFletes + endosoPorDia.Cantidad
                            varSumaUnitaria = varSumaUnitaria + endosoPorDia.SumaAseguradaUnitaria
                            sumaAseguradaPorDia = sumaAseguradaPorDia + endosoPorDia.SumaAseguradaTotal
                            countRow = countRow + 1
                            
                        tipoEndoso = 'DT'
                        varSumaUnitaria = varSumaUnitaria / countRow
                        montoAPagar = (sumaAseguradaPorDia * datosConstancia[0][15]) / prima
            else:
                
                periodoPago = PeriodoPagoCuotaAnual.objects.all()
                
                tipoEndoso = 'CA'
                vigenciaInicio = datetime.strptime(datosConstancia[0][5], '%d/%m/%Y')
                vigenciaFin = datetime.strptime(datosConstancia[0][6], '%d/%m/%Y')
                fechaActual = datetime.now()
                diasDevengados = (fechaActual - vigenciaInicio).days + 1
                diasTotales = (vigenciaFin - vigenciaInicio).days
                varCuotaAnual = datosConstancia[0][16]
                
                if periodoPago:                    
                    for periodo in periodoPago:
                        if diasDevengados >= periodo.DiasDesde and diasDevengados <= periodo.DiasHasta:
                            porcentaje = periodo.Porcentaje
                            break;
                        
                    montoAPagar = (float(varCuotaAnual) * int(porcentaje)) / 100
                else:
                    montoAPagar = 0    
    
    html = render_to_string('reporteendosocancelacion.html',{'datosConstancia':datosConstancia, 'Asegurado':informacionAsegurado, 'descripcionBienes':listDescripcionBien,
                                                      'SumaAseguradaBienes':'{:10,.4f}'.format(sumaAseguradaBienes), 'montoAPagar':'{:10,.4f}'.format(montoAPagar), 'TipoEndoso':tipoEndoso,
                                                      'CantidadFletes':varCantidadFletes, 'SumaAseguradaUnitaria':'{:10,.4f}'.format(varSumaUnitaria), 'SumaAseguradaTotal':'{:10,.4f}'.format(sumaAseguradaPorDia),
                                                      'Cuota':'{:10,.4f}'.format(0), 'PromedioDiario':'{:,}'.format(varPromedioDiario), 'Precio':'{:,}'.format(varPrecio), 'Valor':'{:,}'.format(varExistencia), 
                                                      'TarifaMensual':'{:,}'.format(varTarifaMensual), 'Cuota':'{:10,.4f}'.format(varCuota), 'CuotaAnual':'{:10,.4f}'.format(varCuotaAnual), 'DiasDevengados':diasDevengados,
                                                      'DiasTotales':diasTotales,'Porcentaje':(str(int(porcentaje)) + ' %'), 'usuario':request.user}, context_instance = RequestContext(request))
    return generar_pdf(html)