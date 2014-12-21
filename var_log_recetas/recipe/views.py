from django.http import HttpResponse
from django.shortcuts import render, redirect

from ingredient.models import Ingredient, MeasureUnit
from utils.views import has_models
from .models import Recipe, MeasuredIngredient
from .forms import RecipeAddForm, MeasuredIngredientForm



def home(request):
    return render(request, 'recipe/home.html', {
        'recipes': Recipe.objects.all().order_by('id'),
    })


@has_models
def recipe_edit(request, recipe):
    return render(request, 'recipe/recipe_edit.html', {
        'recipe': recipe,
    })


def _get_object_or_none(model, model_pk):
    try:
        return model.objects.get(pk=model_pk)
    except model.DoesNotExist:
        return None


@has_models
def recipe_edit_ingredient_add(request, recipe):
    instance = MeasuredIngredient(recipe=recipe)
    if request.method == "POST":
        form = MeasuredIngredientForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponse("1")
    else:
        ingredient_id = request.GET.get('ingredient', None)
        ingredient = _get_object_or_none(Ingredient, ingredient_id)
        unit_id = request.GET.get('unit', None)
        unit = _get_object_or_none(MeasureUnit, unit_id)
        form = MeasuredIngredientForm(instance=instance, initial={
            'ingredient': ingredient,
            'amount': request.GET.get('amount', None),
            'unit': unit,
        })
    form.helper.form_id = 'ingredient-add-form'
    return render(request, 'recipe/recipe_edit/ingredient_add.html', {
        'form': form,
    })

@has_models
def recipe_edit_ingredients(request, recipe):
    return render(request, 'recipe/recipe_edit/ingredients.html', {
        'measured_ingredients': recipe.measuredingredient_set.all(),
    })


def recipe_add(request):
    recipe = Recipe()
    if request.method == "POST":
        form = RecipeAddForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_recipe_edit', recipe.id)
    else:
        form = RecipeAddForm(instance=recipe)
    return render(request, 'recipe/recipe_add.html', {
        'form': form,
    })
