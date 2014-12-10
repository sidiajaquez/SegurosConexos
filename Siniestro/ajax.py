#encoding:utf-8
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from Siniestro.models import AvisoSiniestro, BienAfectadoAviosoSiniestro,\
    Inspeccion, ActaSiniestro
from Constancias.models import Constancia
from django.db import connections
import datetime
from Solicitud.models import Solicitud, DescripcionBienActaVerificacion,\
    RelacionAnexaActaVerificacion
from smtpd import program
from Programas.models import Programa, CoberturaPrograma, Cobertura
from Cotizador.models import Cotizador, CotizadorCobertura
from ConexosAgropecuarios.models import Persona, Telefono, PersonalApoyo
from django.db.models import Q
from Direcciones.models import Direccion
from dajaxice.utils import deserialize_form
from Endoso.models import DescripcionBienEndosoAD

@dajaxice_register
def CargarActasSiniestro(request): #Metodo que obtiene las actas de siniestro para su dictamen
    
    cursor = connections['siobicx'].cursor()
    sql_string = "SELECT * FROM vdictamensiniestro" 
    cursor.execute(sql_string)
    actasSiniestro = cursor.fetchall()
    
    return simplejson.dumps({'ActasSiniestro':actasSiniestro})

@dajaxice_register
def obtener_avisos_siniestro(request):# Método que obtiene los avisos de siniestros de la base de datos.
    dajax = Dajax()
    try:
        cursor = connections['siobicx'].cursor()
        sql_string = "SELECT * FROM vlistadoavisossiniestro" 
        cursor.execute(sql_string)
        result = cursor.fetchall()
                    
    except:
        return dajax.json()
    
    return simplejson.dumps({'avisos':result})


@dajaxice_register
def buscar_constancia(request, buscar): # Funcion que obtiene la busqueda de las constancias vigentes para realizar un aviso de siniestro.
    
    constancias = Constancia.objects.filter(Q(FolioConstancia__contains = buscar), VigenciaFin__gte = datetime.datetime.now())
    datosConstancia = list()
    causaSiniestro = list()
    
    if constancias:
        for constancia in constancias:
            
            solicitud = Solicitud.objects.filter(IdSolicitud = constancia.Solicitud_id)[0]
            programa = Programa.objects.filter(IdPrograma = solicitud.Programa_id)[0]
            persona = Persona.objects.filter(IdPersona = solicitud.PersonaAsegurada_id)[0]
            
            if persona.TipoPersona == 'F':
                nombreAsegurado = persona.PrimerNombre + ' ' + persona.SegundoNombre + ' ' + persona.ApellidoPaterno + ' ' + persona.ApellidoMaterno
            else:
                nombreAsegurado = persona.RazonSocial
                               
            vigenciaConstancia = constancia.VigenciaInicio.strftime("%d/%m/%Y") + " al " + constancia.VigenciaFin.strftime("%d/%m/%Y")
            datosConstancia.append({'IdConstancia':constancia.IdConstancia, 'Constancia':constancia.FolioConstancia,'Ejercicio':programa.Ejercicio,'Asegurado':nombreAsegurado,
                                    'Vigencia':vigenciaConstancia, 'CausaSiniestro':causaSiniestro, 'IdPrograma':programa.IdPrograma})

    return simplejson.dumps({'constancias':datosConstancia})

@dajaxice_register
def buscar_causa_siniestro_programa(req, idPrograma): # Metodo que nos permite buscar la causa del siniestro, mediante los riesgos del programa.
    causaSiniestro = list()
    
    cotizadorEncontrado = Cotizador.objects.filter(Programa_id = idPrograma)
            
    if cotizadorEncontrado:
        cotizadorCoberturaEncontradas = CotizadorCobertura.objects.filter(Cotizador_id = cotizadorEncontrado[0].IdCotizador)
          
        if cotizadorCoberturaEncontradas:
            for cotizadorCobertura in cotizadorCoberturaEncontradas:                        
                coberturaProgramaEncontrada = CoberturaPrograma.objects.filter(IdCoberturaPrograma = cotizadorCobertura.CoberturaPrograma_id)
                
                if coberturaProgramaEncontrada:                            
                    for cotizadorPrograma in coberturaProgramaEncontrada:
                        coberturaEncontrada = Cobertura.objects.using('catalogos').filter(IdCobertura = cotizadorPrograma.IdCobertura)
                        
                        if coberturaEncontrada:
                            
                            causaSiniestro.append({'IdCotizadorCobertura':cotizadorCobertura.IdCotizadorCobertura, 'Descripcion':coberturaEncontrada[0].Descripcion, 'Deducible':str(cotizadorCobertura.Deducible),
                                                   'ParticipacionAPerdida':str(cotizadorCobertura.ParticipacionAPerdida)})
                                                        
    return simplejson.dumps({'causaSiniestro':causaSiniestro})

