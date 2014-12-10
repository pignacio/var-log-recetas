from django.db import models
from django.utils.translation import ugettext as _


# Create your models here.

CATEGORY_CHOICES = (
    ('dairy', _('Dairy')),
    ('spices', _('Spices')),
    ('meat', _('Meat')),
    ('veggies', _('Veggies')),
    ('fruit', _('Fruit')),
    ('fat', _('Fat')),
    ('carbohidrates', _('Carbohidrates')),
)


class Ingredient(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)
    units = models.ManyToManyField('MeasureUnit')
    categories = models.ManyToManyField('IngredientCategory',
                                        blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('ingredient')
        verbose_name_plural = _('ingredients')


class MeasureUnit(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)
    short_name = models.CharField(_('Short name'), max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('measure unit')
        verbose_name_plural = _('measure units')


class IngredientCategory(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('ingredient category')
        verbose_name_plural = _('ingredient categories')
