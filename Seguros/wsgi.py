"""
WSGI config for Seguros project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
#Importa site para agregar el directorio donde se encuentra la virtualizacion de python con sus paquetes
import site

#Se agrega el directorio de los paquetes virtualizados
#site.addsitedir('/home/noel/virtualenvs/SistemasSeguros/local/lib/python2.7/site-packages')

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
#os.environ["DJANGO_SETTINGS_MODULE"] = "Seguros.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.production")

#Activamos el entorno de virtualizacion que tengo en esta maquina
#activate_env = os.path.expanduser("/home/noel/virtualenvs/SistemasSeguros/bin/activate_this.py")
#execfile(activate_env, dict(__file__ = activate_env))

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
