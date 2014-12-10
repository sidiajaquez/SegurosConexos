# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DescripcionDetalladaBienSolicitadoActaVerificacion'
        db.create_table('DescripcionDetalladaBienSolicitadoActaVerificacion', (
            ('IdDescripcionDetalladaBienSolicitadoActaVerificacion', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('RelacionAnexaActaVerificacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Solicitud.RelacionAnexaActaVerificacion'])),
            ('NombreEquipo', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('Marca', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('Modelo', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('Serie', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('FechaBien', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('DocumentacionEvaluacion', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('Cantidad', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('ValorUnitario', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=2, blank=True)),
        ))
        db.send_create_signal(u'Solicitud', ['DescripcionDetalladaBienSolicitadoActaVerificacion'])


    def backwards(self, orm):
        # Deleting model 'DescripcionDetalladaBienSolicitadoActaVerificacion'
        db.delete_table('DescripcionDetalladaBienSolicitadoActaVerificacion')


    models = {
        u'ConexosAgropecuarios.persona': {
            'ApellidoMaterno': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'ApellidoPaterno': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'Curp': ('django.db.models.fields.CharField', [], {'max_length': '18', 'null': 'True', 'blank': 'True'}),
            'Email': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'EsSocio': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'EstadoCivil': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'FechaIngreso': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'FechaNacimiento': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'IdPersona': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'ordering': "('Rfc',)", 'object_name': 'Persona', 'db_table': "'Personas'"},
            'PrimerNombre': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'RazonSocial': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'Rfc': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'SegundoNombre': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'Sexo': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'TipoPersona': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'})
        },
        u'Programas.programa': {
            'Ejercicio': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'FechaPrograma': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'FolioPrograma': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'IdContratoFondo': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'IdPrograma': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'IdSubTipoSeguro': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            'IdTipoMoneda': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            'IdTipoSeguro': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'Programa', 'db_table': "'programas'"},
            'Observaciones': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'PersonaHabilitador': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ConexosAgropecuarios.Persona']"}),
            'Utilizado': ('django.db.models.fields.NullBooleanField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'})
        },
        u'Solicitud.actaverificacionsolicitud': {
            'DictamenInspeccion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'FechaCampo': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'FechaPrellenada': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'IdActaVerificacionSolicitud': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'ordering': "('IdActaVerificacionSolicitud',)", 'object_name': 'ActaVerificacionSolicitud', 'db_table': "'ActaVerificacionSolicitud'"},
            'Solicitud': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Solicitud.Solicitud']"})
        },
        u'Solicitud.beneficiario': {
            'IdBeneficiario': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'ordering': "('IdBeneficiario',)", 'object_name': 'Beneficiario', 'db_table': "'Beneficiario'"},
            'PersonaBeneficiario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ConexosAgropecuarios.Persona']"}),
            'Solicitud': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Solicitud.Solicitud']"})
        },
        u'Solicitud.descripciondetalladabiensolicitado': {
            'Cantidad': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'DocumentacionEvaluacion': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'FechaBien': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'IdDescripcionDetalladaBienSolicitado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Marca': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'Meta': {'ordering': "('IdDescripcionDetalladaBienSolicitado',)", 'object_name': 'DescripcionDetalladaBienSolicitado', 'db_table': "'DescripcionDetalladaBienSolicitado'"},
            'Modelo': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'NombreEquipo': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'RelacionAnexaSolicitud': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Solicitud.RelacionAnexaSolicitud']"}),
            'Serie': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'ValorUnitario': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'})
        },
        u'Solicitud.descripciondetalladabiensolicitadoactaverificacion': {
            'Cantidad': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'DocumentacionEvaluacion': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'FechaBien': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'IdDescripcionDetalladaBienSolicitadoActaVerificacion': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Marca': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'Meta': {'ordering': "('IdDescripcionDetalladaBienSolicitadoActaVerificacion',)", 'object_name': 'DescripcionDetalladaBienSolicitadoActaVerificacion', 'db_table': "'DescripcionDetalladaBienSolicitadoActaVerificacion'"},
            'Modelo': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'NombreEquipo': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'RelacionAnexaActaVerificacion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Solicitud.RelacionAnexaActaVerificacion']"}),
            'Serie': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'ValorUnitario': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'})
        },
        u'Solicitud.medidaseguridadactaverificacion': {
            'ActaVerificacionSolicitud': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Solicitud.ActaVerificacionSolicitud']"}),
            'IdMedidaSeguridad': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'MedidasSeguridad': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'Meta': {'ordering': "('IdMedidaSeguridad',)", 'object_name': 'MedidaSeguridadActaVerificacion', 'db_table': "'MedidaSeguridadActaVerificacion'"}
        },
        u'Solicitud.relacionanexaactaverificacion': {
            'DescripcionBienAsegurado': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'FechaRelacionAnexaActaVerificacion': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'IdRelacionAnexaActaVerificacion': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'ordering': "('Solicitud',)", 'object_name': 'RelacionAnexaActaVerificacion', 'db_table': "'RelacionAnexaActaVerificacion'"},
            'Solicitud': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Solicitud.Solicitud']"}),
            'UbicacionBienLat': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'UbicacionBienLng': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        u'Solicitud.relacionanexasolicitud': {
            'DescripcionBienAsegurado': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'FechaRelacionAnexa': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'IdRelacionAnexaSolicitud': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'ordering': "('Solicitud',)", 'object_name': 'RelacionAnexaSolicitud', 'db_table': "'RelacionAnexaSolicitud'"},
            'ObservacionesSolicitante': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Solicitud': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Solicitud.Solicitud']"}),
            'UbicacionBienLat': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'UbicacionBienLng': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        u'Solicitud.solicitud': {
            'DeclaracionSolicitud': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True', 'blank': 'True'}),
            'Estatus': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'FechaSolicitud': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'FolioSolicitud': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'IdSolicitud': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'ordering': "('IdSolicitud',)", 'object_name': 'Solicitud', 'db_table': "'Solicitud'"},
            'Observaciones': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'PersonaContratante': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'PersonaContratante'", 'to': u"orm['ConexosAgropecuarios.Persona']"}),
            'PersonaSolicitante': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'PersonaSolicitante'", 'to': u"orm['ConexosAgropecuarios.Persona']"}),
            'Programa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Programas.Programa']"}),
            'Unidades': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ValorUnidad': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'})
        }
    }

    complete_apps = ['Solicitud']