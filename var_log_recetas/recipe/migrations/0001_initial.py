# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MeasuredIngredient'
        db.create_table(u'recipe_measuredingredient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ingredient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ingredient.Ingredient'])),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ingredient.MeasureUnit'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recipe.Recipe'])),
        ))
        db.send_create_signal(u'recipe', ['MeasuredIngredient'])

        # Adding model 'Step'
        db.create_table(u'recipe_step', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recipe.Recipe'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'recipe', ['Step'])

        # Adding model 'Recipe'
        db.create_table(u'recipe_recipe', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'recipe', ['Recipe'])

        # Adding M2M table for field tags on 'Recipe'
        m2m_table_name = db.shorten_name(u'recipe_recipe_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recipe', models.ForeignKey(orm[u'recipe.recipe'], null=False)),
            ('tags', models.ForeignKey(orm[u'recipe.tags'], null=False))
        ))
        db.create_unique(m2m_table_name, ['recipe_id', 'tags_id'])

        # Adding model 'Tags'
        db.create_table(u'recipe_tags', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'recipe', ['Tags'])


    def backwards(self, orm):
        # Deleting model 'MeasuredIngredient'
        db.delete_table(u'recipe_measuredingredient')

        # Deleting model 'Step'
        db.delete_table(u'recipe_step')

        # Deleting model 'Recipe'
        db.delete_table(u'recipe_recipe')

        # Removing M2M table for field tags on 'Recipe'
        db.delete_table(db.shorten_name(u'recipe_recipe_tags'))

        # Deleting model 'Tags'
        db.delete_table(u'recipe_tags')


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
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'recipe.tags': {
            'Meta': {'object_name': 'Tags'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['recipe']