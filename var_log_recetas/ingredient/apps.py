from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class IngredientConfig(AppConfig):
    name = "var_log_recetas.ingredient"
    verbose_name = _("Ingredients")
