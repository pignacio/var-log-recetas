#!/usr/bin/env python
# encoding: utf-8
# pylint: disable=too-few-public-methods

from django.db import models
from django.utils.translation import ugettext as _


# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)
    units = models.ManyToManyField('MeasureUnit', blank=True)
    unit_groups = models.ManyToManyField('MeasureUnitGroup', blank=True)

    def has_unit(self, unit):
        return (self.units.filter(id=unit.id).exists() or
                self.groups.filter(units=unit).exists())

    def all_units(self):
        units = set()
        units.update(self.units.all())
        for unit_group in self.unit_groups.all():
            units.update(unit_group.units.all())
        return units

    def __unicode__(self):
        return self.name

    class Meta(object):
        verbose_name = _('ingredient')
        verbose_name_plural = _('ingredients')

        ordering = ('name',)


class MeasureUnit(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)
    short_name = models.CharField(_('Short name'), max_length=255)

    def __unicode__(self):
        return self.name

    class Meta(object):
        verbose_name = _('measure unit')
        verbose_name_plural = _('measure units')

        ordering = ('name',)


class MeasureUnitGroup(models.Model):
    name = models.CharField(_('Nombre'), max_length=255, unique=True)
    units = models.ManyToManyField('MeasureUnit', related_name='groups')

    def __unicode__(self):
        return self.name

    class Meta(object):
        verbose_name = _('grupo de unidades')
        verbose_name_plural = _('grupos de unidades')

        ordering = ('name',)

