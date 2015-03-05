#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from django.utils.translation import ugettext as _
from django.forms import ValidationError

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
import floppyforms.__future__ as forms

from .models import Recipe, MeasuredIngredient, Step, SubRecipe
from ingredient.models import Ingredient, MeasureUnit


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
            'unit',
        )

    ingredient_name = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super(MeasuredIngredientForm, self).__init__(*args, **kwargs)
        logger.debug("initial=%s", self.initial)
        logger.debug("data: %s", self.data)
        if self.is_bound and self.data.get('ingredient_name', None):
            ingredient_name = self.data.get('ingredient_name', None)
            logger.debug("Ingredient name from instance: '%s'", ingredient_name)
        else:
            ingredient_name = self.initial.get('ingredient_name', None)
            logger.debug("Ingredient name from initial: '%s'", ingredient_name)
        if ingredient_name:
            try:
                ingredient = Ingredient.objects.get(name=ingredient_name)
                units = ingredient.all_units()
            except (Ingredient.DoesNotExist, ValueError):
                units = MeasureUnit.objects.all()
        else:
            units = MeasureUnit.objects.all()

        self.fields['amount'].widget.attrs.update({
            'placeholder': 'Amount',
            'min': 0.001,
            'step': 'any',
        })
        self.fields['ingredient_name'].widget.attrs['placeholder'] = 'Ingredient'
        self.fields['ingredient_name'].empty_label = None
        self.fields['ingredient_name'].widget.datalist = [
            i.name for i in Ingredient.objects.all()]
        logging.debug("Units: %s", units)
        self.fields['unit'].queryset = MeasureUnit.objects.filter(id__in=[u.id for u in units])
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            'amount',
            'unit',
            'ingredient_name',
            Submit('submit', _('Agregar'),
                   css_class='btn-primary',
                   data_loading_text=_('Agregando...')),
        )

    def clean_ingredient_name(self):
        name = self.cleaned_data['ingredient_name']
        try:
            ingredient = Ingredient.objects.get(name=name)
        except Ingredient.DoesNotExist:
            raise ValidationError('Invalid ingredient')
        else:
            self.instance.ingredient = ingredient

    def clean(self):
        cleaned_data = super(MeasuredIngredientForm, self).clean()
        ingredient = cleaned_data.get('ingredient', None)
        unit = cleaned_data.get('unit', None)
        if (ingredient and unit and
                not ingredient.has_unit(unit)):
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
