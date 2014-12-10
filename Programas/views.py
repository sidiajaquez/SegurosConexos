# Create your views here.
from Programas.forms import ProgramaForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ConexosAgropecuarios.models import ContratoFondo, Moneda 
from Programas.models import Programa, SubTipoSeguro

@login_required()
def programas(request):
    return render(request, 'listadoprogramas.html',{'usuario':request.user})

@login_required()
def reportePrograma(request):
    return render(request, 'reporteprograma.html',{'usuario':request.user})

@login_required()
def programa(request,id_programa = None): #Vista para obtener los datos del programa segun si sea programa para modificar o programa nuevo
    tipoMonedas = list()
    if id_programa: #si se manda un id del programa se obtienen los datos para mostrarlos en el template
        informacionPrograma = Programa.objects.filter(IdPrograma = id_programa)[0]
        contratoPrograma = ContratoFondo.objects.filter(IdContratoFondo = informacionPrograma.IdContratoFondo)[0]
        subTiposSeguro = SubTipoSeguro.objects.using('catalogos').filter(TipoSeguro = informacionPrograma.IdTipoSeguro)
        
        if contratoPrograma.IdMoneda == 3:
            monedas = Moneda.objects.using('catalogos').filter(IdMoneda__in=[1,2])
            for moneda in monedas:
                tipoMonedas.append({'IdMoneda':moneda.IdMoneda,'DescripcionMoneda':moneda.Descripcion})
        else:
            moneda = Moneda.objects.using('catalogos').get(IdMoneda=contratoPrograma.IdMoneda)
            tipoMonedas.append({'IdMoneda':moneda.IdMoneda,'DescripcionMoneda':moneda.Descripcion})
    else:
        informacionPrograma = ''
        contratoPrograma = False
        subTiposSeguro = ''
    contratos = ContratoFondo.objects.all()
    return render(request, 'programa.html', {'formulario_programas':ProgramaForm(auto_id='%s'), 'contratos':contratos,'InformacionPrograma':informacionPrograma,
                                             'ContratoPrograma':contratoPrograma, 'TipoMonedas':tipoMonedas,'SubTiposSeguro':subTiposSeguro,'usuario':request.user})