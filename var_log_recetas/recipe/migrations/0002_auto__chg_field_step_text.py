# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Step.text'
        db.alter_column(u'recipe_step', 'text', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):

        # Changing field 'Step.text'
        db.alter_column(u'recipe_step', 'text', self.gf('django.db.models.fields.CharField')(max_length=255))

    models = {
        u'ingredient.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ingredient.IngredientCategory']", 'symmetrical': 'False', 'blank': 'True'}),
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
        },
        u'recipe.measuredingredient': {
            'Meta': {'object_name': 'MeasuredIngredient'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ingredient.Ingredient']"}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recipe.Recipe']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ingredient.MeasureUnit']"})
        },
        u'recipe.recipe': {
            'Meta': {'object_name': 'Recipe'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['recipe.Tags']", 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'recipe.step': {
            'Meta': {'object_name': 'Step'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recipe.Recipe']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'recipe.tags': {
            'Meta': {'object_name': 'Tags'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['recipe']