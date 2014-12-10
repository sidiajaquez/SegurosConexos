#encoding:utf-8
import datetime

from django.utils import simplejson
from django.db.models import Q

from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from dajax.core import Dajax

from Programas.models import TipoSeguro, SubTipoSeguro, Programa, Cobertura, CoberturaPrograma, AreaInfluenciaPrograma
from ConexosAgropecuarios.models import AreaInfluencia, Municipio, Persona
from Programas.forms import ProgramaForm
from ConexosAgropecuarios.models import ContratoFondo,Moneda
from Cotizador.models import Cotizador


@dajaxice_register
def cargar_Combo_TipoSeguro(request): # Método que busca los tipos de seguro y los carga en el combo IdTipoSeguro.
    dajax = Dajax()
    tiposSeguros = TipoSeguro.objects.using('catalogos').all()
    
    out = []
    out.append("<option value='#'>%s</option>" % "---------")
    for tipo in tiposSeguros:
        out.append("<option value='" + str(tipo.IdTipoSeguro) + "'>%s</option>" % tipo.DescripcionTipoSeguro)

    dajax.assign('#IdTipoSeguro', 'innerHTML', ''.join(out))
    
    return dajax.json()

@dajaxice_register
def cargar_Combo_SubTipoSeguro(request, idTipoSeguro): # Método que busca los sub tipos de seguro pasandole el id del tipo de seguro
    dajax = Dajax()
    subTipoSeguros = SubTipoSeguro.objects.using('catalogos').filter(TipoSeguro_id = idTipoSeguro)
    
    out = []
    for subTipo in subTipoSeguros:
        out.append("<option value='" + str(subTipo.IdSubTipoSeguro) + "'>%s</option>" % subTipo.DescripcionSubTipoSeguro)

    dajax.assign('#IdSubTipoSeguro', 'innerHTML', ''.join(out))
    
    return dajax.json()

@dajaxice_register
def cargar_Combo_Coberturas(request, idTipoSeguro): # Método que busca las coberturas ligadas al id tipo seguro.
    dajax = Dajax()
    try:
        coberturasTipoSeguro = Cobertura.objects.using('catalogos').filter(TipoSeguro_id = idTipoSeguro)
        datos = list()
        
        for cobertura in coberturasTipoSeguro:
            datos.append({'IdCobertura':cobertura.IdCobertura, 'Descripcion':cobertura.Descripcion})          
    
    except:
        return dajax.json()
    
    return simplejson.dumps({'coberturas':datos})

@dajaxice_register
def guardar_programas(request, formulario, coberturas, folio, areaInfluencia):# Método que recibe el formulario de programas obtenido de programa.html y lo deserializa para obtener la información de sus controles y lo valida con ProgramaForm, si la información es valida guarda los datos y limpia los controles del formulario mediante una función de js.
    dajax = Dajax()
            
    formulario_deserializado = deserialize_form(formulario)              
        
    datos = {'IdTipoSeguro':formulario_deserializado.get('IdTipoSeguro'), 'IdSubTipoSeguro':formulario_deserializado.get('IdSubTipoSeguro'),
             'IdTipoMoneda':formulario_deserializado.get('IdTipoMoneda'), 'Ejercicio':formulario_deserializado.get('Ejercicio'), 
             'Observaciones':formulario_deserializado.get('Observaciones'), 'PersonaHabilitador': formulario_deserializado.get('varIdHabilitador')}
    formulario = ProgramaForm(datos)
        
    if formulario.is_valid():       
    
        if formulario_deserializado.get('varIdPrograma') == '': 
            
            fechaPrograma = datetime.datetime.now()
            
            programaAGuardar = Programa(IdTipoSeguro = formulario_deserializado.get('IdTipoSeguro'), IdSubTipoSeguro = formulario_deserializado.get('IdSubTipoSeguro'),
                                      IdTipoMoneda = formulario_deserializado.get('IdTipoMoneda'), Ejercicio = formulario_deserializado.get('Ejercicio'),
                                      FechaPrograma = fechaPrograma, Observaciones = formulario_deserializado.get('Observaciones').upper(),
                                      IdContratoFondo = formulario_deserializado.get('IdContratoFondo'), Utilizado = 0, PersonaHabilitador_id = formulario_deserializado.get('varIdHabilitador'))
            programaAGuardar.save()
            
            folioAGuardar = folio.upper() + str(programaAGuardar.IdPrograma)
            
            Programa.objects.filter(IdPrograma = programaAGuardar.IdPrograma).update(FolioPrograma = folioAGuardar)
                        
            for cobertura in coberturas:
                guardarCoberturas(cobertura, programaAGuardar.IdPrograma)                          

            for area in areaInfluencia:
                guardarAreaInfluencia(area, programaAGuardar.IdPrograma)
                                          
            dajax.add_data(folioAGuardar, 'mensajePrograma')
            
        else:
            actualizar_programa(formulario_deserializado, coberturas, areaInfluencia)                      
            dajax.script('manejadorMensajes(2);')
    
    else:
        dajax.alert('El formulario es invalido')               
         
    return dajax.json()