@dajaxice_register
def buscar_persona_avisa(req, datosBuscar): # Metodo que nos permite buscar en la tabla personas, filtrando mediante la variable datosBuscar.
    dajax = Dajax()
    try:
        datos = list()
        personas = Persona.objects.filter((Q(Rfc__contains=datosBuscar) | Q(PrimerNombre__contains=datosBuscar) | Q(SegundoNombre__contains=datosBuscar) | Q(ApellidoPaterno__contains=datosBuscar) | Q(ApellidoMaterno__contains=datosBuscar)), Q(TipoPersona='F'))
            
        for persona in personas:
            nombre = persona.PrimerNombre + " " + persona.SegundoNombre + " " + persona.ApellidoPaterno + " " + persona.ApellidoMaterno
            datos.append({'IdPersona':persona.IdPersona,'Nombre':nombre,'Rfc':persona.Rfc})
                              
    except:
        return dajax.json()
    
    return simplejson.dumps({'personas':datos})

@dajaxice_register
def buscar_persona_tecnico(req, datosBuscar): # Metodo que nos permite obtener los tecnicos del fondo.
    dajax = Dajax()
    
    try:
        cursor = connections['siobicx'].cursor()
        sql_string = 'SELECT * FROM vpersonalapoyo WHERE Nombre Like ' + "'%" + str(datosBuscar) + "%'"
        cursor.execute(sql_string)
        tecnicos = cursor.fetchall()
        
    except:
        return dajax.json()
    
    return simplejson.dumps({'tecnicos':tecnicos})

@dajaxice_register
def guardar_aviso_siniestro(request, formulario, horaAviso, horaSiniestro, bienes, tieneAumento, causaSiniestro, idCotizadorCobertura, deducible, participacionAPerdida):# Metodo que nos permite guardar el aviso de siniestro obteniendo la informacion del formulario obtenida del js.
    dajax = Dajax()          
                      
    if bienes == '':
        list_bienes = ''
    else:
        array_convertido_string = simplejson.dumps(bienes, separators=('|',','))
        list_bienes = array_convertido_string.replace('[', '').replace(']', '').replace('"', '').split(';')                     
                      
    formulario_deserializado = deserialize_form(formulario)
     
    if formulario_deserializado.get('varIdAvisoSiniestro') == '':
        
        fechaAviso = formulario_deserializado.get('dtpFechaAviso');
        fechaSiniestro = formulario_deserializado.get('dtpFechaSiniestro');
        
        if formulario_deserializado.get('varIdPersonaAvisa') == '':
            idPersonaAvisa = None
        else:
            idPersonaAvisa = formulario_deserializado.get('varIdPersonaAvisa')
            
        if formulario_deserializado.get('txtOtros') == '':
            viaAviso = formulario_deserializado.get('cmbViaAviso')
            otravia = False
        else:
            viaAviso = formulario_deserializado.get('txtOtros')
            otravia = True
        
        avisoSiniestro = AvisoSiniestro(Constancia_id = formulario_deserializado.get('varIdConstancia'), 
                                        FechaAviso = datetime.datetime.strptime(fechaAviso,'%d/%m/%Y').strftime('%Y-%m-%d'),
                                        FechaSiniestro = datetime.datetime.strptime(fechaSiniestro,'%d/%m/%Y').strftime('%Y-%m-%d'),     
                                        PersonaAvisa_id = idPersonaAvisa, NombreAvisa = formulario_deserializado.get('txtQuienAvisa').upper(),
                                        ViaAviso = viaAviso.upper(),
                                        DescripcionBienAfectado = formulario_deserializado.get('txtBien').upper(), PersonaTecnico_id = formulario_deserializado.get('varIdTecnico'),
                                        HoraAviso = str(horaAviso), HoraSiniestro = str(horaSiniestro), OtraVia = otravia, TipoAviso = formulario_deserializado.get('cmbTipoAviso'),
                                        CausaSiniestro = str(causaSiniestro.upper()), IdStatusAvisoSiniestro = int(formulario_deserializado.get('varStatusAviso')),
                                        CausaAgravante = str(formulario_deserializado.get('txtCausaAgravante').upper()), CotizadorCobertura_id = idCotizadorCobertura, Deducible = deducible,
                                        ParticipacionAPerdida = participacionAPerdida)        
        avisoSiniestro.save();  
        
        folioAviso = 'AVS-' + str(avisoSiniestro.IdAvisoSiniestro)
        
        AvisoSiniestro.objects.filter(IdAvisoSiniestro = avisoSiniestro.IdAvisoSiniestro).update(FolioAviso = folioAviso)
        
        if list_bienes != '':
            for bien in list_bienes:
                guardar_bienes_afectados(avisoSiniestro.IdAvisoSiniestro, bien, tieneAumento)
                      
        dajax.add_data(avisoSiniestro.IdAvisoSiniestro, 'mensajeGuardadoSiniestro')
    
    else:
        actualizar_aviso(formulario_deserializado, horaAviso, horaSiniestro, list_bienes, tieneAumento, causaSiniestro, idCotizadorCobertura, deducible, participacionAPerdida) 
        
    return dajax.json()

