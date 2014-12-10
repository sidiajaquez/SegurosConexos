from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'GuardarDictamenSiniestro/$', 'Siniestro.views.guardarDictamenSiniestro'),
                       url(r'ListadoDictamenSiniestro/$', 'Siniestro.views.listadoDictamenSiniestro'),
                       url(r'DictamenSiniestro/(?P<id_ActaSiniestro>\d+)$', 'Siniestro.views.dictamenSiniestro', name='DictamenSiniestro'),
)