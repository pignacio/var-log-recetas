#!/usr/bin/env python
# encoding: utf-8
# pylint: disable=too-few-public-methods

from django.contrib import admin

from .models import Recipe


class RecipeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Recipe, RecipeAdmin)
