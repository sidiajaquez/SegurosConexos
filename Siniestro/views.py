from django.shortcuts import render, get_object_or_404, render_to_response
from datetime import datetime
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from Constancias.models import Constancia
from Solicitud.models import Solicitud, RelacionAnexaActaVerificacion,DescripcionBienActaVerificacion, ActaVerificacionSolicitud
from Programas.models import Programa, TipoSeguro, SubTipoSeguro,\
    CoberturaPrograma, Cobertura
from ConexosAgropecuarios.models import Persona,PersonalApoyo, Moneda
from Siniestro.models import AvisoSiniestro, BienAfectadoAviosoSiniestro, CausaSiniestro, Inspeccion, ActaSiniestro, BienActaSiniestro,\
    ImagenSiniestro,Improcedencia
from Endoso.models import DescripcionBienEndosoAD
from django.template import RequestContext
from django.template.loader import render_to_string
from ConexosAgropecuarios.pdf import generar_pdf
from django.db import connections
import json
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from django.core import serializers
from decimal import Decimal
from Cotizador.models import Cotizador, CotizadorCobertura

def guardarDictamenSiniestro(request): #Metodo para guardar el dictamen de los siniestros, se regresa el folio generado
    if request.is_ajax(): #Se utiliza el request ajax para evitar entrar por get a la pagina solicitada
        if request.POST['data']:
            return HttpResponse (json.dumps({'nada':'prueba'}), content_type="application/json; charset=utf8")
    else:
        raise Http404

@login_required()
def dictamenSiniestro(request,id_ActaSiniestro): # Vista para la generacion del dictamen del siniestro, tambien utilizada para guardar las imagenes de los siniestros
    if request.method == 'POST':
        new_file = ImagenSiniestro(Imagen=request.FILES['file'],Thumbnail=request.FILES['file'],DateAdded = datetime.now())
        new_file.save()
        
        return HttpResponseRedirect(reverse('Siniestro:DictamenSiniestro', kwargs={'id_ActaSiniestro':id_ActaSiniestro}))
    else:
        #Obtenemos los datos del acta de siniestro
        informacionActaSiniestro = get_object_or_404(ActaSiniestro, IdActaSiniestro = id_ActaSiniestro)
        #Datos de la Inspeccion del Siniestro
        informacionInspeccionSiniestro = Inspeccion.objects.get(IdInspeccion = informacionActaSiniestro.Inspeccion_id)
        #Datos del aviso de siniestro
        informacionAvisoSiniestro = AvisoSiniestro.objects.get(IdAvisoSiniestro = informacionInspeccionSiniestro.AvisoSiniestro_id)
        #se obtiene todos los bienes afectados segun acta de siniestro
        bienesActaSiniestro = BienActaSiniestro.objects.filter(ActaSiniestro = id_ActaSiniestro)
        #Personal Asignada
        personaAsignada = PersonalApoyo.objects.get(IdPersonalApoyo = informacionInspeccionSiniestro.PersonalApoyo_id)
        #Datos de la Constancia
        constancia = Constancia.objects.get(IdConstancia = informacionInspeccionSiniestro.Constancia_id)
        #Datos de la Solicitud
        solicitud = Solicitud.objects.get(IdSolicitud = constancia.Solicitud_id)
        #Longitud y Latitud
        relacionAnexaActaVerificacion = RelacionAnexaActaVerificacion.objects.get(Solicitud_id = solicitud.IdSolicitud)
        #Datos del programa de la constancia
        programa = Programa.objects.get(IdPrograma = solicitud.Programa_id)
        #Tipo de seguro
        tipoSeguro = TipoSeguro.objects.using('catalogos').get(IdTipoSeguro = programa.IdTipoSeguro)
        #Subtipo de seguro
        subTipoSeguro = SubTipoSeguro.objects.using('catalogos').get(IdSubTipoSeguro = programa.IdSubTipoSeguro)
        #Moneda de la constancia
        moneda = Moneda.objects.using('catalogos').get(IdMoneda = programa.IdTipoMoneda)
        #Se envia el catalogo de improcedencias
        Improcedencias = Improcedencia.objects.using('catalogos').all()
        return render(request, 'dictamensiniestro.html', {'usuario':request.user, 'BienesActaSiniestro':bienesActaSiniestro, 'Improcedencias':Improcedencias, 'AvisoSiniestro':informacionAvisoSiniestro,
                                                          'ActaSiniestro':informacionActaSiniestro,'Inspeccion':informacionInspeccionSiniestro,'Asignada':personaAsignada.Persona.PrimerNombre + " " + personaAsignada.Persona.SegundoNombre + " " + personaAsignada.Persona.ApellidoPaterno + " " + personaAsignada.Persona.ApellidoMaterno,
                                                          'Constancia':constancia,'Asegurado':solicitud.PersonaAsegurada.PrimerNombre + " " + solicitud.PersonaAsegurada.SegundoNombre + " " + solicitud.PersonaAsegurada.ApellidoPaterno + " " + solicitud.PersonaAsegurada.ApellidoMaterno,
                                                          'RelacionAnexaActaVerificacion':relacionAnexaActaVerificacion,'Seguro':tipoSeguro.DescripcionTipoSeguro,'SubTipoSeguro':subTipoSeguro.DescripcionSubTipoSeguro,
                                                          'Moneda':moneda.Nombre,'Ejercicio':programa.Ejercicio,'DiaActual':datetime.now()})

@login_required()
def listaAvisoSiniestro(request): # Listado que muestra los avisos de siniestro mediante la plantilla listadoavisosiniestro.html
    return render(request, 'listadoavisosiniestro.html', {'usuario':request.user})

