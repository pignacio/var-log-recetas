#!/usr/bin/env python
# encoding: utf-8
# pylint: disable=too-few-public-methods,too-many-ancestors

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views.generic import ListView, FormView, UpdateView

from utils.views import GenericFormMixin
from .forms import IngredientForm, MeasureUnitForm
from .models import Ingredient, MeasureUnit


# Create your views here.


class IngredientListView(ListView):
    model = Ingredient


class IngredientAddView(GenericFormMixin, FormView):
    form_class = IngredientForm
    title = _("Agregar ingrediente")

    def form_valid(self, form):
        form.save()
        return redirect('ingredient_list')


class IngredientUpdateView(GenericFormMixin, UpdateView):
    model = Ingredient
    form_class = IngredientForm
    pk_url_kwarg = 'ingredient_id'
    success_url = reverse_lazy('ingredient_list')
    title = _("Modificar ingrediente")


class MeasureUnitListView(ListView):
    model = MeasureUnit


class MeasureUnitAddView(GenericFormMixin, FormView):
    form_class = MeasureUnitForm
    title = _('Agregar unidad')

    def form_valid(self, form):
        form.save()
        return redirect('unit_list')
