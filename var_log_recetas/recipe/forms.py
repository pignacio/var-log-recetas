#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from django.utils.translation import ugettext as _

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
import floppyforms.__future__ as forms

from .models import Recipe, MeasuredIngredient, Step, SubRecipe
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
        if self.is_bound and self.data.get('ingredient', None):
            try:
                ingredient = Ingredient.objects.get(pk=self.data.get('ingredient',None))
                logger.debug("Ingredient from instance: %s", ingredient)
            except (Ingredient.DoesNotExist, ValueError):
                ingredient = None
        else:
            ingredient = self.initial.get('ingredient', None)
            logger.debug("Ingredient from initial: %s", ingredient)
        if ingredient is None:
            ingredient = Ingredient.objects.all()[0]
            logger.debug("Ingredient from nowhere: %s", ingredient)
        logger.debug("Ingredient: %s", ingredient)
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
        ingredient = cleaned_data.get('ingredient', None)
        unit = cleaned_data.get('unit', None)
        if (ingredient and unit and
                not ingredient.units.filter(id=unit.id).exists()):
            raise forms.ValidationError(_("Unit and Ingredient do not match"))
        return cleaned_data


class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = (
            'text',
        )
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'cols':140,
                                          'style': 'resize: none;'})
        }

    def __init__(self, *args, **kwargs):
        super(StepForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            'text',
            Submit('submit', _('Agregar'),
                   css_class='btn-primary',
                   data_loading_text=_('Agregando...')),
        )


class SubRecipeSelectForm(forms.Form):
    def __init__(self, recipe, *args, **kwargs):
        super(SubRecipeSelectForm, self).__init__(*args, **kwargs)
        self.fields['subrecipe'] = forms.ChoiceField(
            choices=[(sr.pk, sr.title) for sr in recipe.subrecipe_set.all()],
            label=_("Parte"),
        )
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_id = 'select-subrecipe-form'


class SubRecipeForm(forms.ModelForm):
    class Meta:
        model = SubRecipe
        fields = (
            'title',
        )

    def __init__(self, *args, **kwargs):
        super(SubRecipeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            'title',
            Submit('submit', _('Guardar'),
                   css_class='btn-primary',
                   data_loading_text=_('Guardando...')),
        )
