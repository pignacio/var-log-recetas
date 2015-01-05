# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    no_dry_run = True
    MEASURE_UNITS = (
        (u'units', u'u'),
        (u'grams', u'g'),
        (u'cups', u'c'),
        (u'mililiters', u'ml'),
        (u'cubic centimeters', u'cc'),
        (u'tablespoons', u'tbsp'),
        (u'teaspoons', u'tsp'),
    )

    INGREDIENT_CATEGORIES = (
        u'Carbohidrates'
        u'Dairy',
        u'Dry',
        u'Fat',
        u'Fruit',
        u'Liquid',
        u'Meat',
        u'Spices',
        u'Veggies',
    )

    INGREDIENTS = (
        (u'Sugar',
         (u'cups', u'tablespoons', u'teaspoons', u'grams'),
         (u'Carbohidrates',)),
        (u'Milk',
         (u'cups', u'mililiters', u'cubic centimeters', u'tablespoons', u'teaspoons'),
         (u'Dairy',)),
        (u'Egg',
         (u'units', u'grams'),
         ()),
        (u'Egg yolk',
         (u'units',),
         ()),
        (u'Egg white',
         (u'units',),
         ()),
        (u'Cream',
         (u'cups', u'mililiters', u'cubic centimeters', u'tablespoons', u'teaspoons'),
         (u'Dairy', u'Fat')),
        (u'Vanilla extract',
         (u'mililiters', u'cubic centimeters', u'tablespoons', u'teaspoons'),
         (u'Spices',)),
        (u'Oat',
         (u'cups', u'tablespoons', u'teaspoons', u'grams'),
         (u'Carbohidrates',)),
        (u'Flour',
         (u'cups', u'tablespoons', u'teaspoons', u'grams'),
         (u'Carbohidrates',)),
        (u'Selfraising Flour',
         (u'cups', u'tablespoons', u'teaspoons', u'grams'),
         (u'Carbohidrates',)),
        (u'Condensed milk',
         (u'cups',
          u'mililiters',
          u'cubic centimeters',
          u'tablespoons',
          u'teaspoons',
          u'grams'),
         (u'Dairy',)),
        (u'Baking powder',
         (u'tablespoons', u'teaspoons', u'grams'),
         ()),
        (u'Baking soda',
         (u'tablespoons', u'teaspoons', u'grams'),
         ()),
        (u'Butter',
         (u'cups', u'tablespoons', u'teaspoons', u'grams'),
         (u'Dairy', u'Fat')),
        (u'Water',
         (u'cups', u'mililiters', u'cubic centimeters', u'tablespoons', u'teaspoons'),
         (u'Liquid',)),
        (u'Salt',
         (u'cups', u'tablespoons', u'teaspoons', u'grams'),
         (u'Spices',)),
        (u'Oil',
         (u'cups', u'mililiters', u'cubic centimeters', u'tablespoons', u'teaspoons'),
         (u'Liquid',)),
    )

    def forwards(self, orm):
        for name, short_name in self.MEASURE_UNITS:
            if orm['ingredient.MeasureUnit'].objects.filter(name=name).exists():
                continue
            orm['ingredient.MeasureUnit'].objects.create(
                name=name,
                short_name=short_name,
            )

        for name in self.INGREDIENT_CATEGORIES:
            if orm['ingredient.IngredientCategory'].objects.filter(name=name).exists():
                continue
            orm['ingredient.IngredientCategory'].objects.create(
                name=name,
            )

        for name, units, categories in self.INGREDIENTS:
            if orm['ingredient.Ingredient'].objects.filter(name=name).exists():
                continue
            ingredient = orm['ingredient.Ingredient'].objects.create(
                name=name,
            )
            for unit in units:
                ingredient.units.add(orm['ingredient.MeasureUnit'].objects.get(name=unit))
            for category in categories:
                ingredient.categories.add(orm['ingredient.IngredientCategory'].objects.get(name=category))


    def backwards(self, orm):
        pass

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
        }
    }

    complete_apps = ['ingredient']
