from ConexosAgropecuarios.forms import PersonaFisicaForm, PersonaMoralForm, RegistroFondoForm, CuentaBancoForm, ContratoFondoForm, ConsejoAdminsitracionForm, PersonalApoyoForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from ConexosAgropecuarios.models import Estado

@login_required()
def handler404(request):
    return render(request,'404.html')

@login_required()
def inicio(request):
    return render(request,'home.html', {'usuario':request.user}, context_instance=RequestContext(request))

@login_required()
def personaFisica(request):# Llama a la plantilla fisica.html pasando el formulario PersonaFisicaForm en la variable persona_Form. 
    return render(request,'personas/fisica.html', { 'persona_Form': PersonaFisicaForm(auto_id='%s'),'usuario':request.user})

@login_required()
def personaMoral(request): #manda llamar a moral.html renderizando el formulario de PersonaMoralForm en la variable formulario, sin la generacion de los campos con prefixo inicial id_
    return render(request,'personas/moral.html', {'formulario':PersonaMoralForm(auto_id='%s'),'usuario':request.user})

@login_required()
def datosFondo(request): #manda llamar a datosFondo.html
    tiposEstados = Estado.objects.using('catalogos').all()
     
    return render(request,'fondo/datosFondo.html', {'Estados':tiposEstados,'formulario_RegistroFondo':RegistroFondoForm(auto_id='%s'), 'formulario_CuentaBanco':CuentaBancoForm(auto_id='%s'), 'formulario_ContratoFondo':ContratoFondoForm(auto_id='%s'), 'formulario_ConsejoAdministracion':ConsejoAdminsitracionForm(auto_id='%s'), 'formulario_PersonalApoyo':PersonalApoyoForm(auto_id='%s'),
                                                    'usuario':request.user})