@login_required()
def listadoDictamenSiniestro(request): #Listado que muestra las actas de siniestro completadas para elaborar su dictaminacion
    return render(request, 'listadodictamensiniestro.html', {'usuario': request.user})

@login_required()
def avisoSiniestroNuevo(request): # Metodo que nos permite crear un nuevo aviso de siniestro mediante la plantilla avisosiniestro.html
    
    #causaSiniestro = CausaSiniestro.objects.using('catalogos').all()
    status = 0    
    
    return render(request, 'avisosiniestro.html', {'status':status, 'usuario':request.user})

@login_required()
def avisoSiniestroEditar(request, id_aviso_siniestro): # Metodo que nos permite mostrar la informacion de un aviso de siniestro para permitir editarla mediante la plantialla avisosiniestro.html
    
    tieneAumento = False
    bienesAMostrar = list()
    causaSiniestro = list()
    idBienAfectado = ''
    noBienesAfectados = ''
    estadoDanos = ''
    descripcion = ''
    
    avisoSiniestro = AvisoSiniestro.objects.filter(IdAvisoSiniestro = id_aviso_siniestro)[0]
    
    if avisoSiniestro:
        constancia = Constancia.objects.filter(IdConstancia = avisoSiniestro.Constancia_id)[0]
        
        if constancia:
            solicitud = Solicitud.objects.filter(IdSolicitud = constancia.Solicitud_id)[0]
            programa = Programa.objects.filter(IdPrograma = solicitud.Programa_id)[0]
            personaConstnacia = Persona.objects.filter(IdPersona = solicitud.PersonaAsegurada_id)[0]
            personaTecnico = Persona.objects.filter(IdPersona = avisoSiniestro.PersonaTecnico_id)[0]
            
            cotizadorEncontrado = Cotizador.objects.filter(Programa_id = programa.IdPrograma)
            
            if cotizadorEncontrado:
                cotizadorCoberturaEncontradas = CotizadorCobertura.objects.filter(Cotizador_id = cotizadorEncontrado[0].IdCotizador)
                  
                if cotizadorCoberturaEncontradas:
                    for cotizadorCobertura in cotizadorCoberturaEncontradas:                        
                        coberturaProgramaEncontrada = CoberturaPrograma.objects.filter(IdCoberturaPrograma = cotizadorCobertura.CoberturaPrograma_id)
                        
                        if coberturaProgramaEncontrada:                            
                            for cotizadorPrograma in coberturaProgramaEncontrada:
                                coberturaEncontrada = Cobertura.objects.using('catalogos').filter(IdCobertura = cotizadorPrograma.IdCobertura)
                                
                                if coberturaEncontrada:
                                    
                                    causaSiniestro.append({'IdCotizadorCobertura':cotizadorCobertura.IdCotizadorCobertura, 'Descripcion':coberturaEncontrada[0].Descripcion.upper(), 'Deducible':str(cotizadorCobertura.Deducible),
                                                           'ParticipacionAPerdida':str(cotizadorCobertura.ParticipacionAPerdida)})
            
            nombreTecnico = personaTecnico.PrimerNombre + ' ' + personaTecnico.SegundoNombre + ' ' + personaTecnico.ApellidoPaterno + ' ' + personaTecnico.ApellidoMaterno
            
            if personaConstnacia.TipoPersona == 'F':
                nombreAsegurado = personaConstnacia.PrimerNombre + ' ' + personaConstnacia.SegundoNombre + ' ' + personaConstnacia.ApellidoPaterno + ' ' + personaConstnacia.ApellidoMaterno
            else:
                nombreAsegurado = personaConstnacia.RazonSocial       
                   
            vigenciaConstancia = constancia.VigenciaInicio.strftime("%d/%m/%Y") + " al " + constancia.VigenciaFin.strftime("%d/%m/%Y")
            
            if avisoSiniestro.OtraVia == True:
                viaAviso = 'OTROS' 
                OtraVia = avisoSiniestro.ViaAviso
            else:
                viaAviso = avisoSiniestro.ViaAviso
                OtraVia = ''
                          
            descripcionesBienAD = DescripcionBienEndosoAD.objects.filter(Constancia_id = constancia.IdConstancia)
            
            if descripcionesBienAD:
                for descripcionBienAD in descripcionesBienAD: 
                    
                    tieneAumento = True
                    bienesAfectados = BienAfectadoAviosoSiniestro.objects.filter(AvisoSiniestro_id = avisoSiniestro.IdAvisoSiniestro)
                        
                    for bienAfectado in bienesAfectados:
                        if descripcionBienAD.IdDescripcionBienEndosoAD == bienAfectado.IdBienConstancia:
                            idBienAfectado = bienAfectado.IdBienAfectado
                            noBienesAfectados = bienAfectado.NumeroBienAfectado
                            estadoDanos = bienAfectado.EstadoDelDano
                            descripcion = bienAfectado.Descripcion
                            
                    sumaBien = descripcionBienAD.Cantidad * descripcionBienAD.ValorUnitario
                    bienesAMostrar.append({'IdBienAfectado':idBienAfectado, 'IdDescripcion':descripcionBienAD.IdDescripcionBienEndosoAD, 'Nombre':descripcionBienAD.NombreEquipo, 'Cantidad':'{:,}'.format(descripcionBienAD.Cantidad),
                                            'ValorUnitario':'{:,}'.format(descripcionBienAD.ValorUnitario), 'SumaAsegurada':'{:,}'.format(sumaBien), 'NoBienesAfectados':noBienesAfectados, 'EstadoDanos':estadoDanos,
                                            'Descripcion':descripcion})
                    idBienAfectado = ''
                    noBienesAfectados = ''
                    estadoDanos = ''
                    descripcion = ''
            else:
                
                relacionAnexaActaVerificacion = RelacionAnexaActaVerificacion.objects.filter(Solicitud_id = constancia.Solicitud_id)[0]
                descripcionBienActaVerificacion = DescripcionBienActaVerificacion.objects.filter(RelacionAnexaActaVerificacion_id = relacionAnexaActaVerificacion.IdRelacionAnexaActaVerificacion)
                
                for descripcionBien in descripcionBienActaVerificacion:
                    
                    bienesAfectados = BienAfectadoAviosoSiniestro.objects.filter(AvisoSiniestro_id = avisoSiniestro.IdAvisoSiniestro)
                    
                    for bienAfectado in bienesAfectados:
                        if descripcionBien.IdDescripcionBienActaVerificacion == bienAfectado.IdBienConstancia:
                            idBienAfectado = bienAfectado.IdBienAfectado
                            noBienesAfectados = bienAfectado.NumeroBienAfectado
                            estadoDanos = bienAfectado.EstadoDelDano
                            descripcion = bienAfectado.Descripcion
                    
                    sumaBien = descripcionBien.Cantidad * descripcionBien.ValorUnitario
                    bienesAMostrar.append({'IdBienAfectado':idBienAfectado, 'IdDescripcion':descripcionBien.IdDescripcionBienActaVerificacion, 'Nombre':descripcionBien.NombreEquipo, 'Cantidad':descripcionBien.Cantidad,
                                        'ValorUnitario':descripcionBien.ValorUnitario, 'SumaAsegurada':sumaBien, 'NoBienesAfectados':noBienesAfectados, 'EstadoDanos':estadoDanos,
                                        'Descripcion':descripcion})
                    
                    idBienAfectado = ''
                    noBienesAfectados = ''
                    estadoDanos = ''
                    descripcion = ''
                        
    return render(request, 'avisosiniestro.html', {'avisoSiniestro':avisoSiniestro, 'NumeroConstancia': constancia.FolioConstancia, 'Ejercicio':programa.Ejercicio, 'Vigencia':vigenciaConstancia,
                  'Asegurado':nombreAsegurado, 'NombreTecnico':nombreTecnico, 'ViaAviso':viaAviso, 'OtraVia':OtraVia, 'bienesAfectados':bienesAMostrar, 'tieneAumento':tieneAumento, 'causaSiniestro':causaSiniestro, 'status':avisoSiniestro.IdStatusAvisoSiniestro,
                  'idPrograma':programa.IdPrograma, 'usuario':request.user})
    
