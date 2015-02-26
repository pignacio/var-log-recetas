# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def create_measure_units(apps, schema_editor):
    MeasureUnit = apps.get_model('ingredient', 'MeasureUnit')
    db_alias = schema_editor.connection.alias
    MeasureUnit.objects.using(db_alias).bulk_create([
        MeasureUnit(name='units', short_name='u'),
        MeasureUnit(name='grams', short_name='g'),
        MeasureUnit(name='cups', short_name='u'),
        MeasureUnit(name='mililiters', short_name='ml'),
        MeasureUnit(name='cubic centimeters', short_name='cc'),
        MeasureUnit(name='tablespoons', short_name='tbsp'),
        MeasureUnit(name='teaspoons', short_name='tsp'),
    ])


def create_ingredients(apps, schema_editor):
    INGREDIENTS = {
        'Sugar': ('cups', 'tablespoons', 'teaspoons', 'grams'),
        'Milk': ('cups', 'mililiters', 'cubic centimeters', 'tablespoons', 'teaspoons'),
        'Egg': ('units', 'grams'),
        'Egg yolk': ('units',),
        'Egg white': ('units',),
        'Cream': ('cups', 'mililiters', 'cubic centimeters', 'tablespoons', 'teaspoons'),
        'Vanilla extract': ('mililiters', 'cubic centimeters', 'tablespoons', 'teaspoons'),
        'Oat': ('cups', 'tablespoons', 'teaspoons', 'grams'),
        'Flour': ('cups', 'tablespoons', 'teaspoons', 'grams'),
        'Selfraising Flour': ('cups', 'tablespoons', 'teaspoons', 'grams'),
        'Condensed milk': ('cups',
                           'cubic centimeters',
                           'tablespoons',
                           'teaspoons',
                           'grams'),
        'Baking powder': ('tablespoons', 'teaspoons', 'grams'),
        'Baking soda': ('tablespoons', 'teaspoons', 'grams'),
        'Butter': ('cups', 'tablespoons', 'teaspoons', 'grams'),
        'Water': ('cups', 'mililiters', 'cubic centimeters', 'tablespoons', 'teaspoons'),
        'Salt': ('cups', 'tablespoons', 'teaspoons', 'grams'),
        'Oil': ('cups', 'mililiters', 'cubic centimeters', 'tablespoons', 'teaspoons'),
    }

    MeasureUnit = apps.get_model('ingredient', 'MeasureUnit')
    Ingredient = apps.get_model('ingredient', 'Ingredient')
    for ingredient, units in INGREDIENTS.items():
        ingredient, _created = Ingredient.objects.get_or_create(name=ingredient)
        for unit in units:
            ingredient.units.add(MeasureUnit.objects.get(name=unit))
    db_alias = schema_editor.connection.alias



class Migration(migrations.Migration):

    dependencies = [
        ('ingredient', '0001_initial'),
    ]

    operations = [
        migrations.operations.RunPython(create_measure_units),
        migrations.operations.RunPython(create_ingredients),
    ]
