from django.db import models
from django.utils.translation import ugettext as _


# Create your models here.

class MeasuredIngredient(models.Model):
    ingredient = models.ForeignKey('ingredient.Ingredient')
    unit = models.ForeignKey('ingredient.MeasureUnit')
    amount = models.FloatField(_('Amount'))
    recipe = models.ForeignKey('Recipe')

    def __unicode__(self):
        return "{:2f} {} of {}".format(self.amount, self.unit.name,
                                       self.ingredient.name)


class Step(models.Model):
    recipe = models.ForeignKey('Recipe')
    text = models.CharField(max_length=255)
    position = models.PositiveIntegerField()

    def __unicode__(self):
        return "Step #{} of {}: {}".format(self.position, self.recipe,
                                           self.text)


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    tags = models.ManyToManyField('Tags', blank=True)

    def __unicode__(self):
        return self.title


class Tags(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return "#" + self.name
