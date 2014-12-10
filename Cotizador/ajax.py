#encoding:utf-8
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from Cotizador.forms import CotizadorForm
from dajaxice.utils import deserialize_form
from dajax.core import Dajax
from Cotizador.models import Cotizador, CotizadorCobertura
from Programas.models import Programa, TipoSeguro, SubTipoSeguro, Cobertura,\
    CoberturaPrograma
from decimal import Decimal

@dajaxice_register
def guardar_cotizador(request, formulario, coberturas, prima, tarifaTotal):# Método que recibe el formulario de cotizador obtenido de cotizador.html y lo deserializa para obtener la información de sus controles y lo valida con CotizadorForm, si la información es valida guarda los datos y limpia los controles del formulario mediante una función de js.
    dajax = Dajax()
    
    if coberturas == '':
        list_Coberturas = ''
    else:
        array_convertido_string = simplejson.dumps(coberturas, separators=('|',','))
        list_Coberturas = array_convertido_string.replace('[', '').replace(']', '').replace('"', '').split(';')      
    
    formulario_deserializado = deserialize_form(formulario)
    
    datos = {'PorcentajeFondo':formulario_deserializado.get('PorcentajeFondo'), 'PorcentajeReaseguro':formulario_deserializado.get('PorcentajeReaseguro')}
    formulario = CotizadorForm(datos)
    
    if formulario.is_valid():
        if formulario_deserializado.get('varIdCotizador') == '':
            
            folioAGuardar = "C/" + str(formulario_deserializado.get('txtFolio'))
            
            if tarifaTotal == '':
                tarifa = 0
            else:
                tarifa = tarifaTotal
            
            cotizadorAGuardar = Cotizador(Programa_id = formulario_deserializado.get('varIdPrograma'), PorcentajeFondo = formulario_deserializado.get('PorcentajeFondo'),
                                       PorcentajeReaseguro = formulario_deserializado.get('PorcentajeReaseguro'), Prima = prima, FolioCotizador = folioAGuardar, 
                                       TotalTarifa = Decimal(str(tarifa)), Vigencia = str(formulario_deserializado.get('cmdVigencia')))
            cotizadorAGuardar.save()
            
            Programa.objects.filter(IdPrograma = cotizadorAGuardar.Programa_id).update(Utilizado = 1)
            
            if list_Coberturas != '':
                for cobertura in list_Coberturas:
                    guardar_cotizador_cobertura(cobertura, cotizadorAGuardar.IdCotizador)
            
            dajax.add_data(folioAGuardar, 'mensajeCotizador')
   
        else:
            actualizar_cotizador(formulario_deserializado, list_Coberturas, prima) 
            dajax.script('actualizarVariableIdProgramaAnterior();')
    else:
        dajax.alert('Formulario invalido')
         
    return dajax.json()

def actualizar_cotizador(formularioCotizador, cotizadorCoberturas, prima): # Método que permite actualizar los datos del programa.
    dajax = Dajax()
                 
    folioAGuardar = "C/" + str(formularioCotizador.get('txtFolio'))
             
    if formularioCotizador.get('varTotalTarifa') == '':
        tarifa = 0
    else:
        tarifa = formularioCotizador.get('varTotalTarifa')     
             
    Cotizador.objects.filter(IdCotizador = int(formularioCotizador.get('varIdCotizador'))).update(
                             Programa = formularioCotizador.get('varIdPrograma'), PorcentajeFondo = formularioCotizador.get('PorcentajeFondo'),
                             PorcentajeReaseguro = formularioCotizador.get('PorcentajeReaseguro'), Prima = prima, FolioCotizador = folioAGuardar, 
                             TotalTarifa = Decimal(str(tarifa)))
    
    Programa.objects.filter(IdPrograma = formularioCotizador.get('varIdPrograma')).update(Utilizado = 1)
        
    actualizar_cotizador_coberturas(cotizadorCoberturas, formularioCotizador.get('varIdCotizador'))
    
    if formularioCotizador.get('varIdPrograma') != formularioCotizador.get('varIdProgramaAnterior') and formularioCotizador.get('varIdProgramaAnterior') != '':
        Programa.objects.filter(IdPrograma = formularioCotizador.get('varIdProgramaAnterior')).update(Utilizado = 0)
            
    return dajax.json()