def guardar_bienes_afectados(id_aviso, bien, tieneAumento): # Metodo que nos permite guardar el bien afectado en la tabla de la base de datos mediante el id del aviso de siniestro.
    dajax = Dajax()
    
    list_bien = bien.split(',')
    bienAfectado = BienAfectadoAviosoSiniestro(AvisoSiniestro_id = id_aviso, IdBienConstancia = list_bien[1], NumeroBienAfectado = list_bien[2], EstadoDelDano = (list_bien[3]).upper(), Descripcion = (list_bien[4]).upper(), TieneAumento = bool(tieneAumento))
    bienAfectado.save()
        
    return dajax.json()

def actualizar_aviso(formulario, horaAviso, horaSiniestro, bienesAfectados, tieneAumento, causaSiniestro, idCotizadorCobertura, deducible, participacionAPerdida):# Metodo que nos permite actualizar los datos del aviso de siniestro pasando el formulario y las horas de siniestro y aviso.
    dajax = Dajax()
    
    fechaAviso = formulario.get('dtpFechaAviso');
    fechaSiniestro = formulario.get('dtpFechaSiniestro');
    
    if formulario.get('varIdPersonaAvisa') == '' or formulario.get('varIdPersonaAvisa') == 'None':
        idPersonaAvisa = None
    else:
        idPersonaAvisa = formulario.get('varIdPersonaAvisa')
        
    if formulario.get('txtOtros') == '':
        viaAviso = formulario.get('cmbViaAviso')
        otravia = False
    else:
        viaAviso = formulario.get('txtOtros')
        otravia = True
    
    AvisoSiniestro.objects.filter(IdAvisoSiniestro = formulario.get('varIdAvisoSiniestro')).update(Constancia = int(formulario.get('varIdConstancia')), 
                                        FechaAviso = datetime.datetime.strptime(fechaAviso,'%d/%m/%Y').strftime('%Y-%m-%d'),
                                        FechaSiniestro = datetime.datetime.strptime(fechaSiniestro,'%d/%m/%Y').strftime('%Y-%m-%d'),     
                                        PersonaAvisa = idPersonaAvisa, NombreAvisa = formulario.get('txtQuienAvisa').upper(),
                                        ViaAviso = viaAviso.upper(), DescripcionBienAfectado = formulario.get('txtBien').upper(),
                                        PersonaTecnico = formulario.get('varIdTecnico'), HoraAviso = str(horaAviso),
                                        HoraSiniestro = str(horaSiniestro), OtraVia = otravia, TipoAviso = formulario.get('cmbTipoAviso'),
                                        CausaSiniestro = str(causaSiniestro.upper()), IdStatusAvisoSiniestro = int(formulario.get('varStatusAviso')),
                                        CausaAgravante = str(formulario.get('txtCausaAgravante').upper()), CotizadorCobertura = idCotizadorCobertura, Deducible = deducible,
                                        ParticipacionAPerdida = participacionAPerdida)
    
    actualizar_bienes_afectados(bienesAfectados, formulario.get('varIdAvisoSiniestro'), tieneAumento)    
                
    return dajax.json()

