# Create your views here.
from Solicitud.forms import SolicitudForm, RelacionAnexaSolicitudForm, DescripcionDetalladaBienSolicitadoForm, ActaVerificacionSolicitudForm, MedidaSeguridadActaVerificacionForm
from django.shortcuts import render, get_object_or_404
from Solicitud.models import Solicitud, Beneficiario, RelacionAnexaSolicitud, DescripcionDetalladaBienSolicitado, ActaVerificacionSolicitud, MedidaSeguridadActaVerificacion, RelacionAnexaActaVerificacion, DescripcionBienActaVerificacion 
from Solicitud import ajax
from Programas.models import Programa, TipoSeguro, SubTipoSeguro, CoberturaPrograma, Cobertura, AreaInfluenciaPrograma
from ConexosAgropecuarios.models import ContratoFondo, AreaInfluencia, Municipio, Moneda
from Constancias.models import Constancia
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required()
def reporteRelacionAnexaActaVerificacion(request,id_Solicitud):
    informacionSolicitud = get_object_or_404(Solicitud, IdSolicitud=id_Solicitud)
    informacionAsegurado = ajax.datosPersona(informacionSolicitud.PersonaAsegurada_id)
    informacionContratante = ajax.datosPersona(informacionSolicitud.PersonaContratante_id)    
    informacionRelacionAnexaActaVerificacion = RelacionAnexaActaVerificacion.objects.filter(Solicitud_id = id_Solicitud)[0]
    date = datetime.now()
    sumaAseguradaBienes = 0
    listDescripcionBienes = list()
    informacionDescripcionBienes = DescripcionBienActaVerificacion.objects.filter(RelacionAnexaActaVerificacion_id = informacionRelacionAnexaActaVerificacion.IdRelacionAnexaActaVerificacion)

    for bienes in informacionDescripcionBienes:
        valorUnitario = '{:10,.2f}'.format(bienes.ValorUnitario)
        sumaAsegurada = '{:10,.2f}'.format(bienes.Cantidad * bienes.ValorUnitario)
        sumaAseguradaBienes = sumaAseguradaBienes + (bienes.Cantidad * bienes.ValorUnitario) 
        listDescripcionBienes.append({'NombreEquipo':bienes.NombreEquipo,'Marca':bienes.Marca,'Modelo':bienes.Modelo,'Serie':bienes.Serie, 'DocumentacionEvaluacion':bienes.DocumentacionEvaluacion,
                                      'FechaBien':bienes.FechaBien,'Cantidad':bienes.Cantidad,'ValorUnitario':valorUnitario,'SumaAsegurada':sumaAsegurada})
            
    return render(request, 'reporterelacionanexaactaverificacion.html',{'InformacionSolicitud':informacionSolicitud,'FechaActual':date,'InformacionRelacionAnexaAV':informacionRelacionAnexaActaVerificacion,
                                                                        'Asegurado':informacionAsegurado,'Contratante':informacionContratante,'DescripcionBienes':listDescripcionBienes,
                                                                        'SumaAseguradaBienes':'{:10,.2f}'.format(sumaAseguradaBienes), 'usuario':request.user})

@login_required()
def listaActasVerificacionRechazadas(request): #Listado de las actas de verificacion que tuvieron un dictamen negativo
    return render(request, 'listaactasverificacionrechazadas.html', {'usuario':request.user}) 

@login_required()
def listaActasVerificacion(request): #Listado para generar las actas de verificacion con su relacion anexa
    return render(request, 'listaactasverificacion.html', {'usuario':request.user})

@login_required()
def solicitudes(request): #Vista para listasolicitudes.html
    return render(request, 'listasolicitudes.html', {'usuario':request.user})

@login_required()
def solicitud(request): #vista para la solicitud.html
    return render(request, 'solicitud.html', {'formulario_solicitud':SolicitudForm(auto_id='%s'),'usuario':request.user})