@login_required()
def reporte_aviso_siniestro(request, id_aviso): #Vista que nos permite generar y llenar el reporte del aviso de siniestro obteniendo los datos mediante el id del aviso.
    
    bienesAMostrar = list()
    idBienAfectado = ''
    noBienesAfectados = ''
    estadoDanos = ''
    descripcion = ''
    
    avisoSiniestro = AvisoSiniestro.objects.filter(IdAvisoSiniestro = id_aviso)[0]
    
    if avisoSiniestro:
        constancia = Constancia.objects.filter(IdConstancia = avisoSiniestro.Constancia_id)[0]
        
        if constancia:
            solicitud = Solicitud.objects.filter(IdSolicitud = constancia.Solicitud_id)[0]
            programa = Programa.objects.filter(IdPrograma = solicitud.Programa_id)[0]
            personaConstnacia = Persona.objects.filter(IdPersona = solicitud.PersonaAsegurada_id)[0]
            personaTecnico = Persona.objects.filter(IdPersona = avisoSiniestro.PersonaTecnico_id)[0]
            
            nombreTecnico = personaTecnico.PrimerNombre + ' ' + personaTecnico.SegundoNombre + ' ' + personaTecnico.ApellidoPaterno + ' ' + personaTecnico.ApellidoMaterno
            
            if personaConstnacia.TipoPersona == 'F':
                nombreAsegurado = personaConstnacia.PrimerNombre + ' ' + personaConstnacia.SegundoNombre + ' ' + personaConstnacia.ApellidoPaterno + ' ' + personaConstnacia.ApellidoMaterno
            else:
                nombreAsegurado = personaConstnacia.RazonSocial       
                   
            vigenciaConstancia = constancia.VigenciaInicio.strftime("%d/%m/%Y") + " al " + constancia.VigenciaFin.strftime("%d/%m/%Y")
            
            if avisoSiniestro.OtraVia == True:
                viaAviso = 'OTROS' 
                OtraVia = avisoSiniestro.ViaAviso
            else:
                viaAviso = avisoSiniestro.ViaAviso
                OtraVia = ''
                          
            descripcionesBienAD = DescripcionBienEndosoAD.objects.filter(Constancia_id = constancia.IdConstancia)
            
            if descripcionesBienAD:
                for descripcionBienAD in descripcionesBienAD: 
                    
                    bienesAfectados = BienAfectadoAviosoSiniestro.objects.filter(AvisoSiniestro_id = avisoSiniestro.IdAvisoSiniestro)
                        
                    for bienAfectado in bienesAfectados:
                        if descripcionBienAD.IdDescripcionBienEndosoAD == bienAfectado.IdBienConstancia:
                            idBienAfectado = bienAfectado.IdBienAfectado
                            noBienesAfectados = bienAfectado.NumeroBienAfectado
                            estadoDanos = bienAfectado.EstadoDelDano
                            descripcion = bienAfectado.Descripcion
                            
                    sumaBien = descripcionBienAD.Cantidad * descripcionBienAD.ValorUnitario
                    bienesAMostrar.append({'IdBienAfectado':idBienAfectado, 'IdDescripcion':descripcionBienAD.IdDescripcionBienEndosoAD, 'Nombre':descripcionBienAD.NombreEquipo, 'Cantidad':'{:,}'.format(descripcionBienAD.Cantidad),
                                            'ValorUnitario':'{:,}'.format(descripcionBienAD.ValorUnitario), 'SumaAsegurada':'{:,}'.format(sumaBien), 'NoBienesAfectados':noBienesAfectados, 'EstadoDanos':estadoDanos,
                                            'Descripcion':descripcion})
                    idBienAfectado = ''
                    noBienesAfectados = ''
                    estadoDanos = ''
                    descripcion = ''
            else:
                
                relacionAnexaActaVerificacion = RelacionAnexaActaVerificacion.objects.filter(Solicitud_id = constancia.Solicitud_id)[0]
                descripcionBienActaVerificacion = DescripcionBienActaVerificacion.objects.filter(RelacionAnexaActaVerificacion_id = relacionAnexaActaVerificacion.IdRelacionAnexaActaVerificacion)
                
                for descripcionBien in descripcionBienActaVerificacion:
                    
                    bienesAfectados = BienAfectadoAviosoSiniestro.objects.filter(AvisoSiniestro_id = avisoSiniestro.IdAvisoSiniestro)
                        
                    for bienAfectado in bienesAfectados:
                        if descripcionBien.IdDescripcionBienActaVerificacion == bienAfectado.IdBienConstancia:
                            idBienAfectado = bienAfectado.IdBienAfectado
                            noBienesAfectados = bienAfectado.NumeroBienAfectado
                            estadoDanos = bienAfectado.EstadoDelDano
                            descripcion = bienAfectado.Descripcion
                    
                    sumaBien = descripcionBien.Cantidad * descripcionBien.ValorUnitario
                    bienesAMostrar.append({'IdBienAfectado':idBienAfectado, 'IdDescripcion':descripcionBien.IdDescripcionBienActaVerificacion, 'Nombre':descripcionBien.NombreEquipo, 'Cantidad':descripcionBien.Cantidad,
                                        'ValorUnitario':descripcionBien.ValorUnitario, 'SumaAsegurada':sumaBien, 'NoBienesAfectados':noBienesAfectados, 'EstadoDanos':estadoDanos,
                                        'Descripcion':descripcion})
                    
                    idBienAfectado = ''
                    noBienesAfectados = ''
                    estadoDanos = ''
                    descripcion = ''
    
    html = render_to_string('reporteavisosiniestro.html',{'avisoSiniestro':avisoSiniestro, 'NumeroConstancia': constancia.FolioConstancia, 'Ejercicio':programa.Ejercicio, 'Vigencia':vigenciaConstancia,
                  'Asegurado':nombreAsegurado, 'NombreTecnico':nombreTecnico, 'ViaAviso':viaAviso, 'bienesAfectados':bienesAMostrar,'usuario':request.user}, context_instance = RequestContext(request))
    return generar_pdf(html)

