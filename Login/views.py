#encoding:utf-8
import json

from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

import django.conf as conf

def login(request): #Metodo para identificar los login del sistema
    if 'next' in request.GET:
        next = request.GET['next']
    else:
        next = "/"
    
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username = usuario, password = clave)
            if acceso is not None:
                if acceso.is_active:                    
                    auth_login(request,acceso) #I use an alias for avoid troubles with this method
                    usuarioFondo = User.objects.get(username=usuario)
                    conf.settings.DATABASES['siobicx']['NAME'] = usuarioFondo.usuariofondo.BaseDatos
                    return HttpResponseRedirect(next)
                else:
                    return render(request,'login.html',{'formulario':formulario, 'next':next,'deactivate':True})
            else:
                return render(request,'login.html',{'formulario':formulario, 'next':next,'denied':True})
                
    else:
        formulario = AuthenticationForm()
    
    return render(request,'login.html',{'formulario':formulario, 'next':next})

@login_required()
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

@login_required()
def settingsUser(request): #Metodo para el cambio de password del usuario
    if request.is_ajax():
        if request.POST['data']:
            userdata = json.loads(request.POST['data'])
            usuario = User.objects.get(username__exact=userdata['username'])
            usuario.set_password(userdata['pw'])
            usuario.save()
            return HttpResponse (json.dumps({'mensaje':'Datos actualizados correctamente'}), content_type="application/json; charset=utf8")
    else:    
        return render(request, 'settingsuser.html', {'usuario':request.user,'database':conf.settings.DATABASES['siobicx']['NAME']})