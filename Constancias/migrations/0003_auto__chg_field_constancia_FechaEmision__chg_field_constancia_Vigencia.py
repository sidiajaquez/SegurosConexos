# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Constancia.FechaEmision'
        db.alter_column('Constancia', 'FechaEmision', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Constancia.VigenciaInicio'
        db.alter_column('Constancia', 'VigenciaInicio', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Constancia.VigenciaFin'
        db.alter_column('Constancia', 'VigenciaFin', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # Changing field 'Constancia.FechaEmision'
        db.alter_column('Constancia', 'FechaEmision', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Constancia.VigenciaInicio'
        db.alter_column('Constancia', 'VigenciaInicio', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Constancia.VigenciaFin'
        db.alter_column('Constancia', 'VigenciaFin', self.gf('django.db.models.fields.DateField')(null=True))

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
        u'Constancias.constancia': {
            'CuotaNeta': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'FechaEmision': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'FolioConstancia': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'IdConstancia': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'ordering': "('IdConstancia',)", 'object_name': 'Constancia', 'db_table': "'Constancia'"},
            'Solicitud': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Solicitud.Solicitud']"}),
            'SumaAsegurada': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'VigenciaFin': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'VigenciaInicio': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'Constancias.constanciacobertura': {
            'Constancia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Constancias.Constancia']"}),
            'CuotaFondo': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'CuotaReaseguro': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'IdCobertura': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'IdConstanciaCobertura': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'ordering': "('IdConstanciaCobertura',)", 'object_name': 'ConstanciaCobertura', 'db_table': "'ConstanciaCobertura'"},
            'Tarifa': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'TarifaFondo': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'TarifaReaseguro': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'})
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

    complete_apps = ['Constancias']