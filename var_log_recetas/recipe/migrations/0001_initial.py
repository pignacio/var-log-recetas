# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingredient', '0002_initial_ingredients'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeasuredIngredient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField(verbose_name='Amount')),
                ('ingredient', models.ForeignKey(to='ingredient.Ingredient')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('position', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ('position',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubRecipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=200)),
                ('recipe', models.ForeignKey(to='recipe.Recipe')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='step',
            name='subrecipe',
            field=models.ForeignKey(to='recipe.SubRecipe'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(to='recipe.Tags', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measuredingredient',
            name='subrecipe',
            field=models.ForeignKey(to='recipe.SubRecipe'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measuredingredient',
            name='unit',
            field=models.ForeignKey(to='ingredient.MeasureUnit'),
            preserve_default=True,
        ),
    ]