@login_required()
def relacionAnexaActaVerificacion(request,id_Solicitud): #vista para la relacion anexa al acta de verificacion
    informacionSolicitud = Solicitud.objects.filter(IdSolicitud = id_Solicitud)[0]  #get_object_or_404(Solicitud, IdSolicitud=id_Solicitud)
    informacionAsegurado = ajax.datosPersona(informacionSolicitud.PersonaAsegurada_id)
    informacionContratante = ajax.datosPersona(informacionSolicitud.PersonaContratante_id)
    informacionBeneficiarios = Beneficiario.objects.filter(Solicitud_id = id_Solicitud)
    listBeneficiarios = list()
    for beneficiario in informacionBeneficiarios:
        datosBeneficiario = ajax.datosPersona(beneficiario.PersonaBeneficiario_id)
        listBeneficiarios.append({'NombrePersonaBeneficiario':datosBeneficiario[0]['NombrePersona'],'DomicilioPersonaBeneficiario':datosBeneficiario[0]['DireccionPersona'],'RfcPersonaBeneficiario':datosBeneficiario[0]['RfcPersona']})

    sumaAseguradaSolicitada = informacionSolicitud.Unidades * informacionSolicitud.ValorUnidad
    programa = Programa.objects.filter(IdPrograma = informacionSolicitud.Programa_id)[0]
    tipoSeguro = TipoSeguro.objects.using('catalogos').filter(IdTipoSeguro = programa.IdTipoSeguro)[0]
    subTipoSeguro = SubTipoSeguro.objects.using('catalogos').filter(IdSubTipoSeguro = programa.IdSubTipoSeguro)[0]
    contrato = ContratoFondo.objects.filter(IdContratoFondo = programa.IdContratoFondo)[0]
    descripcionMoneda = Moneda.objects.using('catalogos').filter(IdMoneda = programa.IdTipoMoneda)[0]

    # Se obtiene aparte las observaciones del solicitante porque en la relacion anexa al acta de verificacion no se guardan
    informacionRelacionAnexa = RelacionAnexaSolicitud.objects.filter(Solicitud_id = id_Solicitud)[0]
    observacionesSolicitante = informacionRelacionAnexa.ObservacionesSolicitante
    
    informacionRelacionAnexaActaVerificacion = RelacionAnexaActaVerificacion.objects.filter(Solicitud_id = id_Solicitud)
    
    sumaAseguradaBienes = 0
    listDescripcionBienes = list()
    if not informacionRelacionAnexaActaVerificacion: # Se compara si ya cuenta con una relacion anexa al acta de verificacion, si no tiene muestra los datos de la relacion anexa a la solicitud
        informacionRelacionAnexa = RelacionAnexaSolicitud.objects.filter(Solicitud_id = id_Solicitud)[0]
        informacionDescripcionBienes = DescripcionDetalladaBienSolicitado.objects.filter(RelacionAnexaSolicitud_id = informacionRelacionAnexa.IdRelacionAnexaSolicitud)
        for bienes in informacionDescripcionBienes:
            valorUnitario = '{:10,.2f}'.format(bienes.ValorUnitario)
            sumaAsegurada = '{:10,.2f}'.format(bienes.Cantidad * bienes.ValorUnitario)
            sumaAseguradaBienes = sumaAseguradaBienes + (bienes.Cantidad * bienes.ValorUnitario) 
            listDescripcionBienes.append({'IdBien':bienes.IdDescripcionDetalladaBienSolicitado,'NombreEquipo':bienes.NombreEquipo,'Marca':bienes.Marca,'Modelo':bienes.Modelo,'Serie':bienes.Serie, 'DocumentacionEvaluacion':bienes.DocumentacionEvaluacion,
                                      'FechaBien':bienes.FechaBien,'Cantidad':'{:,}'.format(bienes.Cantidad),'ValorUnitario':valorUnitario,'SumaAsegurada':sumaAsegurada,
                                      'CantidadOriginal':bienes.Cantidad,'ValorUnitarioOriginal':bienes.ValorUnitario})
    else: #Si ya cuenta con relacion anexa al acta de verificacion, se muestran los datos de esta relacion anexa para que se puedan modificar o volver a imprimir
        informacionRelacionAnexa = RelacionAnexaActaVerificacion.objects.filter(Solicitud_id = id_Solicitud)[0]
        informacionDescripcionBienes = DescripcionBienActaVerificacion.objects.filter(RelacionAnexaActaVerificacion_id = informacionRelacionAnexa.IdRelacionAnexaActaVerificacion)
        for bienes in informacionDescripcionBienes:
            valorUnitario = '{:10,.2f}'.format(bienes.ValorUnitario)
            sumaAsegurada = '{:10,.2f}'.format(bienes.Cantidad * bienes.ValorUnitario)
            sumaAseguradaBienes = sumaAseguradaBienes + (bienes.Cantidad * bienes.ValorUnitario)
            listDescripcionBienes.append({'IdBien':bienes.IdDescripcionBienActaVerificacion,'NombreEquipo':bienes.NombreEquipo,'Marca':bienes.Marca,'Modelo':bienes.Modelo,'Serie':bienes.Serie, 'DocumentacionEvaluacion':bienes.DocumentacionEvaluacion,
                                      'FechaBien':bienes.FechaBien,'Cantidad':'{:,}'.format(bienes.Cantidad),'ValorUnitario':valorUnitario,'SumaAsegurada':sumaAsegurada,
                                      'CantidadOriginal':bienes.Cantidad,'ValorUnitarioOriginal':bienes.ValorUnitario})
    
    #Obtencion de los nombres de los municipios para el area de influencia del programa
    areaInfluenciaPrograma = AreaInfluenciaPrograma.objects.filter(Programa_id = informacionSolicitud.Programa_id)
    listMunicipiosPrograma = list()
    for areaInfluencia in areaInfluenciaPrograma:
        areaCatalogo = AreaInfluencia.objects.filter(IdAreaInfluencia = areaInfluencia.IdAreaInfluencia)
        if areaCatalogo: #Si se encuentra el area de influencia del programa en el catalogo del area de influencia
            municipio = Municipio.objects.using('catalogos').filter(IdMunicipio = areaCatalogo[0].Municipio_id)[0]
            listMunicipiosPrograma.append({'Descripcion':municipio.Descripcion})
    
    #Buscamos si ya cuenta con constancia para quitar la opcion de modificar la constancia
    tieneConstancia = False
    constancia = Constancia.objects.filter(Solicitud_id=id_Solicitud)
    if constancia:
        tieneConstancia = True
    
    return render(request, 'relacionanexaactaverificacion.html', {'InformacionSolicitud':informacionSolicitud,'Asegurado':informacionAsegurado, 'Contratante':informacionContratante, 'Beneficiarios':listBeneficiarios,
                                                                  'SumaAseguradaSolicitada':sumaAseguradaSolicitada, 'TipoSeguro': tipoSeguro.DescripcionTipoSeguro, 'SubTipoSeguro': subTipoSeguro.DescripcionSubTipoSeguro,
                                                                  'NumeroContrato':contrato.NumeroContrato, 'Ejercicio':programa.Ejercicio, 'FolioPrograma':programa.FolioPrograma, 'Moneda':descripcionMoneda.Descripcion,
                                                                  'informacionRelacionAnexa':informacionRelacionAnexa, 'DescripcionBienes':listDescripcionBienes, 'formulario_descripcion_bien':DescripcionDetalladaBienSolicitadoForm(auto_id='%s'),
                                                                  'SumaAseguradaBienes':'{:10,.2f}'.format(sumaAseguradaBienes),'ObservacionesSolicitante':observacionesSolicitante,'MunicipiosProgramas':listMunicipiosPrograma,
                                                                  'usuario':request.user,'TieneConstancia':tieneConstancia})