def actualizar_bienes_afectados(bienesAfectados, id_aviso, tieneAumento): # Metodo que nos permite actualizar los bienes afectado en la base de datos.
    dajax = Dajax()
    
    bienesAfectadosGuardado = BienAfectadoAviosoSiniestro.objects.filter(AvisoSiniestro_id = id_aviso)
    
    for bienPorDiaEliminar in bienesAfectadosGuardado:
        encontradoAEliminar = 1
        for bienABuscar in bienesAfectados:
            list_bien = bienABuscar.split(',')
            if list_bien[0] != '':
                if int(list_bien[0]) == bienPorDiaEliminar.IdBienAfectado:
                    encontradoAEliminar = 0
                    break
                
        if encontradoAEliminar == 1:
            eliminar_bien_afectado(bienPorDiaEliminar.IdBienAfectado)
    
    for bien in bienesAfectados:
        list_bien = bien.split(',')
        if list_bien[0] == '':
            guardar_bienes_afectados(id_aviso, bien, tieneAumento)
        else:
            actualizar_bien_afectado(list_bien)

    return dajax.json()

def actualizar_bien_afectado(bien): # Método que nos permite actualizar la informacion de un bien afectado.
    BienAfectadoAviosoSiniestro.objects.filter(IdBienAfectado = bien[0]).update(NumeroBienAfectado = (bien[2]).upper(), EstadoDelDano = (bien[3]).upper(), Descripcion = (bien[4]).upper())
    

def eliminar_bien_afectado(idBienAfectado): # Método que recibe el id del bien afectado para eliminarlo de la base de datos. 
    dajax = Dajax()
    BienAfectadoAviosoSiniestro.objects.filter(IdBienAfectado = idBienAfectado).delete()
      
    return dajax.json()

@dajaxice_register
def obtener_descripcion_bienes_constancia(req, id_constancia): # Método que obtiene los bienes de la constancia seleccionada, si la constancia ya tiene un aumento o disminucion los toma de la tabla DescripcionBienEndosoAD.
    dajax = Dajax()
    datos = list()
    tieneAumento = False
    
    try:        
        descripcionBienAD = DescripcionBienEndosoAD.objects.filter(Constancia_id = id_constancia, Utilizado = 1)
        
        if descripcionBienAD:
            tieneAumento = True
            
            for descripcion in descripcionBienAD:                
                sumaBien = descripcion.Cantidad * descripcion.ValorUnitario            
                datos.append({'IdDescripcion':descripcion.IdDescripcionBienEndosoAD,'NombreEquipo':descripcion.NombreEquipo,'Cantidad':str(descripcion.Cantidad),'ValorUnitario':str(descripcion.ValorUnitario),'SumaBien':str(sumaBien)})
        
        else:    
            constancia = Constancia.objects.filter(IdConstancia = id_constancia)[0]
            relacionAnexaActaVerificacion = RelacionAnexaActaVerificacion.objects.filter(Solicitud_id = constancia.Solicitud_id)[0]
            descripcionAnexaActaVerificacion = DescripcionBienActaVerificacion.objects.filter(RelacionAnexaActaVerificacion_id = relacionAnexaActaVerificacion.IdRelacionAnexaActaVerificacion)
            
            for descripcion in descripcionAnexaActaVerificacion:                
                sumaBien = descripcion.Cantidad * descripcion.ValorUnitario
                datos.append({'IdDescripcion':descripcion.IdDescripcionBienActaVerificacion,'NombreEquipo':descripcion.NombreEquipo,'Cantidad':str(descripcion.Cantidad),'ValorUnitario':str(descripcion.ValorUnitario),'SumaBien':str(sumaBien)})
    except:
        return dajax.json()
    
    return simplejson.dumps({'descripcionBienes':datos, 'tieneAumento':tieneAumento})