@login_required()
def listadoInspecciones(request): # Listado que muestra las inspecciones de siniestro mediante la plantilla listadoinspecciones.html
    return render(request, 'listadoinspecciones.html', {'usuario':request.user})

@login_required()
def inpeccion_nueva(request): # Metodo que nos permite crear una nueva inspeccion mediante la plantilla inspeccion.html
    
    return render(request, 'inspeccion.html', {'usuario':request.user})

@login_required()
def inpeccion_editor(request, id_inspeccion): # Metodo que nos permite editar una inspeccion mediante la plantilla inspeccion.html
    
    idBienAfectado = ''
    noBienesAfectados = ''
    estadoDanos = ''
    descripcion = ''
    
    bienesAMostrar = list()    
    cursor = connections['siobicx'].cursor()
    sql_string = "SELECT * FROM vlistadoinspecciones Where IdInspeccion = " + id_inspeccion  
    cursor.execute(sql_string)
    result = cursor.fetchall()
    
    if result[0][10] == True:
        viaAviso = 'OTROS' 
        OtraVia = result[0][9]
    else:
        viaAviso = result[0][9]
        OtraVia = ''
    
    
    descripcionesBienAD = DescripcionBienEndosoAD.objects.filter(Constancia_id = result[0][0])
            
    if descripcionesBienAD:
        for descripcionBienAD in descripcionesBienAD: 
            
            bienesAfectados = BienAfectadoAviosoSiniestro.objects.filter(AvisoSiniestro_id = result[0][1])
                
            for bienAfectado in bienesAfectados:
                if descripcionBienAD.IdDescripcionBienEndosoAD == bienAfectado.IdBienConstancia:
                    idBienAfectado = bienAfectado.IdBienAfectado
                    noBienesAfectados = bienAfectado.NumeroBienAfectado
                    estadoDanos = bienAfectado.EstadoDelDano
                    descripcion = bienAfectado.Descripcion
                    
            sumaBien = descripcionBienAD.Cantidad * descripcionBienAD.ValorUnitario
            bienesAMostrar.append({'IdBienAfectado':idBienAfectado, 'IdDescripcion':descripcionBienAD.IdDescripcionBienEndosoAD, 'Nombre':descripcionBienAD.NombreEquipo, 'Cantidad':'{:,}'.format(descripcionBienAD.Cantidad),
                                    'ValorUnitario':'{:,}'.format(descripcionBienAD.ValorUnitario), 'SumaAsegurada':'{:,}'.format(sumaBien), 'NoBienesAfectados':noBienesAfectados, 'EstadoDanos':estadoDanos,
                                    'Descripcion':descripcion})
            idBienAfectado = ''
            noBienesAfectados = ''
            estadoDanos = ''
            descripcion = ''
    else:
        
        constancia = Constancia.objects.filter(IdConstancia = result[0][20])[0]
        relacionAnexaActaVerificacion = RelacionAnexaActaVerificacion.objects.filter(Solicitud_id = constancia.Solicitud_id)[0]
        descripcionBienActaVerificacion = DescripcionBienActaVerificacion.objects.filter(RelacionAnexaActaVerificacion_id = relacionAnexaActaVerificacion.IdRelacionAnexaActaVerificacion)
        
        for descripcionBien in descripcionBienActaVerificacion:
            
            bienesAfectados = BienAfectadoAviosoSiniestro.objects.filter(AvisoSiniestro_id = result[0][1])
                
            for bienAfectado in bienesAfectados:
                if descripcionBien.IdDescripcionBienActaVerificacion == bienAfectado.IdBienConstancia:
                    idBienAfectado = bienAfectado.IdBienAfectado
                    noBienesAfectados = bienAfectado.NumeroBienAfectado
                    estadoDanos = bienAfectado.EstadoDelDano
                    descripcion = bienAfectado.Descripcion
            
            sumaBien = descripcionBien.Cantidad * descripcionBien.ValorUnitario
            bienesAMostrar.append({'IdBienAfectado':idBienAfectado, 'IdDescripcion':descripcionBien.IdDescripcionBienActaVerificacion, 'Nombre':descripcionBien.NombreEquipo, 'Cantidad':descripcionBien.Cantidad,
                                'ValorUnitario':descripcionBien.ValorUnitario, 'SumaAsegurada':sumaBien, 'NoBienesAfectados':noBienesAfectados, 'EstadoDanos':estadoDanos,
                                'Descripcion':descripcion})

            idBienAfectado = ''
            noBienesAfectados = ''
            estadoDanos = ''
            descripcion = ''
                        
    return render(request, 'inspeccion.html', {'inspeccion':result, 'bienes':bienesAMostrar, 'viaAviso':viaAviso, 'otraVia':OtraVia, 'usuario':request.user})