@login_required()
def actaVerificacion(request,id_Solicitud): #Vista para el acta de verificacion donde recibe el id del socio y muestra toda la informacion de la solicitud
    informacionSolicitud = get_object_or_404(Solicitud, IdSolicitud=id_Solicitud)
    informacionAsegurado = ajax.datosPersona(informacionSolicitud.PersonaAsegurada_id)
    informacionContratante = ajax.datosPersona(informacionSolicitud.PersonaContratante_id)
    informacionBeneficiarios = Beneficiario.objects.filter(Solicitud_id = id_Solicitud)
    informacionActaVerificacion = ActaVerificacionSolicitud.objects.filter(Solicitud_id = id_Solicitud)
    informacionMedidaSeguridad = ''
    if not informacionActaVerificacion:
        informacionActaVerificacion =''
    else:
        informacionActaVerificacion = ActaVerificacionSolicitud.objects.filter(Solicitud_id = id_Solicitud)[0]
        informacionMedidaSeguridad = MedidaSeguridadActaVerificacion.objects.filter(ActaVerificacionSolicitud_id = informacionActaVerificacion.IdActaVerificacionSolicitud)
            
    listBeneficiarios = list()
    listDescripcionBienes = list()
    sumaAseguradaBienes = 0
    for beneficiario in informacionBeneficiarios:
        datosBeneficiario = ajax.datosPersona(beneficiario.PersonaBeneficiario_id)
        listBeneficiarios.append({'NombrePersonaBeneficiario':datosBeneficiario[0]['NombrePersona'],'DomicilioPersonaBeneficiario':datosBeneficiario[0]['DireccionPersona'],'RfcPersonaBeneficiario':datosBeneficiario[0]['RfcPersona']})
        
    programa = Programa.objects.filter(IdPrograma = informacionSolicitud.Programa_id)[0]
    tipoSeguro = TipoSeguro.objects.using('catalogos').filter(IdTipoSeguro = programa.IdTipoSeguro)[0]
    subTipoSeguro = SubTipoSeguro.objects.using('catalogos').filter(IdSubTipoSeguro = programa.IdSubTipoSeguro)[0]
    contrato = ContratoFondo.objects.filter(IdContratoFondo = programa.IdContratoFondo)[0]
    descripcionMoneda = Moneda.objects.using('catalogos').filter(IdMoneda = programa.IdTipoMoneda)[0]
    informacionRelacionAnexa = RelacionAnexaSolicitud.objects.filter(Solicitud_id = id_Solicitud)[0]
    informacionDescripcionBienes = DescripcionDetalladaBienSolicitado.objects.filter(RelacionAnexaSolicitud_id = informacionRelacionAnexa.IdRelacionAnexaSolicitud)
    for bienes in informacionDescripcionBienes:
        valorUnitario = '{:10,.2f}'.format(bienes.ValorUnitario)
        sumaAsegurada = '{:10,.2f}'.format(bienes.Cantidad * bienes.ValorUnitario)
        sumaAseguradaBienes = sumaAseguradaBienes + (bienes.Cantidad * bienes.ValorUnitario) 
        listDescripcionBienes.append({'IdDescripcionDetalladaBienSolicitado':bienes.IdDescripcionDetalladaBienSolicitado,'NombreEquipo':bienes.NombreEquipo,'Marca':bienes.Marca,'Modelo':bienes.Modelo,'Serie':bienes.Serie, 'DocumentacionEvaluacion':bienes.DocumentacionEvaluacion,
                                      'FechaBien':bienes.FechaBien,'Cantidad':bienes.Cantidad,'ValorUnitario':valorUnitario,'SumaAsegurada':sumaAsegurada})
      
    coberturasProgramas = CoberturaPrograma.objects.filter(Programa_id = informacionSolicitud.Programa_id)
    listCoberturasProgramas = list()
    
    for coberturaPrograma in coberturasProgramas:
            coberturaCatalogo = Cobertura.objects.using('catalogos').filter(IdCobertura = coberturaPrograma.IdCobertura)[0]
            listCoberturasProgramas.append({'Descripcion':coberturaCatalogo.Descripcion})
            
    sumaAseguradaSolicitada = informacionSolicitud.Unidades * informacionSolicitud.ValorUnidad
    
    return render(request, 'actaverificacion.html', {'InformacionSolicitud':informacionSolicitud,'Asegurado':informacionAsegurado,'Contratante':informacionContratante,'Beneficiarios':listBeneficiarios,
                                                     'TipoSeguro': tipoSeguro.DescripcionTipoSeguro, 'SubTipoSeguro': subTipoSeguro.DescripcionSubTipoSeguro, 'Moneda':descripcionMoneda.Descripcion,'Ejercicio':programa.Ejercicio,
                                                     'NumeroContrato':contrato.NumeroContrato, 'FolioPrograma':programa.FolioPrograma, 'Coberturas':listCoberturasProgramas, 'SumaAseguradaSolicitada':sumaAseguradaSolicitada,
                                                     'informacionRelacionAnexa':informacionRelacionAnexa, 'DescripcionBienes':listDescripcionBienes, 'formulario_acta_verificacion':ActaVerificacionSolicitudForm(auto_id='%s'),
                                                     'formulario_medidas_seguridad':MedidaSeguridadActaVerificacionForm(auto_id='%s'),'informacionActaVerificacion':informacionActaVerificacion,
                                                     'informacionMedidaSeguridad':informacionMedidaSeguridad,'usuario':request.user})

