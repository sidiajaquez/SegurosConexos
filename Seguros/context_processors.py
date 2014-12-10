#encoding:utf-8
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect

import django.conf as conf

def BaseDatosUsuario(request):
    if not conf.settings.DATABASES['siobicx']['NAME']:
        auth_logout(request)
        return HttpResponseRedirect('/')
    else:
        return {'database':conf.settings.DATABASES['siobicx']['NAME']}