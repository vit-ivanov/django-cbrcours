# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CurrencyLastUpdate'
        db.create_table(u'cbrcource_currencylastupdate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_update', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'cbrcource', ['CurrencyLastUpdate'])

        # Adding model 'Currency'
        db.create_table(u'cbrcource_currency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('value', self.gf('django.db.models.fields.DecimalField')(max_digits=30, decimal_places=10)),
        ))
        db.send_create_signal(u'cbrcource', ['Currency'])


    def backwards(self, orm):
        # Deleting model 'CurrencyLastUpdate'
        db.delete_table(u'cbrcource_currencylastupdate')

        # Deleting model 'Currency'
        db.delete_table(u'cbrcource_currency')


    models = {
        u'cbrcource.currency': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Currency'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '30', 'decimal_places': '10'})
        },
        u'cbrcource.currencylastupdate': {
            'Meta': {'object_name': 'CurrencyLastUpdate'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cbrcource']
