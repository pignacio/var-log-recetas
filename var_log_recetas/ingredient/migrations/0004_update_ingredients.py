# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import collections

from django.db import models, migrations


Unit = collections.namedtuple('Unit', ['name', 'short_name'])
Group = collections.namedtuple('Group', ['name', 'units'])
IngredientData = collections.namedtuple('Ingredient', ['name', 'units', 'groups'])


def update_units(apps, schema_editor):
    UNITS = [
        Unit(name='cubic centimeters', short_name='cc'),
        Unit(name='cups', short_name='u'),
        Unit(name='grams', short_name='g'),
        Unit(name='heaped tablespoons', short_name='htbsp'),
        Unit(name='heaped teaspoons', short_name='htsp'),
        Unit(name='mililiters', short_name='ml'),
        Unit(name='pinch', short_name='pch'),
        Unit(name='tablespoons', short_name='tbsp'),
        Unit(name='teaspoons', short_name='tsp'),
        Unit(name='units', short_name='u'),
    ]
    GROUPS = [
        Group(name='Sólidos', units=[
            'cups', 'grams', 'heaped tablespoons', 'heaped teaspoons',
            'pinch', 'tablespoons', 'teaspoons',
        ]),
        Group(name='Líquidos', units=[
            'cubic centimeters', 'cups', 'mililiters',
            'pinch', 'tablespoons', 'teaspoons',
        ]),
    ]

    MeasureUnit = apps.get_model('ingredient', 'MeasureUnit')
    MeasureUnitGroup = apps.get_model('ingredient', 'MeasureUnitGroup')

    for unit in UNITS:
        MeasureUnit.objects.get_or_create(name=unit.name, defaults=unit._asdict())

    for group_data in GROUPS:
        group, _created = MeasureUnitGroup.objects.get_or_create(name=group_data.name)
        for unit_name in group_data.units:
            group.units.add(MeasureUnit.objects.get(name=unit_name))


def update_ingredients(apps, schema_editor):
    INGREDIENTS = [
        IngredientData(name='Baking powder', groups=['Sólidos'], units=[]),
        IngredientData(name='Baking soda', groups=['Sólidos'], units=[]),
        IngredientData(name='Butter', groups=['Sólidos'], units=[]),
        IngredientData(name='Cinnamon', groups=['Sólidos'], units=[]),
        IngredientData(name='Flour', groups=['Sólidos'], units=[]),
        IngredientData(name='Icing sugar', groups=['Sólidos'], units=[]),
        IngredientData(name='Oat', groups=['Sólidos'], units=[]),
        IngredientData(name='Salt', groups=['Sólidos'], units=[]),
        IngredientData(name='Self raising flour', groups=['Sólidos'], units=[]),
        IngredientData(name='Sugar', groups=['Sólidos'], units=[]),

        IngredientData(name='Condensed milk', groups=['Líquidos'], units=['grams']),
        IngredientData(name='Cream', groups=['Líquidos'], units=[]),
        IngredientData(name='Lemon juice', groups=['Líquidos'], units=[]),
        IngredientData(name='Oil', groups=['Líquidos'], units=[]),
        IngredientData(name='Orange juice', groups=['Líquidos'], units=[]),
        IngredientData(name='Vanilla extract', groups=['Líquidos'], units=[]),
        IngredientData(name='Water', groups=['Líquidos'], units=[]),

        IngredientData(name='Apple', groups=[], units=['units', 'grams']),
        IngredientData(name='Egg', groups=[], units=['units', 'grams']),
        IngredientData(name='Egg white', groups=[], units=['units', 'grams']),
        IngredientData(name='Egg yolk', groups=[], units=['units', 'grams']),
        IngredientData(name='Lemon', groups=[], units=['units', 'grams']),
        IngredientData(name='Orange', groups=[], units=['units', 'grams']),
    ]

    Ingredient = apps.get_model('ingredient', 'Ingredient')
    MeasureUnit = apps.get_model('ingredient', 'MeasureUnit')
    MeasureUnitGroup = apps.get_model('ingredient', 'MeasureUnitGroup')

    for data in INGREDIENTS:
        ingredient, _created = Ingredient.objects.get_or_create(
            name=data.name)
        ingredient.units = [MeasureUnit.objects.get(name=unit_name)
                            for unit_name in data.units]
        ingredient.unit_groups = [MeasureUnitGroup.objects.get(name=group_name)
                                  for group_name in data.groups]


class Migration(migrations.Migration):
    dependencies = [
        ('ingredient', '0003_unit_groups'),
    ]

    operations = [
        migrations.operations.RunPython(update_units, lambda a, m: None),
        migrations.operations.RunPython(update_ingredients, lambda a, m: None),
    ]
