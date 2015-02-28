#!/usr/bin/env python
# encoding: utf-8
# pylint: disable=too-few-public-methods

from django.db import models
from django.utils.translation import ugettext as _


# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)
    units = models.ManyToManyField('MeasureUnit')

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
