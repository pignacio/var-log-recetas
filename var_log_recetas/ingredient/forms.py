import logging

import floppyforms.__future__ as forms
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Layout, Submit
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _

from .models import Ingredient, MeasureUnit, MeasureUnitGroup

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class MeasureUnitForm(forms.ModelForm):
    class Meta(object):
        model = MeasureUnit
        fields = (
            "name",
            "short_name",
        )

    def __init__(self, *args, **kwargs):
        super(MeasureUnitForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "name",
            "short_name",
            FormActions(
                ButtonHolder(
                    Submit(
                        "add",
                        _("Agregar"),
                        css_class="btn-default",
                        data_loading_text=_("Agregando..."),
                    ),
                    css_class="form-actions pull-right",
                ),
            ),
        )


class IngredientForm(forms.ModelForm):

    add_button = True
    form_action = None

    class Meta(object):
        model = Ingredient
        fields = (
            "name",
            "units",
            "unit_groups",
        )

        widgets = {
            "units": forms.CheckboxSelectMultiple,
            "unit_groups": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super(IngredientForm, self).__init__(*args, **kwargs)
        submit_text = _("Guardar") if self.instance.pk else _("Agregar")
        loading_text = _("Guardando...") if self.instance.pk else _("Agregando...")
        self.helper = FormHelper()
        self.helper.form_id = "ingredient-create-form"
        if self.form_action:
            self.helper.form_action = self.form_action
        self.helper.layout = Layout("name", "unit_groups", "units",)
        if self.add_button:
            self.helper.layout.append(
                FormActions(
                    ButtonHolder(
                        Submit(
                            "add",
                            submit_text,
                            css_class="btn-default",
                            data_loading_text=loading_text,
                        ),
                        css_class="form-actions pull-right",
                    ),
                ),
            )


class IngredientModalForm(IngredientForm):
    add_button = False
    form_action = reverse_lazy("ingredient_add_modal_submit")


class MeasureUnitGroupForm(forms.ModelForm):
    class Meta(object):
        model = MeasureUnitGroup
        fields = ("name", "units")

        widgets = {
            "units": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super(MeasureUnitGroupForm, self).__init__(*args, **kwargs)
        submit_text = _("Guardar") if self.instance.pk else _("Agregar")
        loading_text = _("Guardando...") if self.instance.pk else _("Agregando...")
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "name",
            "units",
            FormActions(
                ButtonHolder(
                    Submit(
                        "add",
                        submit_text,
                        css_class="btn-default",
                        data_loading_text=loading_text,
                    ),
                    css_class="form-actions pull-right",
                ),
            ),
        )
