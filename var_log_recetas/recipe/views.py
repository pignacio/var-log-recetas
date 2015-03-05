#!/usr/bin/env python
# encoding: utf-8
# pylint: disable=too-few-public-methods,too-many-ancestors

import datetime
import json
import logging

from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    FormView, ListView, DetailView, RedirectView
)

from ingredient.models import MeasureUnit
from utils.views import has_models, has_get_models
from .models import Recipe, MeasuredIngredient, Step, SubRecipe
from .forms import (
    RecipeAddForm, MeasuredIngredientForm, StepForm, SubRecipeSelectForm,
    SubRecipeForm
)


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def _render_json_error(err, *_args, **_kwargs):
    return HttpResponse(json.dumps({
        'success': False,
        'error': str(err),
    }))


class RecipeListView(ListView):
    model = Recipe


class RecipeCreateView(FormView):
    form_class = RecipeAddForm
    template_name = 'recipe/recipe_form.html'

    def form_valid(self, form):
        form.save()
        return redirect('recipe_edit', form.instance.id)


class RecipeEditView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=kwargs['recipe_id'])
        try:
            subrecipe_id = self.request.GET['subrecipe']
            subrecipe = recipe.subrecipe_set.get(id=subrecipe_id)
        except (KeyError, SubRecipe.DoesNotExist):
            subrecipe = (recipe.subrecipe_set.first() or
                         recipe.subrecipe_set.create(title='la receta'))
        return reverse('subrecipe_edit', kwargs=dict(subrecipe_id=subrecipe.id))


class RecipePartsView(DetailView):
    model = Recipe
    pk_url_kwarg = 'recipe_id'
    template_name = 'recipe/recipe_parts.html'


class RecipeAddPartView(FormView):
    form_class = SubRecipeForm
    template_name = "generic/form.html"

    def get_form(self, form_class):
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('recipe_id'))
        subrecipe = SubRecipe(recipe=recipe)
        return form_class(instance=subrecipe, **self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        return redirect('recipe_parts', form.instance.recipe.id)


class SubRecipeRenameView(FormView):
    form_class = SubRecipeForm
    template_name = "generic/form.html"

    def get_form(self, form_class):
        subrecipe = get_object_or_404(SubRecipe,
                                      id=self.kwargs.get('subrecipe_id'))
        return form_class(instance=subrecipe, **self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        return redirect('recipe_parts', form.instance.recipe.id)


class SubRecipeDetailView(DetailView):
    model = SubRecipe
    pk_url_kwarg = 'subrecipe_id'

    def get_context_data(self, *args, **kwargs):
        context = super(SubRecipeDetailView, self).get_context_data(*args,
                                                                    **kwargs)
        if self.object.recipe.subrecipe_set.count() > 1:
            context['subrecipe_select_form'] = SubRecipeSelectForm(
                self.object.recipe,
                initial=dict(
                    subrecipe=self.object.id
                ),
            )
        context['recipe'] = self.object.recipe
        return context


def home(request):
    return render(request, 'recipe/home.html', {
        'recipes': Recipe.objects.all().order_by('id'),
    })


def recipe_detail(request, recipe):
    return render(request, 'recipe/recipe_detail.html', {
        'recipe': recipe,
    })


@has_models
def recipe_edit(request, recipe):
    return render(request, 'recipe/recipe_edit.html', {
        'recipe': recipe,
    })


@has_models
def subrecipe_edit(request, subrecipe):
    return render(request, 'recipe/subrecipe_edit.html', {
        'recipe': subrecipe.recipe,
        'subrecipe': subrecipe,
    })


def _get_object_or_none(model, model_pk):
    try:
        return model.objects.get(pk=model_pk)
    except (model.DoesNotExist, ValueError):
        return None


@has_models
def subrecipe_edit_ingredient_add(request, subrecipe):
    instance = MeasuredIngredient(subrecipe=subrecipe)
    if request.method == "POST":
        form = MeasuredIngredientForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponse("1")
    else:
        unit_id = request.GET.get('unit', None)
        unit = _get_object_or_none(MeasureUnit, unit_id)
        form = MeasuredIngredientForm(instance=instance, initial={
            'ingredient_name': request.GET.get('ingredient_name'),
            'amount': request.GET.get('amount', None),
            'unit': unit,
        })
    form.helper.form_id = 'ingredient-add-form'
    return render(request, 'recipe/recipe_edit/ingredient_add.html', {
        'form': form,
    })


@has_models
def subrecipe_edit_ingredient_delete(request, subrecipe):  # pylint: disable=invalid-name
    error = None
    try:
        ingredient_id = request.GET['ingredient_id']
    except KeyError:
        error = "Missing ingredient_id"
    else:
        try:
            ingredient = subrecipe.measuredingredient_set.get(pk=ingredient_id)
        except MeasuredIngredient.DoesNotExist:
            error = "Ingredient does not exist"
        else:
            ingredient.delete()

    return HttpResponse(json.dumps({
        'success': not error,
        'error': error,
    }))


@has_models
def subrecipe_edit_ingredients(request, subrecipe):
    return render(request, 'recipe/recipe_edit/ingredients.html', {
        'measured_ingredients': subrecipe.measuredingredient_set.all(),
    })


@has_models
def subrecipe_edit_step_add(request, subrecipe):
    instance = Step(subrecipe=subrecipe)
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
def subrecipe_edit_step_delete(_request, _subrecipe, step):
    step.delete()
    return HttpResponse(json.dumps({
        'success': True,
    }))


@has_models
def subrecipe_edit_steps(request, subrecipe):
    return render(request, 'recipe/recipe_edit/steps.html', {
        'steps': subrecipe.step_set.all(),
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
def subrecipe_edit_step_move_up(_request, subrecipe, step):
    error = None
    previous_step = (subrecipe.step_set.filter(position__lt=step.position)
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
def subrecipe_edit_step_move_down(_request, subrecipe, step):
    error = None
    next_step = (subrecipe.step_set.filter(position__gt=step.position)
                 .order_by('position').first())
    if next_step is None:
        error = "There is no next step"
    else:
        _swap_steps(step, next_step)
    return HttpResponse(json.dumps({
        'success': not error,
        'error': error,
    }))


def _serialize_subrecipe(subrecipe):
    output = {}
    output['title'] = subrecipe.title
    output['ingredients'] = [{
        'amount': i.amount,
        'unit': i.unit.name,
        'ingredient': i.ingredient.name,
    } for i in subrecipe.measuredingredient_set.all()]
    output['steps'] = [s.text for s in subrecipe.step_set.all()]
    return output


def _serialize_recipe(recipe):
    output = {}
    output['title'] = recipe.title
    output['subrecipes'] = [_serialize_subrecipe(sr)
                            for sr in recipe.subrecipe_set.all()]
    return output


@has_models
def recipe_export(_request, recipe):
    output = _serialize_recipe(recipe)
    filename = "receta-{}-{}.json".format(recipe.id, slugify(recipe.title))
    response = HttpResponse(json.dumps(output, indent=1),
                            content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    return response


def recipe_export_all(_request):
    output = {}
    for recipe in Recipe.objects.all():
        output[recipe.id] = _serialize_recipe(recipe)
    now = datetime.datetime.now()
    filename = "recetas-{}.json".format(now.strftime("%Y-%m-%d.%H.%M.%S"))
    response = HttpResponse(json.dumps(output, indent=1, sort_keys=True),
                            content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    return response


def recipe_view(_request, _recipe):
    pass
