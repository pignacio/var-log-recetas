# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Ingredient'
        db.create_table(u'ingredient_ingredient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'ingredient', ['Ingredient'])

        # Adding M2M table for field units on 'Ingredient'
        m2m_table_name = db.shorten_name(u'ingredient_ingredient_units')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ingredient', models.ForeignKey(orm[u'ingredient.ingredient'], null=False)),
            ('measureunit', models.ForeignKey(orm[u'ingredient.measureunit'], null=False))
        ))
        db.create_unique(m2m_table_name, ['ingredient_id', 'measureunit_id'])

        # Adding M2M table for field categories on 'Ingredient'
        m2m_table_name = db.shorten_name(u'ingredient_ingredient_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ingredient', models.ForeignKey(orm[u'ingredient.ingredient'], null=False)),
            ('ingredientcategory', models.ForeignKey(orm[u'ingredient.ingredientcategory'], null=False))
        ))
        db.create_unique(m2m_table_name, ['ingredient_id', 'ingredientcategory_id'])

        # Adding model 'MeasureUnit'
        db.create_table(u'ingredient_measureunit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'ingredient', ['MeasureUnit'])

        # Adding model 'IngredientCategory'
        db.create_table(u'ingredient_ingredientcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'ingredient', ['IngredientCategory'])


    def backwards(self, orm):
        # Deleting model 'Ingredient'
        db.delete_table(u'ingredient_ingredient')

        # Removing M2M table for field units on 'Ingredient'
        db.delete_table(db.shorten_name(u'ingredient_ingredient_units'))

        # Removing M2M table for field categories on 'Ingredient'
        db.delete_table(db.shorten_name(u'ingredient_ingredient_categories'))

        # Deleting model 'MeasureUnit'
        db.delete_table(u'ingredient_measureunit')

        # Deleting model 'IngredientCategory'
        db.delete_table(u'ingredient_ingredientcategory')


    models = {
        u'ingredient.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['ingredient.IngredientCategory']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'units': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ingredient.MeasureUnit']", 'symmetrical': 'False'})
        },
        u'ingredient.ingredientcategory': {
            'Meta': {'object_name': 'IngredientCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'ingredient.measureunit': {
            'Meta': {'object_name': 'MeasureUnit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['ingredient']