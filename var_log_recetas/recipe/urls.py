#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
from __future__ import absolute_import, unicode_literals

import logging

from django.urls import path

from . import views

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


urlpatterns = [
    path("", views.RecipeListView.as_view(), name="recipe_home"),
    path("add/", views.RecipeCreateView.as_view(), name="recipe_add"),
    path("export/", views.recipe_export_all, name="recipe_export_all"),
    path("<int:recipe_id>/", views.recipe_view, name="recipe_view"),
    path("<int:recipe_id>/edit/", views.RecipeEditView.as_view(), name="recipe_edit"),
    path(
        "<int:recipe_id>/parts/", views.RecipePartsView.as_view(), name="recipe_parts"
    ),
    path(
        "<int:recipe_id>/parts/add/",
        views.RecipeAddPartView.as_view(),
        name="recipe_parts_add",
    ),
    path("<int:recipe_id>/export/", views.recipe_export, name="recipe_export"),
    path(
        "part/<int:subrecipe_id>/",
        views.SubRecipeDetailView.as_view(),
        name="subrecipe_edit",
    ),
    path(
        "part/<int:subrecipe_id>/rename/",
        views.SubRecipeRenameView.as_view(),
        name="subrecipe_rename",
    ),
    path(
        "part/<int:subrecipe_id>/ingredient_add/",
        views.subrecipe_edit_ingredient_add,
        name="subrecipe_edit_ingredient_add",
    ),
    path(
        "part/<int:subrecipe_id>/ingredient_delete/",
        views.subrecipe_edit_ingredient_delete,
        name="subrecipe_edit_ingredient_delete",
    ),
    path(
        "part/<int:subrecipe_id>/ingredients/",
        views.subrecipe_edit_ingredients,
        name="subrecipe_edit_ingredients",
    ),
    path(
        "part/<int:subrecipe_id>/step_add/",
        views.subrecipe_edit_step_add,
        name="subrecipe_edit_step_add",
    ),
    path(
        "part/<int:subrecipe_id>/step_delete/",
        views.subrecipe_edit_step_delete,
        name="subrecipe_edit_step_delete",
    ),
    path(
        "part/<int:subrecipe_id>/step_move_up/",
        views.subrecipe_edit_step_move_up,
        name="subrecipe_edit_step_move_up",
    ),
    path(
        "part/<int:subrecipe_id>/step_move_down/",
        views.subrecipe_edit_step_move_down,
        name="subrecipe_edit_step_move_down",
    ),
    path(
        "part/<int:subrecipe_id>/steps/",
        views.subrecipe_edit_steps,
        name="subrecipe_edit_steps",
    ),
]