@login_required()    
def reporteActaVerificacion(request,id_Solicitud):
    date = datetime.now()
    
    informacionSolicitud = get_object_or_404(Solicitud, IdSolicitud=id_Solicitud)
    informacionAsegurado = ajax.datosPersona(informacionSolicitud.PersonaAsegurada_id)
    informacionContratante = ajax.datosPersona(informacionSolicitud.PersonaContratante_id)
    informacionActaVerificacion = ActaVerificacionSolicitud.objects.filter(Solicitud_id = id_Solicitud)
    informacionMedidaSeguridad = ''
    if not informacionActaVerificacion:
        informacionActaVerificacion =''
    else:
        informacionActaVerificacion = ActaVerificacionSolicitud.objects.filter(Solicitud_id = id_Solicitud)[0]
        informacionMedidaSeguridad = MedidaSeguridadActaVerificacion.objects.filter(ActaVerificacionSolicitud_id = informacionActaVerificacion.IdActaVerificacionSolicitud)
       
    return render(request, 'reporteactaverificacion.html', {'InformacionSolicitud':informacionSolicitud,'Asegurado':informacionAsegurado,'Contratante':informacionContratante,
                                                     'formulario_acta_verificacion':ActaVerificacionSolicitudForm(auto_id='%s'),
                                                     'formulario_medidas_seguridad':MedidaSeguridadActaVerificacionForm(auto_id='%s'),'informacionActaVerificacion':informacionActaVerificacion,
                                                     'informacionMedidaSeguridad':informacionMedidaSeguridad, 'FechaActual':date,'usuario':request.user})

