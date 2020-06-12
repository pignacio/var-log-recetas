from django.db import models
from django.utils.translation import ugettext as _


class MeasuredIngredient(models.Model):
    ingredient = models.ForeignKey("ingredient.Ingredient", on_delete=models.PROTECT)
    unit = models.ForeignKey("ingredient.MeasureUnit", on_delete=models.PROTECT)
    amount = models.FloatField(_("Amount"))
    subrecipe = models.ForeignKey("SubRecipe", on_delete=models.PROTECT)

    def __str__(self):
        return "{:2f} {} of {}".format(
            self.amount, self.unit.name, self.ingredient.name
        )


class Step(models.Model):
    subrecipe = models.ForeignKey("SubRecipe", on_delete=models.PROTECT)
    text = models.TextField()
    position = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if self.position is None:
            max_position = (
                self.subrecipe.step_set.aggregate(models.Max("position"))[
                    "position__max"
                ]
                or 0
            )
            self.position = max_position + 1
        super(Step, self).save(*args, **kwargs)

    def __str__(self):
        return "Step #{} of {}: {}".format(self.position, self.subrecipe, self.text)

    class Meta:
        ordering = ("position",)


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    tags = models.ManyToManyField("Tags", blank=True)

    def as_json(self):
        output = {}
        output["title"] = self.title
        output["subrecipes"] = [sr.as_json() for sr in self.subrecipe_set.all()]
        return output

    def __str__(self):
        return self.title


class SubRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT)
    position = models.PositiveIntegerField()
    title = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        if self.position is None:
            max_position = (
                self.recipe.subrecipe_set.aggregate(models.Max("position"))[
                    "position__max"
                ]
                or 0
            )
            self.position = max_position + 1
        super(SubRecipe, self).save(*args, **kwargs)

    def as_json(self):
        output = {}
        output["title"] = self.title
        output["ingredients"] = [
            {"amount": i.amount, "unit": i.unit.name, "ingredient": i.ingredient.name}
            for i in self.measuredingredient_set.all()
        ]
        output["steps"] = [s.text for s in self.step_set.all()]
        return output

    def __str__(self):
        return "{s.recipe} part #{s.position}: {s.title}".format(s=self)


class Tags(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return "#" + self.name