@login_required()
def reporte_acta_siniestro(request, id_inspeccion): # Nos permite generar el reporte del acta de siniestro con la informacion obtenida de la base de datos.
    
    bienesAMostrar = list()
    
    cursor = connections['siobicx'].cursor()
    sql_string = "SELECT * FROM vactasiniestro Where IdInspeccion = " + id_inspeccion  
    cursor.execute(sql_string)
    actasiniestro = cursor.fetchall()
    numeroBienAfectado = ''
    
    bienesConstanciaEndoso = DescripcionBienEndosoAD.objects.filter(Constancia_id = actasiniestro[0][13])
        
    if bienesConstanciaEndoso:
        
        for bienConstancia in bienesConstanciaEndoso:
        
            bienesAfectados = BienAfectadoAviosoSiniestro.objects.filter(IdBienConstancia = bienConstancia.IdDescripcionBienEndosoAD)
            
            if bienesAfectados:
                numeroBienAfectado = bienesAfectados[0].NumeroBienAfectado
            
            sumaAsegurada = bienConstancia.Cantidad * bienConstancia.ValorUnitario;
            bienesAMostrar.append({'Nombre':bienConstancia.NombreEquipo, 'Cantidad':bienConstancia.Cantidad, 'SumaAseguradaUnitaria':bienConstancia.ValorUnitario, 'SumaAsegurada':sumaAsegurada,
                                   'NumeroBienesAfectados':numeroBienAfectado});
            
            numeroBienAfectado = ''
    else:
        
        relacionAnexaEncontrada = RelacionAnexaActaVerificacion.objects.filter(Solicitud_id = actasiniestro[0][12])[0]
        bienesConstancia = DescripcionBienActaVerificacion.objects.filter(RelacionAnexaActaVerificacion_id = relacionAnexaEncontrada.IdRelacionAnexaActaVerificacion)
        
        for bienConstancia in bienesConstancia:
            
            bienesAfectados = BienAfectadoAviosoSiniestro.objects.filter(IdBienConstancia = bienConstancia.IdDescripcionBienActaVerificacion)
            
            if bienesAfectados:
                numeroBienAfectado = bienesAfectados[0].NumeroBienAfectado
            
            sumaAsegurada = bienConstancia.Cantidad * bienConstancia.ValorUnitario;
            bienesAMostrar.append({'Nombre':bienConstancia.NombreEquipo, 'Cantidad':bienConstancia.Cantidad, 'SumaAseguradaUnitaria':bienConstancia.ValorUnitario, 'SumaAsegurada':sumaAsegurada,
                                       'NumeroBienesAfectados':numeroBienAfectado});
            
            numeroBienAfectado = ''
    
    html = render_to_string('reporteactasiniestro.html',{'actasiniestro':actasiniestro, 'bienesAfectados':bienesAMostrar, 'usuario':request.user}, context_instance = RequestContext(request))
    return generar_pdf(html)

def obtenerNombrePersona(idPersona):
    
    nombrePersona = ''
    
    persona = Persona.objects.filter(IdPersona = idPersona)[0]
    
    if persona.TipoPersona == 'F':
        nombrePersona = persona.PrimerNombre + " " + persona.SegundoNombre + " " + persona.ApellidoPaterno + " " + persona.ApellidoMaterno
    elif persona.TipoPersona == 'M':
        nombrePersona = persona.RazonSocial

    return nombrePersona
    