@login_required()
def reporteSolicitud(request):
    return render(request, 'reportesolicitud.html',{'usuario':request.user})

@login_required()
def relacionAnexaSolicitudAseguramiento(request,id_Solicitud): #Vista para la generacion de la relacion anexa, se consulta toda la informacion para enviarla a la plantilla relacionanexasolicitud.html
    informacionSolicitud = get_object_or_404(Solicitud, IdSolicitud=id_Solicitud)
    informacionAsegurado = ajax.datosPersona(informacionSolicitud.PersonaAsegurada_id)
    informacionContratante = ajax.datosPersona(informacionSolicitud.PersonaContratante_id)
    informacionBeneficiarios = Beneficiario.objects.filter(Solicitud_id = id_Solicitud)
    listDescripcionBienes = list()
    sumaAseguradaBienes = 0
    informacionRelacionAnexa = RelacionAnexaSolicitud.objects.filter(Solicitud_id = id_Solicitud)
    if not informacionRelacionAnexa:
        informacionRelacionAnexa =''
    else:
        informacionRelacionAnexa = RelacionAnexaSolicitud.objects.filter(Solicitud_id = id_Solicitud)[0]
        informacionDescripcionBienes = DescripcionDetalladaBienSolicitado.objects.filter(RelacionAnexaSolicitud_id = informacionRelacionAnexa.IdRelacionAnexaSolicitud)
        for bienes in informacionDescripcionBienes:
            valorUnitario = '{:10,.2f}'.format(bienes.ValorUnitario)
            sumaAsegurada = '{:10,.2f}'.format(bienes.Cantidad * bienes.ValorUnitario)
            sumaAseguradaBienes = sumaAseguradaBienes + (bienes.Cantidad * bienes.ValorUnitario) 
            listDescripcionBienes.append({'IdDescripcionDetalladaBienSolicitado':bienes.IdDescripcionDetalladaBienSolicitado,'NombreEquipo':bienes.NombreEquipo,'Marca':bienes.Marca,'Modelo':bienes.Modelo,'Serie':bienes.Serie, 'DocumentacionEvaluacion':bienes.DocumentacionEvaluacion,
                                          'FechaBien':bienes.FechaBien,'Cantidad':'{:,}'.format(bienes.Cantidad),'ValorUnitario':valorUnitario,'SumaAsegurada':sumaAsegurada})
        
    programa = Programa.objects.filter(IdPrograma = informacionSolicitud.Programa_id)[0]
    tipoSeguro = TipoSeguro.objects.using('catalogos').filter(IdTipoSeguro = programa.IdTipoSeguro)[0]    
    subTipoSeguro = SubTipoSeguro.objects.using('catalogos').filter(IdSubTipoSeguro = programa.IdSubTipoSeguro)[0]
    contrato = ContratoFondo.objects.filter(IdContratoFondo = programa.IdContratoFondo)[0]
    descripcionMoneda = Moneda.objects.using('catalogos').filter(IdMoneda = programa.IdTipoMoneda)[0]
    
    listBeneficiarios = list()    
    for beneficiario in informacionBeneficiarios:
        datosBeneficiario = ajax.datosPersona(beneficiario.PersonaBeneficiario_id)
        listBeneficiarios.append({'NombrePersonaBeneficiario':datosBeneficiario[0]['NombrePersona'],'DomicilioPersonaBeneficiario':datosBeneficiario[0]['DireccionPersona'],'RfcPersonaBeneficiario':datosBeneficiario[0]['RfcPersona']})
    
    coberturasProgramas = CoberturaPrograma.objects.filter(Programa_id = informacionSolicitud.Programa_id)
    listCoberturasProgramas = list()
    for coberturaPrograma in coberturasProgramas:
        coberturaCatalogo = Cobertura.objects.using('catalogos').filter(IdCobertura = coberturaPrograma.IdCobertura)[0]
        listCoberturasProgramas.append({'Descripcion':coberturaCatalogo.Descripcion})
            
    #Obtencion de los nombres de los municipios para el area de influencia del programa
    areaInfluenciaPrograma = AreaInfluenciaPrograma.objects.filter(Programa_id = informacionSolicitud.Programa_id)
    listMunicipiosPrograma = list()
    for areaInfluencia in areaInfluenciaPrograma:
        areaCatalogo = AreaInfluencia.objects.filter(IdAreaInfluencia = areaInfluencia.IdAreaInfluencia)
        if areaCatalogo: #Si se encuentra el area de influencia del programa en el catalogo del area de influencia
            municipio = Municipio.objects.using('catalogos').filter(IdMunicipio = areaCatalogo[0].Municipio_id)[0]
            listMunicipiosPrograma.append({'Descripcion':municipio.Descripcion})
    
    sumaAseguradaSolicitada = informacionSolicitud.Unidades * informacionSolicitud.ValorUnidad
    restanteSumaAseguradaBienes = sumaAseguradaSolicitada - sumaAseguradaBienes


    actaVerificacion = ActaVerificacionSolicitud.objects.filter(Solicitud_id = id_Solicitud)
    if actaVerificacion: 
        tieneActaVerificacion = True
    else:
        tieneActaVerificacion = False
    
    return render(request, 'relacionanexasolicitud.html', {'InformacionSolicitud':informacionSolicitud,'Asegurado':informacionAsegurado,'Contratante':informacionContratante, 'Beneficiarios':listBeneficiarios,
                                                           'TipoSeguro': tipoSeguro.DescripcionTipoSeguro, 'SubTipoSeguro': subTipoSeguro.DescripcionSubTipoSeguro,'Moneda':descripcionMoneda.Descripcion,'Ejercicio':programa.Ejercicio,
                                                           'NumeroContrato':contrato.NumeroContrato,'FolioPrograma':programa.FolioPrograma, 'Coberturas':listCoberturasProgramas, 'SumaAseguradaSolicitada':sumaAseguradaSolicitada,
                                                           'formulario_relacion_anexa':RelacionAnexaSolicitudForm(auto_id='%s'), 'formulario_descripcion_bien':DescripcionDetalladaBienSolicitadoForm(auto_id='%s'),
                                                           'informacionRelacionAnexa':informacionRelacionAnexa,'DescripcionBienes':listDescripcionBienes,'SumaAseguradaBienes':'{:10,.2f}'.format(sumaAseguradaBienes),
                                                           'RestanteSumaAseguradaBienes':'{:10,.2f}'.format(restanteSumaAseguradaBienes),'MunicipiosProgramas':listMunicipiosPrograma,
                                                           'usuario':request.user,'TieneActaVerificacion':tieneActaVerificacion})
      
