# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Sepomex'
        db.create_table('sepomex', (
            ('IdSepomex', self.gf('django.db.models.fields.IntegerField')(primary_key=True, db_column='IdSepomex')),
            ('DCodigo', self.gf('django.db.models.fields.CharField')(max_length=5L, db_column='DCodigo', blank=True)),
            ('DAsenta', self.gf('django.db.models.fields.CharField')(max_length=200L, db_column='DAsenta', blank=True)),
            ('DTipoAsenta', self.gf('django.db.models.fields.CharField')(max_length=100L, db_column='DTipoAsenta', blank=True)),
            ('DMnpio', self.gf('django.db.models.fields.CharField')(max_length=200L, db_column='DMnpio', blank=True)),
            ('DEstado', self.gf('django.db.models.fields.CharField')(max_length=100L, db_column='DEstado', blank=True)),
            ('DCiudad', self.gf('django.db.models.fields.CharField')(max_length=200L, db_column='DCiudad', blank=True)),
            ('DCp', self.gf('django.db.models.fields.CharField')(max_length=5L, db_column='DCp', blank=True)),
            ('CEstado', self.gf('django.db.models.fields.CharField')(max_length=2L, db_column='CEstado', blank=True)),
            ('COficina', self.gf('django.db.models.fields.CharField')(max_length=5L, db_column='COficina', blank=True)),
            ('CCp', self.gf('django.db.models.fields.CharField')(max_length=5L, db_column='CCp', blank=True)),
            ('CTipoAsenta', self.gf('django.db.models.fields.CharField')(max_length=50L, db_column='CTipoAsenta', blank=True)),
            ('CMnpio', self.gf('django.db.models.fields.CharField')(max_length=5L, db_column='CMnpio', blank=True)),
            ('IdAsentaCpCons', self.gf('django.db.models.fields.CharField')(max_length=10L, db_column='IdAsentaCpcons', blank=True)),
            ('DZona', self.gf('django.db.models.fields.CharField')(max_length=10L, db_column='DZona', blank=True)),
            ('CCveCiudad', self.gf('django.db.models.fields.CharField')(max_length=5L, db_column='CCveCiudad', blank=True)),
        ))
        db.send_create_signal(u'Direcciones', ['Sepomex'])

        # Adding model 'Direccion'
        db.create_table('Direcciones', (
            ('IdDireccion', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ConexosAgropecuarios.Persona'])),
            ('TipoDireccion', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('Detalle', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('Calle', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('NumeroExterior', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('NumeroInterior', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('IdSepomex', self.gf('django.db.models.fields.CharField')(max_length=11, null=True, blank=True)),
        ))
        db.send_create_signal(u'Direcciones', ['Direccion'])


    def backwards(self, orm):
        # Deleting model 'Sepomex'
        db.delete_table('sepomex')

        # Deleting model 'Direccion'
        db.delete_table('Direcciones')


    models = {
        u'ConexosAgropecuarios.persona': {
            'ApellidoMaterno': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'ApellidoPaterno': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'Curp': ('django.db.models.fields.CharField', [], {'max_length': '18', 'null': 'True', 'blank': 'True'}),
            'Email': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'EstadoCivil': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
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
        u'Direcciones.direccion': {
            'Calle': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'Detalle': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'IdDireccion': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'IdSepomex': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            'Meta': {'ordering': "('Persona',)", 'object_name': 'Direccion', 'db_table': "'Direcciones'"},
            'NumeroExterior': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'NumeroInterior': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'Persona': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ConexosAgropecuarios.Persona']"}),
            'TipoDireccion': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'})
        },
        u'Direcciones.sepomex': {
            'CCp': ('django.db.models.fields.CharField', [], {'max_length': '5L', 'db_column': "'CCp'", 'blank': 'True'}),
            'CCveCiudad': ('django.db.models.fields.CharField', [], {'max_length': '5L', 'db_column': "'CCveCiudad'", 'blank': 'True'}),
            'CEstado': ('django.db.models.fields.CharField', [], {'max_length': '2L', 'db_column': "'CEstado'", 'blank': 'True'}),
            'CMnpio': ('django.db.models.fields.CharField', [], {'max_length': '5L', 'db_column': "'CMnpio'", 'blank': 'True'}),
            'COficina': ('django.db.models.fields.CharField', [], {'max_length': '5L', 'db_column': "'COficina'", 'blank': 'True'}),
            'CTipoAsenta': ('django.db.models.fields.CharField', [], {'max_length': '50L', 'db_column': "'CTipoAsenta'", 'blank': 'True'}),
            'DAsenta': ('django.db.models.fields.CharField', [], {'max_length': '200L', 'db_column': "'DAsenta'", 'blank': 'True'}),
            'DCiudad': ('django.db.models.fields.CharField', [], {'max_length': '200L', 'db_column': "'DCiudad'", 'blank': 'True'}),
            'DCodigo': ('django.db.models.fields.CharField', [], {'max_length': '5L', 'db_column': "'DCodigo'", 'blank': 'True'}),
            'DCp': ('django.db.models.fields.CharField', [], {'max_length': '5L', 'db_column': "'DCp'", 'blank': 'True'}),
            'DEstado': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'db_column': "'DEstado'", 'blank': 'True'}),
            'DMnpio': ('django.db.models.fields.CharField', [], {'max_length': '200L', 'db_column': "'DMnpio'", 'blank': 'True'}),
            'DTipoAsenta': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'db_column': "'DTipoAsenta'", 'blank': 'True'}),
            'DZona': ('django.db.models.fields.CharField', [], {'max_length': '10L', 'db_column': "'DZona'", 'blank': 'True'}),
            'IdAsentaCpCons': ('django.db.models.fields.CharField', [], {'max_length': '10L', 'db_column': "'IdAsentaCpcons'", 'blank': 'True'}),
            'IdSepomex': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'IdSepomex'"}),
            'Meta': {'object_name': 'Sepomex', 'db_table': "'sepomex'"}
        }
    }

    complete_apps = ['Direcciones']