@dajaxice_register
def obtener_bienes_afectados(req, id_aviso, id_constancia): # Método que obtiene los bienes afectados mediante el id del aviso de siniestro.
    dajax = Dajax()
    datos = list()
    
    try:
       
        descripcionesBienAD = DescripcionBienEndosoAD.objects.filter(Constancia_id = id_constancia)
            
        if descripcionesBienAD:
            for descripcionBienAD in descripcionesBienAD: 
                
                bienesAfectados = BienAfectadoAviosoSiniestro.objects.filter(AvisoSiniestro_id = id_aviso)

                for bienAfectado in bienesAfectados:
                    if descripcionBienAD.IdDescripcionBienEndosoAD == bienAfectado.IdBienConstancia:
                        idBienAfectado = bienAfectado.IdBienAfectado
                        noBienesAfectados = bienAfectado.NumeroBienAfectado
                        estadoDanos = bienAfectado.EstadoDelDano
                        descripcion = bienAfectado.Descripcion
                        
                sumaBien = descripcionBienAD.Cantidad * descripcionBienAD.ValorUnitario
                datos.append({'IdBienAfectado':idBienAfectado, 'IdDescripcion':descripcionBienAD.IdDescripcionBienEndosoAD, 'Nombre':descripcionBienAD.NombreEquipo, 'Cantidad':str('{:,}'.format(descripcionBienAD.Cantidad)),
                                        'ValorUnitario':str('{:,}'.format(descripcionBienAD.ValorUnitario)), 'SumaAsegurada':str('{:,}'.format(sumaBien)), 'NoBienesAfectados':noBienesAfectados, 'EstadoDanos':estadoDanos,
                                        'Descripcion':descripcion})
                idBienAfectado = ''
                noBienesAfectados = ''
                estadoDanos = ''
                descripcion = ''
        else:
            
            constancia = Constancia.objects.filter(IdConstancia = id_constancia)[0]
            relacionAnexaActaVerificacion = RelacionAnexaActaVerificacion.objects.filter(Solicitud_id = constancia.Solicitud_id)[0]
            descripcionBienActaVerificacion = DescripcionBienActaVerificacion.objects.filter(RelacionAnexaActaVerificacion_id = relacionAnexaActaVerificacion.IdRelacionAnexaActaVerificacion)
            
            for descripcionBien in descripcionBienActaVerificacion:
                
                bienesAfectados = BienAfectadoAviosoSiniestro.objects.filter(AvisoSiniestro_id = id_aviso)
                    
                for bienAfectado in bienesAfectados:
                    if descripcionBien.IdDescripcionBienActaVerificacion == bienAfectado.IdBienConstancia:
                        idBienAfectado = bienAfectado.IdBienAfectado
                        noBienesAfectados = bienAfectado.NumeroBienAfectado
                        estadoDanos = bienAfectado.EstadoDelDano
                        descripcion = bienAfectado.Descripcion
                
                sumaBien = descripcionBien.Cantidad * descripcionBien.ValorUnitario
                datos.append({'IdBienAfectado':idBienAfectado, 'IdDescripcion':descripcionBien.IdDescripcionBienActaVerificacion, 'Nombre':descripcionBien.NombreEquipo, 'Cantidad':str(descripcionBien.Cantidad),
                                    'ValorUnitario':str(descripcionBien.ValorUnitario), 'SumaAsegurada':str(sumaBien), 'NoBienesAfectados':str(noBienesAfectados), 'EstadoDanos':estadoDanos,
                                    'Descripcion':descripcion})
                idBienAfectado = ''
                noBienesAfectados = ''
                estadoDanos = ''
                descripcion = ''
    except:
        return dajax.json()
    
    return simplejson.dumps({'bienesAfectados':datos})
   
@dajaxice_register
def guardar_estado_aviso(request, idAviso, idStatus):# Metodo que nos permite actualizar el status del aviso de siniestro.
    dajax = Dajax()     
        
    AvisoSiniestro.objects.filter(IdAvisoSiniestro = idAviso).update(IdStatusAvisoSiniestro = idStatus)
    
    return dajax.json()

