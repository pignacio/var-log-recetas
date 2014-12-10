from django.contrib import admin

from .models import MeasureUnit, Ingredient, IngredientCategory


# Register your models here.

class IngredientAdmin(admin.ModelAdmin):
    list_fields = ('name', 'categories',)
    list_filter = ('categories',)
    search_fields = ('name',)


class MeasureUnitAdmin(admin.ModelAdmin):
    pass


class IngredientCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(MeasureUnit, MeasureUnitAdmin)
admin.site.register(IngredientCategory, IngredientCategoryAdmin)