def guardarCoberturas(cobertura, idPrograma): # Método que permite guardar las coberturas en la base de datos pasando el id del programa para enlazar.
    dajax = Dajax()
        
    cuberturaAGuardar = CoberturaPrograma(Programa_id = idPrograma, IdCobertura = cobertura)
    cuberturaAGuardar.save()
    
    return dajax.json() 

def guardarAreaInfluencia(area, idPrograma): # Método que permite guardar el área de influencia de un programa.
    dajax = Dajax()
        
    areaInfluenciaAGuardar = AreaInfluenciaPrograma(Programa_id = idPrograma, IdAreaInfluencia = area)
    areaInfluenciaAGuardar.save()
    
    return dajax.json()

def actualizar_coberturas(coberturas, idPrograma): # Método que permite actualizar las coberturas en la base de datos.
    dajax = Dajax()
        
    coberturasGuardadas = CoberturaPrograma.objects.filter(Programa_id = idPrograma)    
        
    encontradoAElimiar = 1
    for coberturaAEliminar in coberturasGuardadas:
        for coberturaABuscar in coberturas:
            if coberturaABuscar == coberturaAEliminar.IdCobertura:  
                encontradoAElimiar = 0              
                break        
        if encontradoAElimiar == 1:
            eliminar_cobertura(coberturaAEliminar.IdCoberturaPrograma)
            
        
    coberturaAGuardar = 1   
    for cobertura in coberturas:
        for coberturaEncontrada in coberturasGuardadas:
            if coberturaEncontrada.IdCobertura == cobertura:
                coberturaAGuardar = 0
                break
        
        if coberturaAGuardar == 1:     
            guardarCoberturas(cobertura, idPrograma)
        
    return dajax.json()

def actualizar_area_influencia_programa(areaInfluencia, idPrograma): # Método que permite actualizar las coberturas en la base de datos.
    dajax = Dajax()
        
    areaInfluenciaGuardadas = AreaInfluenciaPrograma.objects.filter(Programa_id = idPrograma)    
        
    encontradoAElimiar = 1
    for areaProgramaAEliminar in areaInfluenciaGuardadas:
        for area in areaInfluencia:
            if area == areaProgramaAEliminar.IdAreaInfluencia:  
                encontradoAElimiar = 0
                break        
        if encontradoAElimiar == 1:
            eliminar_area_influencia_programa(areaProgramaAEliminar.IdAreaInfluenciaPrograma)            
        
    coberturaAGuardar = 1   
    for area in areaInfluencia:
        for areaProgramaGuardada in areaInfluenciaGuardadas:
            if areaProgramaGuardada.IdAreaInfluencia == area:
                coberturaAGuardar = 0
                break        
        if coberturaAGuardar == 1:     
            guardarAreaInfluencia(area, idPrograma)
                    
    return dajax.json()


@dajaxice_register
def eliminar_area_influencia_programa(idAreaInfluenciaPrograma): #Método que recibe el id cobertura programa para eliminarlo de la base de datos. 
    dajax = Dajax()
    AreaInfluenciaPrograma.objects.filter(IdAreaInfluenciaPrograma = idAreaInfluenciaPrograma).delete()
    
    return dajax.json()

@dajaxice_register
def eliminar_cobertura(idCoberturaPrograma): #Método que recibe el id cobertura programa para eliminarlo de la base de datos. 
    dajax = Dajax()
    CoberturaPrograma.objects.filter(IdCoberturaPrograma = idCoberturaPrograma).delete()
    
    return dajax.json()

