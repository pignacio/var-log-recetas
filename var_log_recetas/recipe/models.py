from django.db import models
from django.utils.translation import ugettext as _


# Create your models here.

class MeasuredIngredient(models.Model):
    ingredient = models.ForeignKey('ingredient.Ingredient')
    unit = models.ForeignKey('ingredient.MeasureUnit')
    amount = models.FloatField(_('Amount'))
    subrecipe = models.ForeignKey('SubRecipe')

    def __unicode__(self):
        return "{:2f} {} of {}".format(self.amount, self.unit.name,
                                       self.ingredient.name)


class Step(models.Model):
    subrecipe = models.ForeignKey('SubRecipe')
    text = models.TextField()
    position = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if self.position is None:
            max_position = self.subrecipe.step_set.aggregate(
                models.Max('position'))['position__max'] or 0
            self.position = max_position + 1
        super(Step, self).save(*args, **kwargs)

    def __unicode__(self):
        return "Step #{} of {}: {}".format(self.position, self.subrecipe,
                                           self.text)

    class Meta:
        ordering = ('position',)


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    tags = models.ManyToManyField('Tags', blank=True)

    def __unicode__(self):
        return self.title


class SubRecipe(models.Model):
    recipe = models.ForeignKey(Recipe)
    position = models.PositiveIntegerField()
    title = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        if self.position is None:
            max_position = self.recipe.subrecipe_set.aggregate(
                models.Max('position'))['position__max'] or 0
            self.position = max_position + 1
        super(SubRecipe, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{s.recipe} part #{s.position}: {s.title}".format(s=self)


class Tags(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return "#" + self.name
