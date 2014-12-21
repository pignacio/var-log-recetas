#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from django.utils.translation import ugettext as _

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
import floppyforms.__future__ as forms

from .models import Recipe, MeasuredIngredient
from ingredient.models import Ingredient


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class RecipeAddForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'title',
        )

    def __init__(self, *args, **kwargs):
        super(RecipeAddForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            'title',
            FormActions(
                Submit('submit', _('Agregar'),
                       css_class='btn-primary pull-right',
                       data_loading_text=_('Agregando...')),
            )
        )



class MeasuredIngredientForm(forms.ModelForm):
    class Meta:
        model = MeasuredIngredient
        fields = (
            'amount',
            'ingredient',
            'unit',
        )

    def __init__(self, *args, **kwargs):
        super(MeasuredIngredientForm, self).__init__(*args, **kwargs)
        logger.debug("initial=%s", self.initial)
        try:
            ingredient = self.instance.ingredient
        except Ingredient.DoesNotExist:
            if not self.initial['ingredient']:
                self.initial['ingredient'] = Ingredient.objects.all()[0]
            ingredient = self.initial['ingredient']
        self.fields['ingredient'].empty_label = None
        self.fields['unit'].queryset = ingredient.units.all()
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            'ingredient',
            'amount',
            'unit',
            Submit('submit', _('Agregar'),
                   css_class='btn-primary',
                   data_loading_text=_('Agregando...')),
        )

    def clean(self):
        cleaned_data = super(MeasuredIngredientForm, self).clean()
        logger.info("ingredients=%s, unit=%s", cleaned_data['ingredient'], cleaned_data['unit'])
        if (cleaned_data['ingredient'] and cleaned_data['unit'] and not
            cleaned_data['ingredient'].units.filter(id=cleaned_data['unit'].id).exists()):
            raise forms.ValidationError(_("Unit and Ingredient do not match"))
        return cleaned_data