@login_required()
def reporteRelacionAnexaSolicitudAseguramiento(request,id_Solicitud): #Vista para la generacion de la relacion anexa, se consulta toda la informacion para enviarla a la plantilla relacionanexasolicitud.html
    date = datetime.now()
    
    informacionSolicitud = get_object_or_404(Solicitud, IdSolicitud=id_Solicitud)
    informacionAsegurado = ajax.datosPersona(informacionSolicitud.PersonaAsegurada_id)
    informacionContratante = ajax.datosPersona(informacionSolicitud.PersonaContratante_id)
    listDescripcionBienes = list()
    sumaAseguradaBienes = 0
    informacionRelacionAnexa = RelacionAnexaSolicitud.objects.filter(Solicitud_id = id_Solicitud)
    programa = Programa.objects.filter(IdPrograma = informacionSolicitud.Programa_id)[0]
    descripcionMoneda = Moneda.objects.using('catalogos').filter(IdMoneda = programa.IdTipoMoneda)[0]
    
    if not informacionRelacionAnexa:
        informacionRelacionAnexa =''
        
    else:
        informacionRelacionAnexa = RelacionAnexaSolicitud.objects.filter(Solicitud_id = id_Solicitud)[0]
        informacionDescripcionBienes = DescripcionDetalladaBienSolicitado.objects.filter(RelacionAnexaSolicitud_id = informacionRelacionAnexa.IdRelacionAnexaSolicitud)
        for bienes in informacionDescripcionBienes:
            valorUnitario = '{:10,.2f}'.format(bienes.ValorUnitario)
            sumaAsegurada = '{:10,.2f}'.format(bienes.Cantidad * bienes.ValorUnitario)
            sumaAseguradaBienes = sumaAseguradaBienes + (bienes.Cantidad * bienes.ValorUnitario)
            listDescripcionBienes.append({'NombreEquipo':bienes.NombreEquipo,'Marca':bienes.Marca,'Modelo':bienes.Modelo,'Serie':bienes.Serie, 'DocumentacionEvaluacion':bienes.DocumentacionEvaluacion,
                                          'FechaBien':bienes.FechaBien,'Cantidad':bienes.Cantidad,'ValorUnitario':valorUnitario,'SumaAsegurada':sumaAsegurada})

    sumaAseguradaSolicitada = informacionSolicitud.Unidades * informacionSolicitud.ValorUnidad
    
    return render(request, 'reporterelacionanexa.html', {'InformacionSolicitud':informacionSolicitud,'Asegurado':informacionAsegurado,'Contratante':informacionContratante,
                                                           'SumaAseguradaSolicitada':sumaAseguradaSolicitada, 'formulario_relacion_anexa':RelacionAnexaSolicitudForm(auto_id='%s'), 
                                                           'formulario_descripcion_bien':DescripcionDetalladaBienSolicitadoForm(auto_id='%s'),'Moneda':descripcionMoneda.Descripcion,'Ejercicio':programa.Ejercicio,
                                                           'informacionRelacionAnexa':informacionRelacionAnexa,'DescripcionBienes':listDescripcionBienes,'SumaAseguradaBienes':'{:10,.2f}'.format(sumaAseguradaBienes),
                                                           'FechaActual':date,'usuario':request.user})