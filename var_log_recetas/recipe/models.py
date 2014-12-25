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
    text = models.TextField()
    position = models.PositiveIntegerField()

    def save(self):
        if self.position is None:
            max_position = self.recipe.step_set.aggregate(
                models.Max('position'))['position__max'] or 0
            self.position = max_position + 1
        super(Step, self).save()

    def __unicode__(self):
        return "Step #{} of {}: {}".format(self.position, self.recipe,
                                           self.text)

    class Meta:
        ordering = ('position',)

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    tags = models.ManyToManyField('Tags', blank=True)

    def __unicode__(self):
        return self.title


class Tags(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return "#" + self.name
