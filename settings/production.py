from Seguros.settings import *

DEBUG = TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['localhost','192.168.0.117']

MEDIA_ROOT = '/var/www/seguros/static/img/'

MEDIA_URL = 'http://192.168.0.117:90/static/img/'

STATICFILES_DIRS = (
    '/var/www/seguros/static/',
)

#Expire the session when the user close browsers
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#SESSION_COOKIE_AGE = 600 #Seconds