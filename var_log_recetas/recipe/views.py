import json
import logging

from django.http import HttpResponse
from django.shortcuts import render, redirect

from ingredient.models import Ingredient, MeasureUnit
from utils.views import has_models, has_get_models
from .models import Recipe, MeasuredIngredient, Step
from .forms import RecipeAddForm, MeasuredIngredientForm, StepForm


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def _render_json_error(err, *args, **kwargs):
    return HttpResponse(json.dumps({
        'success': False,
        'error': str(err),
    }))



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
    except (model.DoesNotExist, ValueError):
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
def recipe_edit_ingredient_delete(request, recipe):
    error = None
    try:
        ingredient_id = request.GET['ingredient_id']
    except KeyError:
        error = "Missing ingredient_id"
    else:
        try:
            ingredient = MeasuredIngredient.objects.get(pk=ingredient_id)
        except MeasuredIngredient.DoesNotExist:
            error = "Ingredient does not exist"
        else:
            ingredient.delete()

    return HttpResponse(json.dumps({
        'success': not error,
        'error': error,
    }))


@has_models
def recipe_edit_ingredients(request, recipe):
    return render(request, 'recipe/recipe_edit/ingredients.html', {
        'measured_ingredients': recipe.measuredingredient_set.all(),
    })


@has_models
def recipe_edit_step_add(request, recipe):
    instance = Step(recipe=recipe)
    if request.method == "POST":
        form = StepForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponse("1")
    else:
        step_id = request.GET.get('step', None)
        step = _get_object_or_none(Step, step_id)
        unit_id = request.GET.get('unit', None)
        unit = _get_object_or_none(MeasureUnit, unit_id)
        form = StepForm(instance=instance, initial={
            'step': step,
            'amount': request.GET.get('amount', None),
            'unit': unit,
        })
    form.helper.form_id = 'step-add-form'
    return render(request, 'layout/crispyform.html', {
        'form': form,
    })


@has_get_models('step', on_error=_render_json_error)
def recipe_edit_step_delete(request, recipe, step):
    step.delete()
    return HttpResponse(json.dumps({
        'success': True,
    }))


@has_models
def recipe_edit_steps(request, recipe):
    return render(request, 'recipe/recipe_edit/steps.html', {
        'steps': recipe.step_set.all(),
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


def _swap_steps(step, ostep):
    step.position, ostep.position = ostep.position, step.position
    step.save()
    ostep.save()


@has_get_models('step', on_error=_render_json_error)
def recipe_edit_step_move_up(request, recipe, step):
    error = None
    previous_step = (recipe.step_set.filter(position__lt=step.position)
                     .order_by('-position').first())
    if previous_step is None:
        error = "There is no previous step"
    else:
        _swap_steps(step, previous_step)
    return HttpResponse(json.dumps({
        'success': not error,
        'error': error,
    }))

@has_get_models('step', on_error=_render_json_error)
def recipe_edit_step_move_down(request, recipe, step):
    error = None
    next_step = (recipe.step_set.filter(position__gt=step.position)
                     .order_by('position').first())
    if next_step is None:
        error = "There is no next step"
    else:
        _swap_steps(step, next_step)
    return HttpResponse(json.dumps({
        'success': not error,
        'error': error,
    }))