def actualizar_programa(formularioPrograma, coberturas, areaInfluencia): # Método que permite actualizar los datos del programa.
    dajax = Dajax()
                 
    Programa.objects.filter(IdPrograma = formularioPrograma.get('varIdPrograma')).update(
                            IdTipoSeguro = formularioPrograma.get('IdTipoSeguro'), IdSubTipoSeguro = formularioPrograma.get('IdSubTipoSeguro'),
                            Ejercicio = str(formularioPrograma.get('Ejercicio')), IdTipoMoneda = formularioPrograma.get('IdTipoMoneda'), 
                            Observaciones = formularioPrograma.get('Observaciones').upper(), IdContratoFondo = formularioPrograma.get('IdContratoFondo'),
                            PersonaHabilitador = formularioPrograma.get('varIdHabilitador'))
    
    actualizar_coberturas(coberturas, formularioPrograma.get('varIdPrograma'))
    actualizar_area_influencia_programa(areaInfluencia, formularioPrograma.get('varIdPrograma'))
    
    return dajax.json()

@dajaxice_register
def obtener_programas(req): # Función que busca todos los programas ingresados a la base de datos para mostrarlos en el listado de programas.
    dajax = Dajax()
    try:
        datos = list()
        listaProgramas = Programa.objects.all().order_by("-IdPrograma")
        tieneCotizador = 0
        
        for programa in listaProgramas:
            tipoSeguro = TipoSeguro.objects.using('catalogos').filter(IdTipoSeguro = programa.IdTipoSeguro)[0]    
            subTipoSeguro = SubTipoSeguro.objects.using('catalogos').filter(IdSubTipoSeguro = programa.IdSubTipoSeguro)[0] 
            contrato = ContratoFondo.objects.filter(IdContratoFondo = programa.IdContratoFondo)[0]
            cotizadores = Cotizador.objects.filter(Programa_id = programa.IdPrograma)
            
            if cotizadores:
                tieneCotizador = 1
                 
            datos.append({'IdPrograma':programa.IdPrograma,'TipoSeguro':tipoSeguro.DescripcionTipoSeguro,'SubTipoSeguro':subTipoSeguro.DescripcionSubTipoSeguro,
            'Ejercicio':programa.Ejercicio,'IdTipoSeguro':programa.IdTipoSeguro,'IdSubTipoSeguro':programa.IdSubTipoSeguro, 
            'IdTipoMoneda':programa.IdTipoMoneda,'Observaciones':programa.Observaciones,'NumeroContrato':contrato.NumeroContrato,'FolioPrograma':programa.FolioPrograma, 
            'Utilizado':programa.Utilizado, 'TieneCotizador':int(tieneCotizador)})                       
   
    except:
        return dajax.json()
    
    return simplejson.dumps({'programas':datos})

@dajaxice_register
def obtener_areas_infuencia_fondo(req): # Función que busca todos los programas ingresados a la base de datos para mostrarlos en el listado de programas.
    dajax = Dajax()
    try:
        datos = list()
        listaAreaInfluencia = AreaInfluencia.objects.all()
        
        for areaInfluencia in listaAreaInfluencia:              
            municipio = Municipio.objects.using('catalogos').filter(IdMunicipio = areaInfluencia.Municipio_id)[0]
                 
            datos.append({'IdAreaInfluencia':areaInfluencia.IdAreaInfluencia,'Descripcion':municipio.Descripcion})
    
    except:
        return dajax.json()
    
    return simplejson.dumps({'areasInfluencia':datos})