@dajaxice_register
def obtener_avisos_siniestro_terminados(req, buscar): # Metodo que obtiene los avisos de siniestro terminados, para mostrarlos en el modal de busqueda y poder seleccionar uno en la platilla inspeccion.html
    dajax = Dajax()
    try:
        
        cursor = connections['siobicx'].cursor()
        sql_string = "SELECT * FROM vavisosiniestrocompletado WHERE FolioAviso like '%" + buscar + "%'" 
        cursor.execute(sql_string)
        result = cursor.fetchall()
                    
    except:
        return dajax.json()
    
    return simplejson.dumps({'avisos':result})

@dajaxice_register
def obtener_bienes_seleccionados_afectados(req, id_aviso, id_constancia): # Método que obtiene solo los bienes afectados para mostrarlos en reportes.
    dajax = Dajax()
    datos = list()
    
    try:
       
        descripcionesBienAD = DescripcionBienEndosoAD.objects.filter(Constancia_id = id_constancia)
            
        if descripcionesBienAD:
            for descripcionBienAD in descripcionesBienAD: 
                
                bienesAfectados = BienAfectadoAviosoSiniestro.objects.filter(AvisoSiniestro_id = id_aviso)

                for bienAfectado in bienesAfectados:
                    if descripcionBienAD.IdDescripcionBienEndosoAD == bienAfectado.IdBienConstancia:
                        idBienAfectado = bienAfectado.IdBienAfectado
                        noBienesAfectados = bienAfectado.NumeroBienAfectado
                        estadoDanos = bienAfectado.EstadoDelDano
                        descripcion = bienAfectado.Descripcion
                        
                        sumaBien = descripcionBienAD.Cantidad * descripcionBienAD.ValorUnitario
                        datos.append({'IdBienAfectado':idBienAfectado, 'IdDescripcion':descripcionBienAD.IdDescripcionBienEndosoAD, 'Nombre':descripcionBienAD.NombreEquipo, 'Cantidad':'{:,}'.format(descripcionBienAD.Cantidad),
                                                'ValorUnitario':'{:,}'.format(descripcionBienAD.ValorUnitario), 'SumaAsegurada':'{:,}'.format(sumaBien), 'NoBienesAfectados':noBienesAfectados, 'EstadoDanos':estadoDanos,
                                                'Descripcion':descripcion})
                idBienAfectado = ''
                noBienesAfectados = ''
                estadoDanos = ''
                descripcion = ''
        else:
            
            constancia = Constancia.objects.filter(IdConstancia = id_constancia)[0]
            relacionAnexaActaVerificacion = RelacionAnexaActaVerificacion.objects.filter(Solicitud_id = constancia.Solicitud_id)[0]
            descripcionBienActaVerificacion = DescripcionBienActaVerificacion.objects.filter(RelacionAnexaActaVerificacion_id = relacionAnexaActaVerificacion.IdRelacionAnexaActaVerificacion)
            
            for descripcionBien in descripcionBienActaVerificacion:
                
                bienesAfectados = BienAfectadoAviosoSiniestro.objects.filter(AvisoSiniestro_id = id_aviso)
                    
                for bienAfectado in bienesAfectados:
                    if descripcionBien.IdDescripcionBienActaVerificacion == bienAfectado.IdBienConstancia:
                        idBienAfectado = bienAfectado.IdBienAfectado
                        noBienesAfectados = bienAfectado.NumeroBienAfectado
                        estadoDanos = bienAfectado.EstadoDelDano
                        descripcion = bienAfectado.Descripcion
                
                        sumaBien = descripcionBien.Cantidad * descripcionBien.ValorUnitario
                        datos.append({'IdBienAfectado':bienAfectado.IdBienAfectado, 'IdDescripcion':descripcionBien.IdDescripcionBienActaVerificacion, 'Nombre':descripcionBien.NombreEquipo, 'Cantidad':descripcionBien.Cantidad,
                                            'ValorUnitario':str(descripcionBien.ValorUnitario), 'SumaAsegurada':str(sumaBien), 'NoBienesAfectados':bienAfectado.NumeroBienAfectado, 'EstadoDanos':bienAfectado.EstadoDelDano,
                                            'Descripcion':bienAfectado.Descripcion})
                idBienAfectado = ''
                noBienesAfectados = ''
                estadoDanos = ''
                descripcion = ''
                    
    except:
        return dajax.json()
    
    return simplejson.dumps({'bienesAfectados':datos})


