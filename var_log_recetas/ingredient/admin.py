from django.contrib import admin

from .models import Ingredient, MeasureUnit


class IngredientAdmin(admin.ModelAdmin):
    list_fields = ("name",)
    search_fields = ("name",)


class MeasureUnitAdmin(admin.ModelAdmin):
    pass


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(MeasureUnit, MeasureUnitAdmin)