@dajaxice_register
def buscar_programas_ejercicio_actual(req, buscarPrograma, tipoSolicitud): # Función que busca todos los programas con cotizador ingresados a la base de datos para mostrarlos en el listado de programas.
    dajax = Dajax()
    try:
        datos = list()
        year = datetime.datetime.now().year
        
        programasFiltrados = TipoSeguro.objects.using('catalogos').filter(Q(DescripcionTipoSeguro__contains = buscarPrograma))
        listaProgramas = Programa.objects.filter(Ejercicio = year, Utilizado=1)
        
        for programaFiltrado in programasFiltrados:
            for programa in listaProgramas:
                # tipoSolicitud = 1 ANUAL, tipoSolicitud = 2 A DECLARACION
                # ANUAL solo muestra los programas PATRIMONIAL y MAQUINARIA
                # A DECLARACION muestra programas PATRIMONIAL (BODEGAS, SILOS Y CONTENIDOS), TRANSPORTE Y RIESGOS ALGODONEROS
                if programaFiltrado.IdTipoSeguro == int(programa.IdTipoSeguro) and (((programaFiltrado.IdTipoSeguro == 1 or programaFiltrado.IdTipoSeguro == 3) and tipoSolicitud==1) or ((programaFiltrado.IdTipoSeguro == 1 or programaFiltrado.IdTipoSeguro == 2 or programaFiltrado.IdTipoSeguro == 4) and tipoSolicitud==2)):
                    tipoSeguro = TipoSeguro.objects.using('catalogos').filter(IdTipoSeguro = programa.IdTipoSeguro)[0]    
                    subTipoSeguro = SubTipoSeguro.objects.using('catalogos').filter(IdSubTipoSeguro = programa.IdSubTipoSeguro)[0] 
                    contrato = ContratoFondo.objects.filter(IdContratoFondo = programa.IdContratoFondo)[0]
                    descripcionMoneda = Moneda.objects.using('catalogos').filter(IdMoneda = programa.IdTipoMoneda)[0]
                
                    datos.append({'IdPrograma':programa.IdPrograma,'TipoSeguro':tipoSeguro.DescripcionTipoSeguro,'SubTipoSeguro':subTipoSeguro.DescripcionSubTipoSeguro,
                    'Ejercicio':programa.Ejercicio,'IdTipoSeguro':programa.IdTipoSeguro,'IdSubTipoSeguro':programa.IdSubTipoSeguro, 'DescripcionMoneda':descripcionMoneda.Nombre,
                    'IdTipoMoneda':programa.IdTipoMoneda,'Observaciones':programa.Observaciones, 'NumeroContrato':contrato.NumeroContrato,'FolioPrograma':programa.FolioPrograma})
                    
    except:
        return dajax.json()
    
    return simplejson.dumps({'programas':datos})  

@dajaxice_register
def obtener_programas_ejercicio_actual(req): # Método ue busca todos los programas del ciclo actual pasandole el año.
    dajax = Dajax()    
    
    try:
        datos = list()
        year = datetime.datetime.now().year
        programasEjercicioActual = Programa.objects.filter(Ejercicio = year, Utilizado = 0)
        
        for programa in programasEjercicioActual:  
            tipoSeguro = TipoSeguro.objects.using('catalogos').filter(IdTipoSeguro = programa.IdTipoSeguro)[0]    
            subTipoSeguro = SubTipoSeguro.objects.using('catalogos').filter(IdSubTipoSeguro = programa.IdSubTipoSeguro)[0] 
            descripcionMoneda = Moneda.objects.using('catalogos').filter(IdMoneda = programa.IdTipoMoneda)[0]
            
            datos.append({'IdPrograma':programa.IdPrograma,'TipoSeguro':tipoSeguro.DescripcionTipoSeguro,'SubTipoSeguro':subTipoSeguro.DescripcionSubTipoSeguro,
            'Ejercicio':programa.Ejercicio,'IdTipoMoneda':programa.IdTipoMoneda,'FolioPrograma':programa.FolioPrograma,'DescripcionMoneda':descripcionMoneda.Descripcion})
    
    except:
        return dajax.json()
    
    return simplejson.dumps({'programasActuales':datos}) 

@dajaxice_register
def buscar_programa(request, idPrograma): # Método que busca la información del programa pasandole el id del programa a buscar.
    dajax = Dajax()
    
    try:
        programasEncontrados = Programa.objects.filter(IdPrograma = idPrograma)
        datos = list()
        for programa in programasEncontrados:        
            persona = Persona.objects.filter(IdPersona = programa.PersonaHabilitador_id)[0]   
            contrato = ContratoFondo.objects.filter(IdContratoFondo = programa.IdContratoFondo)[0]
            tipoSeguro = TipoSeguro.objects.using('catalogos').filter(IdTipoSeguro = programa.IdTipoSeguro)[0]
            subTipoSeguro = SubTipoSeguro.objects.using('catalogos').filter(IdSubTipoSeguro = programa.IdSubTipoSeguro)[0]             
            datos.append({'IdPrograma':programa.IdPrograma, 'IdTipoSeguro': programa.IdTipoSeguro,'IdSubSeguro':programa.IdSubTipoSeguro, 
                          'IdTipoMoneda':programa.IdTipoMoneda, 'Ejercicio':programa.Ejercicio, 'Observaciones':programa.Observaciones, 
                          'IdContratoFondo':programa.IdContratoFondo, 'Utilizado':programa.Utilizado, 'RazonSocial':persona.RazonSocial, 
                          'IdPersona':persona.IdPersona, 'NumeroContrato':contrato.NumeroContrato,'TipoSeguro':tipoSeguro.DescripcionTipoSeguro, 
                          'SubTipoSeguro':subTipoSeguro.DescripcionSubTipoSeguro, 'FolioPrograma':programa.FolioPrograma})           
    
    except:
        return dajax.json()
    
    return simplejson.dumps({'programaEncontrado':datos})