@dajaxice_register
def obtener_tecnicos(req, buscar): # Metodo que nos permite llamar a la vista vpersonalapoyo para encontrar los tecnicos de seguros para asignarles inspecciones.
    dajax = Dajax()
    try:
        
        cursor = connections['siobicx'].cursor()
        sql_string = "SELECT Rfc, Nombre, IdPersonalApoyo FROM vpersonalapoyo WHERE Nombre like '%" + buscar + "%' And Cargo='TECNICO DE CAMPO'" 
        cursor.execute(sql_string)
        result = cursor.fetchall()
                    
    except:
        return dajax.json()
    
    return simplejson.dumps({'tecnicos':result})

@dajaxice_register
def guardar_inpeccion(request, formulario):# Metodo que nos permite guardar la solicitud de inspección obteniendo la informacion del formulario obtenida del js.
    dajax = Dajax()                            
                      
    formulario_deserializado = deserialize_form(formulario)
    
    if formulario_deserializado.get('varIdInspeccion') == '': 
        inspeccion = Inspeccion(AvisoSiniestro_id = int(formulario_deserializado.get('varIdAvisoSiniestro')), 
                                        Constancia_id = int(formulario_deserializado.get('varIdConstancia')),
                                        PersonalApoyo_id = int(formulario_deserializado.get('varIdPersonalApoyo')), 
                                        FechaInspeccion = datetime.datetime.now().strftime("%Y-%m-%d"))
        
        inspeccion.save();  
        
        folioInspeccion = 'IS-' + str(inspeccion.IdInspeccion)
        
        Inspeccion.objects.filter(IdInspeccion = inspeccion.IdInspeccion).update(FolioInspeccion = folioInspeccion)
                      
        dajax.add_data(inspeccion.IdInspeccion, 'mensajeGuardadoInspeccion')
    
    else:
        actualizar_inspeccion(formulario_deserializado)

    return dajax.json()

def actualizar_inspeccion(formulario): # Método que permite actualizar los datos de la inspección en la base de datos.
    dajax = Dajax()
    
    Inspeccion.objects.filter(IdInspeccion = formulario.get('varIdInspeccion')).update(PersonalApoyo_id = formulario.get('varIdPersonalApoyo'))
    
    return dajax.json()
    
@dajaxice_register
def obtener_listado_inspecciones(req): # Método que obtiene las inspecciones mediante la vista vlistadoinspecciones que se encuentran guardadas en la base de datos.
    dajax = Dajax()
    try:
        
        cursor = connections['siobicx'].cursor()
        sql_string = "SELECT * FROM vlistadoinspecciones"
        cursor.execute(sql_string)
        result = cursor.fetchall()
                    
    except:
        return dajax.json()
    
    return simplejson.dumps({'inspecciones':result})

@dajaxice_register
def guardar_acta_siniestro(request, formulario):# Metodo que nos permite guardar la informacion obtenida del acta de siniestro.
    dajax = Dajax()                            
                      
    formulario_deserializado = deserialize_form(formulario)
    
    #if formulario_deserializado.get('varI') == '':
    actaSiniestro = ActaSiniestro(Inspeccion_id = int(formulario_deserializado.get('varIdInspeccion')), 
                                    TipoAviso = formulario_deserializado.get('txtTipoAviso'),
                                    FechaSiniestro = datetime.datetime.strptime(formulario_deserializado.get('txtFechaSiniestro'),'%d/%m/%Y').strftime('%Y-%m-%d'),
                                    MontoDano = formulario_deserializado.get('txtMontoDano'))
    
    actaSiniestro.save();
    
    folioActaSiniestro = 'ACS-' + str(actaSiniestro.IdActaSiniestro)
    
    ActaSiniestro.objects.filter(IdActaSiniestro = actaSiniestro.IdActaSiniestro).update(FolioActaSiniestro = folioActaSiniestro)
                  
    dajax.add_data(actaSiniestro.IdActaSiniestro, 'mensajeGuardadoActaSiniestro')
        
    #else:
    #    actualizar_inspeccion(formulario_deserializado) 

    return dajax.json()