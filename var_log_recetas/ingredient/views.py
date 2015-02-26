#!/usr/bin/env python
# encoding: utf-8

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.generic import ListView, FormView, UpdateView

from .forms import IngredientForm, MeasureUnitForm
from .models import Ingredient, MeasureUnit


# Create your views here.


class IngredientListView(ListView):
    model = Ingredient


class IngredientAddView(FormView):
    form_class = IngredientForm
    template_name = 'generic/form.html'

    def form_valid(self, form):
        form.save()
        return redirect('ingredient_list')


class IngredientUpdateView(UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'generic/form.html'
    pk_url_kwarg = 'ingredient_id'
    success_url = reverse_lazy('ingredient_list')


class MeasureUnitListView(ListView):
    model = MeasureUnit


class MeasureUnitAddView(FormView):
    form_class = MeasureUnitForm
    template_name = 'generic/form.html'

    def form_valid(self, form):
        form.save()
        return redirect('unit_list')