@dajaxice_register
def buscar_cobertura_programa(request, idPrograma): # Método que busca la información del programa pasandole el id del programa a buscar.
    dajax = Dajax()
    
    try:
        coberturasPrograma = CoberturaPrograma.objects.filter(Programa_id = idPrograma)
        datos = list()
        for cobertura in coberturasPrograma:
            datos.append({'IdCobertura':cobertura.IdCobertura})
    
    except:
        return dajax.json()
    
    return simplejson.dumps({'coberturasprograma':datos})

@dajaxice_register
def buscar_cobertura_programa_descripcion(request, idPrograma): # Método que busca la información de las coberturas pasandole el id del programa a buscar.
    dajax = Dajax()
    
    try:
        coberturasPrograma = CoberturaPrograma.objects.filter(Programa_id = idPrograma)
        datos = list()
        for cobertura in coberturasPrograma:
            coberturaCatalogos = Cobertura.objects.using('catalogos').filter(IdCobertura = cobertura.IdCobertura)[0]
            datos.append({'Descripcion':coberturaCatalogos.Descripcion})
                
    except:
        return dajax.json()
    
    return simplejson.dumps({'coberturasprograma':datos})

@dajaxice_register
def buscar_area_influencia_descripcion(request, idPrograma): # Método que busca la información de las areas de influencia pasandole el id del programa a buscar.
    dajax = Dajax()
    
    try:
        areaInfluenciaPrograma = AreaInfluenciaPrograma.objects.filter(Programa_id = idPrograma)
        datos = list()
        for areaInfluencia in areaInfluenciaPrograma:
            areaCatalogo = AreaInfluencia.objects.filter(IdAreaInfluencia = areaInfluencia.IdAreaInfluencia)[0]
            municipio = Municipio.objects.using('catalogos').filter(IdMunicipio = areaCatalogo.Municipio_id)[0]
            datos.append({'Descripcion':municipio.Descripcion})
                
    except:
        return dajax.json()
    
    return simplejson.dumps({'areasInfluenciaDescripcion':datos}) 

@dajaxice_register
def obtener_cobertura_con_idprograma(req, idPrograma): # Método que obtiene de la base de datos las coberturas pasandole el id de programa y buscando la descripcion en los catalogos.
    dajax = Dajax()
    
    try:
        coberturasProgramas = CoberturaPrograma.objects.filter(Programa_id = idPrograma)
        datos = list()
        
        for coberturaPrograma in coberturasProgramas:
            coberturaCatalogo = Cobertura.objects.using('catalogos').filter(IdCobertura = coberturaPrograma.IdCobertura)[0]
            
            remocion = 0
            if coberturaPrograma.IdCobertura == 3:
                remocion = 1            
            
            datos.append({'IdCoberturaPrograma':coberturaPrograma.IdCoberturaPrograma,'Descripcion':coberturaCatalogo.Descripcion, 'Remocion':remocion})
    
    except:
        return dajax.json()
    
    return simplejson.dumps({'coberturasPorPrograma':datos})
    
@dajaxice_register
def obtener_area_influencia_con_idprograma(req, idPrograma): # Método que obtiene de la base de datos el área de influencia del programa pasando el id del mismo.
    dajax = Dajax()
    
    try:
        areaInfluenciaPrograma = AreaInfluenciaPrograma.objects.filter(Programa_id = idPrograma)
        datos = list()
        
        for area in areaInfluenciaPrograma:
            datos.append({'IdAreaInfluenciaPrograma':area.IdAreaInfluenciaPrograma,'IdAreaInfluencia':area.IdAreaInfluencia})
    
    except:
        return dajax.json()
    
    return simplejson.dumps({'areaInfluenciaPrograma':datos})

@dajaxice_register
def eliminar_programa(request, idPrograma): #Función que permite eliminar el programa seleccionado de la base de datos.
    dajax = Dajax()
    Programa.objects.filter(IdPrograma = idPrograma).delete()
    
    return dajax.json()

@dajaxice_register
def programaUtilizado(request, idPrograma): #Función que permite verificar si un programa se encuentra con cotizador, la función devuelve un 0 si no esta utilizado y un 1 si esta utilizado.
    
    tieneCotizador = 0
    
    cotizadores = Cotizador.objects.filter(Programa_id = idPrograma)
    
    if cotizadores:
        tieneCotizador = 1
    
    return simplejson.dumps({'tieneCotizador':tieneCotizador})