def actualizar_cotizador_coberturas(coberturas, idCotizador): # Método que permite actualizar las coberturas de la cotización en la base de datos.
    dajax = Dajax()
    
    cotizadorCoberturasGuardadas = CotizadorCobertura.objects.filter(Cotizador_id = idCotizador)    
     
    encontradoAEliminar = 1
    for cotizadorCoberturaAEliminar in cotizadorCoberturasGuardadas:
        for coberturaABuscar in coberturas:
            list_cotizador_cobertura = coberturaABuscar.split(',')
            if str(list_cotizador_cobertura[4]) == str(cotizadorCoberturaAEliminar.IdCotizadorCobertura):  
                encontradoAEliminar = 0    
                break
        if encontradoAEliminar == 1:
            eliminar_cotizador_cobertura(cotizadorCoberturaAEliminar.IdCotizadorCobertura)
    
    for cobertura in coberturas:
        list_cotizador_cobertura = cobertura.split(',')
        if str(list_cotizador_cobertura[4]) == '':
            guardar_cotizador_cobertura(cobertura, idCotizador)
        else:
            guardar_actualizar_cotizador_cobertura(cobertura)
    
    return dajax.json()

def guardar_actualizar_cotizador_cobertura(cotizadorCobertura): # Función que recibe una entidad con la información de teléfono y un id de persona para almacenarlos en la base de datos.
    dajax = Dajax()
    
    list_cotizador_cobertura = cotizadorCobertura.split(',')
    
    if len(list_cotizador_cobertura) == 8:
        remocion = 0
    else:
        remocion = list_cotizador_cobertura[8]
    
    CotizadorCobertura.objects.filter(IdCotizadorCobertura = int(list_cotizador_cobertura[4])).update(
                             Tarifa = list_cotizador_cobertura[5], Fondo = list_cotizador_cobertura[2],
                             Reaseguro = list_cotizador_cobertura[3], Remocion = remocion,
                             Deducible = list_cotizador_cobertura[6], ParticipacionAPerdida = list_cotizador_cobertura[7])
        
    return dajax.json()

@dajaxice_register
def eliminar_cotizador_cobertura(idCotizadorCobertura): #Método que recibe el id cotizador cobertura para eliminarlo de la base de datos. 
    dajax = Dajax()
    CotizadorCobertura.objects.filter(IdCotizadorCobertura = idCotizadorCobertura).delete()
    
    return dajax.json()

def guardar_cotizador_cobertura(cotizadorCobertura, idCotizador): # Función que recibe una entidad con la información de teléfono y un id de persona para almacenarlos en la base de datos.
    dajax = Dajax()
    
    list_cotizador = cotizadorCobertura.split(',')
    
    if len(list_cotizador) == 8:
        remocion = 0
    else:
        remocion = list_cotizador[8]
    
    cobertura = CotizadorCobertura(Cotizador_id = idCotizador, CoberturaPrograma_id = list_cotizador[0], Tarifa = list_cotizador[5], Fondo = list_cotizador[2], Reaseguro = list_cotizador[3], Deducible = list_cotizador[6], ParticipacionAPerdida = list_cotizador[7], Remocion = remocion)
    cobertura.save()
        
    return dajax.json()

@dajaxice_register
def obtener_cotizaciones(req): # Método que obtiene de la base de datos las cotizaciones.
    dajax = Dajax()
    
    try:
        cotizaciones = Cotizador.objects.all().order_by('-IdCotizador')
        datos = list()
        
        for cotizador in cotizaciones:
            programa = Programa.objects.filter(IdPrograma = cotizador.Programa_id)[0]       
            datos.append({'IdCotizador':cotizador.IdCotizador,'PorcentajeFondo':cotizador.PorcentajeFondo,'PorcentajeReaseguro':cotizador.PorcentajeReaseguro,'Prima':cotizador.Prima,'FolioPrograma':programa.FolioPrograma,'FolioCotizador':cotizador.FolioCotizador})
    
    except:
        return dajax.json()
    
    return simplejson.dumps({'cotizaciones':datos})