@login_required()
def acta_siniestro(request, id_inspeccion): # Vista que nos permite mostrar la acta de siniestro mediante la plantilla actasiniestro.html pasandole el id de la inspeccion.
    
    bienesAMostrar = list()
    
    idActaSiniestro = ''
    folioActaSiniestro = ''
    tipoAviso = ''
    fechaSiniestro = ''
    montoDano = ''
    tipoDescripcion = '--------'
    nombreAsegurado = ''
    nombreTecnico = ''
    horaSiniestro = ''
    proporcion = 0
    noBienesAfectados = 0
    montoBien = 0
        
    inspeccion = Inspeccion.objects.filter(IdInspeccion = id_inspeccion)[0]
    
    avisoSiniestro = AvisoSiniestro.objects.filter(IdAvisoSiniestro = inspeccion.AvisoSiniestro_id)[0]
    
    actaSiniestro = ActaSiniestro.objects.filter(Inspeccion_id = id_inspeccion)
    
    if actaSiniestro:
        idActaSiniestro = actaSiniestro[0].IdActaSiniestro
        folioActaSiniestro = actaSiniestro[0].FolioActaSiniestro
        tipoAviso = actaSiniestro[0].TipoAviso
        fechaSiniestro = actaSiniestro[0].FechaSiniestro
        montoDano = actaSiniestro[0].MontoDano
        horaSiniestro = actaSiniestro[0].HoraSiniestro
    else:
        tipoAviso = avisoSiniestro.TipoAviso
        fechaSiniestro = avisoSiniestro.FechaSiniestro
        horaSiniestro = avisoSiniestro.HoraSiniestro
        
    constancia = Constancia.objects.filter(IdConstancia = avisoSiniestro.Constancia_id)[0]
    solicitud = Solicitud.objects.filter(IdSolicitud = constancia.Solicitud_id)[0]
    programa = Programa.objects.filter(IdPrograma = solicitud.Programa_id)[0]
    moneda = Moneda.objects.using('catalogos').filter(IdMoneda = programa.IdTipoMoneda)[0]    
    nombreAsegurado = obtenerNombrePersona(solicitud.PersonaAsegurada_id)
    inspeccion = Inspeccion.objects.filter(AvisoSiniestro_id = avisoSiniestro.IdAvisoSiniestro)[0]
    personalApoyo = PersonalApoyo.objects.filter(IdPersonalApoyo = inspeccion.PersonalApoyo_id)[0]   
    nombreTecnico = obtenerNombrePersona(personalApoyo.Persona_id)
                 
    descripcionBienEndosoAd = DescripcionBienEndosoAD.objects.filter(Constancia_id = avisoSiniestro.Constancia_id, Utilizado = 1)
    
    if descripcionBienEndosoAd:
        
        for bien in descripcionBienEndosoAd:
            
            bienAfectado = BienAfectadoAviosoSiniestro.objects.filter(IdBienConstancia = bien.IdDescripcionBienEndosoAD)[0]
            
            if bienAfectado:
                
                if idActaSiniestro != '':
                    bienesActaSiniestro = BienActaSiniestro.objects.filter(IdBienAfectado = bienAfectado.IdBienAfectado, ActaSiniestro_id = idActaSiniestro)
                    
                    if bienesActaSiniestro:
                        tipoDescripcion = bienesActaSiniestro[0].TipoBienActaSiniestro
                        idBienActaSiniestro = bienesActaSiniestro[0].IdBienActaSiniestro
                        noBienesAfectados = bienesActaSiniestro[0].UnidadesAfectadas
                        proporcion = bienesActaSiniestro[0].Proporcion
                        montoBien = bienesActaSiniestro[0].Monto
                else:
                    noBienesAfectados = bienAfectado[0].NumeroBienAfectado
                    proporcion = 0
                    montoBien =  0
                
                sumaBien = bien.Cantidad * bien.ValorUnitario
                bienesAMostrar.append({'IdBienActaSiniestro':idBienActaSiniestro, 'IdBienAfectado':bienAfectado.IdBienAfectado, 'Nombre':bien.NombreEquipo, 'Cantidad':'{:,}'.format(bien.Cantidad),
                    'ValorUnitario':'{:10,.4f}'.format(bien.ValorUnitario), 'SumaAsegurada':'{:10,.4f}'.format(sumaBien), 'NoBienesAfectados':noBienesAfectados, 'EstadoDanos':bienAfectado.EstadoDelDano,
                    'Descripcion':bienAfectado.Descripcion, 'TipoDescripcion':tipoDescripcion, 'proporcion':str(proporcion),
                    'montoBien':str(montoBien)})
                tipoDescripcion = '--------'
                idBienActaSiniestro = 0
                noBienesAfectados = 0
                proporcion = 0
                montoBien = 0
                    
    else:
        
        constancia = Constancia.objects.filter(IdConstancia = avisoSiniestro.Constancia_id)[0]
        relacionAnexaActaVerificacion = RelacionAnexaActaVerificacion.objects.filter(Solicitud_id = constancia.Solicitud_id)[0]
        descripcionBienActaVerificacion = DescripcionBienActaVerificacion.objects.filter(RelacionAnexaActaVerificacion_id = relacionAnexaActaVerificacion.IdRelacionAnexaActaVerificacion)
        
        for bien in descripcionBienActaVerificacion:
                     
            bienAfectado = BienAfectadoAviosoSiniestro.objects.filter(IdBienConstancia = bien.IdDescripcionBienActaVerificacion)
           
            if bienAfectado:
                if idActaSiniestro != '':
                    bienesActaSiniestro = BienActaSiniestro.objects.filter(IdBienAfectado = bienAfectado[0].IdBienAfectado, ActaSiniestro_id = idActaSiniestro)
                    
                    if bienesActaSiniestro:
                        tipoDescripcion = bienesActaSiniestro[0].TipoBienActaSiniestro
                        idBienActaSiniestro = bienesActaSiniestro[0].IdBienActaSiniestro
                        noBienesAfectados = bienesActaSiniestro[0].UnidadesAfectadas
                        proporcion = bienesActaSiniestro[0].Proporcion
                        montoBien = bienesActaSiniestro[0].Monto
                else:
                    noBienesAfectados = bienAfectado[0].NumeroBienAfectado
                    proporcion = 0
                    montoBien =  0
                    
                sumaBien = bien.Cantidad * bien.ValorUnitario
                bienesAMostrar.append({'IdBienAfectado':bienAfectado[0].IdBienAfectado, 'Nombre':bien.NombreEquipo, 'Cantidad':'{:,}'.format(bien.Cantidad),
                    'ValorUnitario':'{:10,.4f}'.format(bien.ValorUnitario), 'SumaAsegurada':'{:10,.4f}'.format(sumaBien), 'NoBienesAfectados':noBienesAfectados, 'EstadoDanos':bienAfectado[0].EstadoDelDano,
                    'Descripcion':bienAfectado[0].Descripcion, 'TipoDescripcion':tipoDescripcion, 'proporcion':str(proporcion),
                    'montoBien':str(montoBien)})
                tipoDescripcion = '--------'
                idBienActaSiniestro = 0
                noBienesAfectados = 0
                proporcion = 0
                montoBien = 0
                
    return render(request, 'actasiniestro.html', {'usuario':request.user, 'bienes':bienesAMostrar, 'idInspeccion':inspeccion.IdInspeccion, 'idActaSiniestro':idActaSiniestro,
                                                 'folioActaSiniestro':folioActaSiniestro, 'tipoAviso':tipoAviso, 'fechaSiniestro':fechaSiniestro,
                                                 'montoDano':montoDano, 'tipoMoneda': moneda.Descripcion, 'nombrePersona':nombreAsegurado, 'nombreTecnico':nombreTecnico, 'avisoSiniestro':avisoSiniestro,
                                                 'fechaInspeccion':str(inspeccion.FechaInspeccion.strftime("%d/%m/%Y")), 'numeroConstancia':constancia.FolioConstancia,
                                                 'horaSiniestro':horaSiniestro},context_instance=RequestContext(request))

