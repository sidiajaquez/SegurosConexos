# Create your views here.
from Cotizador.forms import CotizadorForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Cotizador.models import VigenciaCotizador, Cotizador, CotizadorCobertura
from Programas.models import Programa, TipoSeguro, SubTipoSeguro,\
    CoberturaPrograma, Cobertura
from ConexosAgropecuarios.models import Moneda
from Solicitud.models import Solicitud

@login_required()
def cotizadores(request):
    return render(request, 'listadocotizadores.html',{'usuario':request.user})

@login_required()
def reporteCotizador(request):
    return render(request, 'reportecotizador.html',{'usuario':request.user})

@login_required()
def cotizador(request): #manda llamar a cotizador.html renderizando el formulario de CotizadorForm en la variable formulario, sin la generacion de los campos con prefixo inicial id_
    
    catalogoVigencia = VigenciaCotizador.objects.using('catalogos').all()
    readOnly = 0
    idCotizador = ""
               
    return render(request,'cotizador.html', {'formulario_cotizador':CotizadorForm(auto_id='%s'), 'readOnly':readOnly, 'idCotizador':idCotizador, 'catalogoVigencia':catalogoVigencia,'usuario':request.user})

@login_required()
def cotizadorEditar(request, id_cotizador): # Clase que nos permite editar el cotizador mediante el id.
    datosCoberturas = list()
    varEsRemocion = 0
    varTotalTarifaCobertura = 0
    varTotalFondo = 0
    varTotalReaseguro = 0
    readOnly = 0
    
    catalogoVigencia = VigenciaCotizador.objects.using('catalogos').all()
    cotizadorEncontrado = Cotizador.objects.filter(IdCotizador = id_cotizador)[0]
    coberturasCotizadores = CotizadorCobertura.objects.filter(Cotizador_id = id_cotizador)
    programaEncontrado = Programa.objects.filter(IdPrograma = cotizadorEncontrado.Programa_id)[0]
    tipoSeguroEncontrado = TipoSeguro.objects.using('catalogos').filter(IdTipoSeguro = programaEncontrado.IdTipoSeguro)[0]
    subTipoSeguroEncontrado = SubTipoSeguro.objects.using('catalogos').filter(IdSubTipoSeguro = programaEncontrado.IdSubTipoSeguro)[0]
    monedaEncontrada = Moneda.objects.using('catalogos').filter(IdMoneda = programaEncontrado.IdTipoMoneda)[0]
    
    solicitudesCotizador = Solicitud.objects.filter(Programa_id = programaEncontrado.IdPrograma)
    
    if solicitudesCotizador:
        readOnly = 1
    
    for coberturaCotizador in coberturasCotizadores:
        coberturaPrograma = CoberturaPrograma.objects.filter(IdCoberturaPrograma = coberturaCotizador.CoberturaPrograma_id)[0]
        cobertura = Cobertura.objects.using('catalogos').filter(IdCobertura = coberturaPrograma.IdCobertura)[0]
        
        varTotalTarifaCobertura =  varTotalTarifaCobertura + coberturaCotizador.Tarifa
        varTotalFondo = varTotalFondo + coberturaCotizador.Fondo
        varTotalReaseguro = varTotalReaseguro + coberturaCotizador.Reaseguro
        
        if cobertura.IdCobertura == 3:
            varEsRemocion = 1
                 
        datosCoberturas.append({'IdCoberturaPrograma':coberturaCotizador.CoberturaPrograma_id,'Descripcion': cobertura.Descripcion,'Tarifa':str(coberturaCotizador.Tarifa), 
                      'Fondo':str(coberturaCotizador.Fondo),'Reaseguro':str(coberturaCotizador.Reaseguro),'IdCotizadorCobertura':coberturaCotizador.IdCotizadorCobertura, 'Remocion':str(coberturaCotizador.Remocion),
                      'Deducible':str(coberturaCotizador.Deducible), 'ParticipacionAPerdida':str(coberturaCotizador.ParticipacionAPerdida), 'IdCobertura':cobertura.IdCobertura})
     
    return render(request,'cotizador.html', {'idCotizador':cotizadorEncontrado.IdCotizador, 'cotizador':cotizadorEncontrado, 'programa':programaEncontrado, 'catalogoVigencia':catalogoVigencia, 'tipoSeguro':tipoSeguroEncontrado.DescripcionTipoSeguro,
                                             'subTipoSeguro':subTipoSeguroEncontrado.DescripcionSubTipoSeguro, 'moneda':monedaEncontrada.Nombre, 'coberturasCotizadores':coberturasCotizadores,
                                             'coberturas':datosCoberturas, 'esRemocion':varEsRemocion, 'varTotalTarifa':varTotalTarifaCobertura, 'varTotalFondo':varTotalFondo,
                                             'varTotalReaseguro':varTotalReaseguro, 'readOnly':readOnly, 'usuario':request.user})