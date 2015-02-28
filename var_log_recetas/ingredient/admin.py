#!/usr/bin/env python
# encoding: utf-8
# pylint: disable=too-few-public-methods

from django.contrib import admin

from .models import MeasureUnit, Ingredient


# Register your models here.

class IngredientAdmin(admin.ModelAdmin):
    list_fields = ('name',)
    search_fields = ('name',)


class MeasureUnitAdmin(admin.ModelAdmin):
    pass


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(MeasureUnit, MeasureUnitAdmin)
