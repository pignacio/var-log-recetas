# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingredient', '0002_initial_ingredients'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeasureUnitGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Nombre')),
                ('units', models.ManyToManyField(related_name='groups', to='ingredient.MeasureUnit')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'grupo de unidades',
                'verbose_name_plural': 'grupos de unidades',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ('name',), 'verbose_name': 'ingredient', 'verbose_name_plural': 'ingredients'},
        ),
        migrations.AlterModelOptions(
            name='measureunit',
            options={'ordering': ('name',), 'verbose_name': 'measure unit', 'verbose_name_plural': 'measure units'},
        ),
        migrations.AddField(
            model_name='ingredient',
            name='unit_groups',
            field=models.ManyToManyField(to='ingredient.MeasureUnitGroup'),
            preserve_default=True,
        ),
    ]
