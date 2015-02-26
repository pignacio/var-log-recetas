# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'ingredient',
                'verbose_name_plural': 'ingredients',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MeasureUnit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('short_name', models.CharField(max_length=255, verbose_name='Short name')),
            ],
            options={
                'verbose_name': 'measure unit',
                'verbose_name_plural': 'measure units',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='units',
            field=models.ManyToManyField(to='ingredient.MeasureUnit'),
            preserve_default=True,
        ),
    ]