@login_required()
def guardar_acta_siniestro(request):# Metodo que nos permite guardar la informacion obtenida del acta de siniestro.                
    
    folioActaSiniestro = ''
    idActaSiniestro = 0
    
    if request.is_ajax():
        
        idActaSiniestro = str(request.POST['idActaSiniestro'])
        listaBienesProcedenciaJson = json.loads(request.POST['bienesProcedencia'])
        listaBienesNegativaJson = json.loads(request.POST['bienesNegativa'])
        
        if idActaSiniestro == "":
            
            actaSiniestro = ActaSiniestro(Inspeccion_id = int(request.POST['idInspeccion']), 
                                            TipoAviso = str(request.POST['tipoAviso']).upper(),
                                            FechaSiniestro = datetime.strptime(request.POST['fechaSiniestro'],'%d/%m/%Y').strftime('%Y-%m-%d'),
                                            MontoDano = request.POST['montoDano'],
                                            HoraSiniestro = request.POST['horaSiniestro'])
            actaSiniestro.save();
            
            idActaSiniestro = actaSiniestro.IdActaSiniestro
            
            folioActaSiniestro = 'ACS-' + str(idActaSiniestro)            
            
            ActaSiniestro.objects.filter(IdActaSiniestro = actaSiniestro.IdActaSiniestro).update(FolioActaSiniestro = folioActaSiniestro)
            
            for bien in listaBienesProcedenciaJson:           
                guardar_bien_actaSiniestro_procedencia(bien, actaSiniestro.IdActaSiniestro)                
                
            for bien in listaBienesNegativaJson:                
                guardar_bien_actaSiniestro_negativa(bien, actaSiniestro.IdActaSiniestro)
                       
        else:
                        
            ActaSiniestro.objects.filter(IdActaSiniestro = idActaSiniestro).update(Inspeccion = int(request.POST['idInspeccion']), TipoAviso = str(request.POST['tipoAviso']).upper(),
                                                                                    FechaSiniestro = datetime.strptime(request.POST['fechaSiniestro'],'%d/%m/%Y').strftime('%Y-%m-%d'),
                                                                                    MontoDano = request.POST['montoDano'], HoraSiniestro = request.POST['horaSiniestro'])
            
            bienesActaSiniestroGuardados = BienActaSiniestro.objects.filter(ActaSiniestro_id = idActaSiniestro)
            
            verificar_bienes_actasiniestro_procedencia(bienesActaSiniestroGuardados, listaBienesProcedenciaJson, idActaSiniestro)
            verificar_bienes_actasiniestro_negativa(bienesActaSiniestroGuardados, listaBienesNegativaJson, idActaSiniestro)      
    
    return HttpResponse(json.dumps({'folio':idActaSiniestro, 'idActaSiniestro':idActaSiniestro}), content_type="application/json; charset=uft8")

