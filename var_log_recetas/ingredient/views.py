#!/usr/bin/env python
# encoding: utf-8
# pylint: disable=too-few-public-methods,too-many-ancestors

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views.generic import ListView, FormView, UpdateView

from utils.views import GenericFormMixin
from .forms import (
    IngredientForm, MeasureUnitForm, MeasureUnitGroupForm, IngredientModalForm)
from .models import Ingredient, MeasureUnit, MeasureUnitGroup


# Create your views here.


class IngredientListView(ListView):
    model = Ingredient


class IngredientAddView(GenericFormMixin, FormView):
    form_class = IngredientForm
    title = _("Agregar ingrediente")

    def form_valid(self, form):
        form.save()
        return redirect('ingredient_list')


class IngredientModalAddView(FormView):
    form_class = IngredientModalForm
    template_name = "modal_form_base.html"
    partial = False

    def form_valid(self, form):
        form.save()
        return HttpResponse('1')

    def get_context_data(self, *args, **kwargs):
        data = super(IngredientModalAddView, self).get_context_data(
            *args, **kwargs)
        data['partial'] = self.partial
        data['id'] = 'ingredient-create'
        data['title'] = _('Agregar ingrediente')
        return data


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


class MeasureUnitGroupListView(ListView):
    model = MeasureUnitGroup


class MeasureUnitGroupAddView(GenericFormMixin, FormView):
    form_class = MeasureUnitGroupForm
    title = _("Agregar grupo de unidades")

    def form_valid(self, form):
        form.save()
        return redirect('unit_group_list')


class MeasureUnitGroupUpdateView(GenericFormMixin, UpdateView):
    model = MeasureUnitGroup
    form_class = MeasureUnitGroupForm
    pk_url_kwarg = 'unit_group_id'
    success_url = reverse_lazy('unit_group_list')
    title = _("Modificar grupo de unidades")