@dajaxice_register
def buscar_cotizador(request, idCotizador): # Método que busca la información del cotizador pasandole el id cotizador a buscar.
    dajax = Dajax()
    
    try:
        cotizadorEncontrado = Cotizador.objects.filter(IdCotizador = idCotizador)
        datos = list()
        for cotizador in cotizadorEncontrado:        
            programa = Programa.objects.filter(IdPrograma = cotizador.Programa_id)[0]            
            tipoSeguro = TipoSeguro.objects.using('catalogos').filter(IdTipoSeguro = programa.IdTipoSeguro)[0]
            subTipoSeguro = SubTipoSeguro.objects.using('catalogos').filter(IdSubTipoSeguro = programa.IdSubTipoSeguro)[0]
            datos.append({'IdCotizador':cotizador.IdCotizador,'IdPrograma': cotizador.Programa_id,'PorcentajeFondo':cotizador.PorcentajeFondo, 
                          'PorcentajeReaseguro':cotizador.PorcentajeReaseguro,'Prima':cotizador.Prima,'TipoSeguro':tipoSeguro.DescripcionTipoSeguro,
                          'SubTipoSeguro':subTipoSeguro.DescripcionSubTipoSeguro,'IdTipoMoneda':programa.IdTipoMoneda,'FolioPrograma':programa.FolioPrograma,
                          'FolioCotizador': cotizador.FolioCotizador,'Vigencia':cotizador.Vigencia})
    
    except:
        return dajax.json()
    
    return simplejson.dumps({'cotizadorEncontrado':datos})

@dajaxice_register
def buscar_cotizador_cobertura(request, idCotizador): # Método que busca la información del cotizador con sus coberturas pasandole el id cotizador a buscar.
    dajax = Dajax()
    
    try:
        coberturasCotizador = CotizadorCobertura.objects.filter(Cotizador_id = idCotizador)
        datos = list()
        for coberturaCotizador in coberturasCotizador:
            coberturaPrograma = CoberturaPrograma.objects.filter(IdCoberturaPrograma = coberturaCotizador.CoberturaPrograma_id)[0]
            cobertura = Cobertura.objects.using('catalogos').filter(IdCobertura = coberturaPrograma.IdCobertura)[0]            
            datos.append({'IdCoberturaPrograma':coberturaCotizador.CoberturaPrograma_id,'Descripcion': cobertura.Descripcion,'Tarifa':str(coberturaCotizador.Tarifa), 
                          'Fondo':str(coberturaCotizador.Fondo),'Reaseguro':str(coberturaCotizador.Reaseguro),'IdCotizadorCobertura':coberturaCotizador.IdCotizadorCobertura, 'Remocion':str(coberturaCotizador.Remocion),
                          'Deducible':str(coberturaCotizador.Deducible), 'ParticipacionAPerdida':str(coberturaCotizador.ParticipacionAPerdida)})
    except:
        return dajax.json()
    
    return simplejson.dumps({'cotizadorEncontrado':datos})

@dajaxice_register
def eliminar_cotizador(request, idCotizador): # Método que recibe el id del cotizador para eliminarlo de la base de datos y eliminar los cotizadores de las coberturas.. 
    dajax = Dajax()
    
    cotizadorAEliminar = Cotizador.objects.filter(IdCotizador = idCotizador)
    Programa.objects.filter(IdPrograma = cotizadorAEliminar[0].Programa_id).update(Utilizado = 0)
    cotizadorAEliminar[0].delete()
    cotizadoresCoberturas = CotizadorCobertura.objects.filter(Cotizador_id = idCotizador)
    
    for cotizador in cotizadoresCoberturas:
        cotizador.delete()
    
    return dajax.json()