def verificar_bienes_actasiniestro_procedencia(bienesGuardados, bienesAGuardar, idActaSiniestro): # Funcion que nos permite verificar los bienes procedentes que ya fueron almacenados en la base de datos.
    
    encontrado = False
    
    for bienGuardado in bienesGuardados:
        if bienGuardado.TipoBienActaSiniestro == "PROCEDENCIA":
            for bienAGuardar in bienesAGuardar:
                if bienAGuardar['IdBienActaSiniestro'] != '':
                    if str(bienAGuardar['IdBienActaSiniestro']) == str(bienGuardado.IdBienActaSiniestro):
                        encontrado = True
                    
            if encontrado == False:
                BienActaSiniestro.objects.filter(IdBienActaSiniestro = bienGuardado.IdBienActaSiniestro).delete()
            else:
                encontrado = False    
            
    for bienAGuardar in bienesAGuardar:
        
        if str(bienAGuardar['IdBienActaSiniestro']) == '':
            guardar_bien_actaSiniestro_procedencia(bienAGuardar, idActaSiniestro)
        else:
            BienActaSiniestro.objects.filter(IdBienActaSiniestro = int(bienAGuardar['IdBienActaSiniestro'])).update(IdBienAfectado = int(bienAGuardar['IdBienAfectado']),
                                                                                                                    RiesgoAfectado = bienAGuardar['RiesgoAfectado'].upper(),
                                                                                                                    UnidadesAfectadas = bienAGuardar['UnidadesAfectadas'].upper(),
                                                                                                                    Solvento = bienAGuardar['Solvento'].upper(),
                                                                                                                    Proporcion = bienAGuardar['Proporcion'].upper(),
                                                                                                                    FuePerdida = bienAGuardar['FuePerdida'],
                                                                                                                    Monto = bienAGuardar['Monto'])   

def verificar_bienes_actasiniestro_negativa(bienesGuardados, bienesAGuardar, idActaSiniestro): # Funcion que nos permite verificar los bienes negativos que ya fueron almacenados en la base de datos.
    
    encontrado = False
    
    for bienGuardado in bienesGuardados:
        if bienGuardado.TipoBienActaSiniestro == "NEGATIVA":
            for bienAGuardar in bienesAGuardar:
                if bienAGuardar['IdBienActaSiniestro'] != '':
                    if str(bienAGuardar['IdBienActaSiniestro']) == str(bienGuardado.IdBienActaSiniestro):
                        encontrado = True
                    
            if encontrado == False:
                BienActaSiniestro.objects.filter(IdBienActaSiniestro = bienGuardado.IdBienActaSiniestro).delete()
            else:    
                encontrado = False
            
    for bienAGuardar in bienesAGuardar:
        
        if str(bienAGuardar['IdBienActaSiniestro']) == '':
            guardar_bien_actaSiniestro_negativa(bienAGuardar, idActaSiniestro)
        else:
            BienActaSiniestro.objects.filter(IdBienActaSiniestro = bienAGuardar['IdBienActaSiniestro']).update(IdBienAfectado = int(bienAGuardar['IdBienAfectado']),
                                                                                                                Descripcion = bienAGuardar['Descripcion'].upper())
                

def guardar_bien_actaSiniestro_procedencia(bien, idActaSiniestro): # Funcion que nos permite guardar el bien del acta de siniestro cuando el bien es procedente.
    
    bienActaSiniestro = BienActaSiniestro(
                                            IdBienAfectado = int(bien['IdBienAfectado']),
                                            RiesgoAfectado = bien['RiesgoAfectado'].upper(),
                                            UnidadesAfectadas = bien['UnidadesAfectadas'].upper(),
                                            Solvento = bien['Solvento'].upper(),
                                            Proporcion = bien['Proporcion'].upper(),
                                            FuePerdida = bien['FuePerdida'].upper(),
                                            Monto = bien['Monto'],
                                            ActaSiniestro_id = idActaSiniestro,
                                            TipoBienActaSiniestro = 'PROCEDENCIA')
     
    bienActaSiniestro.save()
    
def guardar_bien_actaSiniestro_negativa(bien, idActaSiniestro): # Funcion que nos permite guardar el bien cuando este es negativa.
    
    bienActaSiniestro = BienActaSiniestro(
                                            IdBienAfectado = int(bien['IdBienAfectado']),
                                            Descripcion = bien['Descripcion'].upper(),
                                            ActaSiniestro_id = idActaSiniestro,
                                            TipoBienActaSiniestro = 'NEGATIVA')
                
    bienActaSiniestro.save()
    
@login_required()
def obtener_bienes_acta_siniestro(request):# Metodo que nos permite obtener de la base de datos los bienes del acta de siniestro.
    
    if request.is_ajax():
        
        datos = list()
            
        idActaSiniestro = request.POST['idActaSiniestro']
        
        if idActaSiniestro != '':
            bienesActaSiniestro = BienActaSiniestro.objects.filter(ActaSiniestro_id = int(idActaSiniestro))
            
            for bien in bienesActaSiniestro:
            
                datos.append({'IdBienActaSiniestro':bien.IdBienActaSiniestro, 'IdBienAfectado':bien.IdBienAfectado, 'RiesgoAfectado':bien.RiesgoAfectado, 'UnidadesAfectadas':bien.UnidadesAfectadas,
                                               'Solvento':bien.Solvento, 'Proporcion':str(bien.Proporcion), 'FuePerdida':bien.FuePerdida, 'Monto':str(bien.Monto),
                                               'Descripcion':bien.Descripcion, 'TipoBienActaSiniestro':bien.TipoBienActaSiniestro})
                 
    return HttpResponse(json.dumps({'bienes':datos}), content_type="application/json; charset=uft8")