# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cotizador'
        db.create_table('cotizador', (
            ('IdCotizador', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Programa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Programas.Programa'])),
            ('PorcentajeFondo', self.gf('django.db.models.fields.IntegerField')(max_length=30, null=True, blank=True)),
            ('PorcentajeReaseguro', self.gf('django.db.models.fields.IntegerField')(max_length=30, null=True, blank=True)),
            ('Prima', self.gf('django.db.models.fields.IntegerField')(max_length=30, null=True, blank=True)),
            ('FolioCotizador', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
        ))
        db.send_create_signal(u'Cotizador', ['Cotizador'])

        # Adding model 'CotizadorCobertura'
        db.create_table('cotizadorcobertura', (
            ('IdCotizadorCobertura', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Cotizador', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Cotizador.Cotizador'])),
            ('CoberturaPrograma', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Programas.CoberturaPrograma'])),
            ('Tarifa', self.gf('django.db.models.fields.DecimalField')(max_digits=19, decimal_places=2, blank=True)),
            ('Fondo', self.gf('django.db.models.fields.DecimalField')(max_digits=19, decimal_places=2, blank=True)),
            ('Reaseguro', self.gf('django.db.models.fields.DecimalField')(max_digits=19, decimal_places=2, blank=True)),
        ))
        db.send_create_signal(u'Cotizador', ['CotizadorCobertura'])


    def backwards(self, orm):
        # Deleting model 'Cotizador'
        db.delete_table('cotizador')

        # Deleting model 'CotizadorCobertura'
        db.delete_table('cotizadorcobertura')


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
        u'Cotizador.cotizador': {
            'FolioCotizador': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'IdCotizador': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'ordering': "('IdCotizador',)", 'object_name': 'Cotizador', 'db_table': "'cotizador'"},
            'PorcentajeFondo': ('django.db.models.fields.IntegerField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'PorcentajeReaseguro': ('django.db.models.fields.IntegerField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'Prima': ('django.db.models.fields.IntegerField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'Programa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Programas.Programa']"})
        },
        u'Cotizador.cotizadorcobertura': {
            'CoberturaPrograma': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Programas.CoberturaPrograma']"}),
            'Cotizador': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Cotizador.Cotizador']"}),
            'Fondo': ('django.db.models.fields.DecimalField', [], {'max_digits': '19', 'decimal_places': '2', 'blank': 'True'}),
            'IdCotizadorCobertura': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'ordering': "('IdCotizadorCobertura',)", 'object_name': 'CotizadorCobertura', 'db_table': "'cotizadorcobertura'"},
            'Reaseguro': ('django.db.models.fields.DecimalField', [], {'max_digits': '19', 'decimal_places': '2', 'blank': 'True'}),
            'Tarifa': ('django.db.models.fields.DecimalField', [], {'max_digits': '19', 'decimal_places': '2', 'blank': 'True'})
        },
        u'Programas.coberturaprograma': {
            'IdCobertura': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'IdCoberturaPrograma': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'object_name': 'CoberturaPrograma', 'db_table': "'coberturaprograma'"},
            'Programa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Programas.Programa']"})
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
        }
    }

    complete_apps = ['Cotizador']