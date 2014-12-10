from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'ExportarExcelBordereaux/(?P<IdContratoFondo>\d+)/(?P<IdTipoMoneda>\d+)/(?P<FechaInicio>[\d-]+)/(?P<FechaFinal>[\d-]+)$', 'Reporteador.views.exportarExcelBordereaux'), #la expresion [\d-] es para que acepte cualquier digito de 0-9 y el "-"
                       url(r'ReporteBordereaux/$', 'Reporteador.views.reporteBordereaux'),
)