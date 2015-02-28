#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
from __future__ import absolute_import, unicode_literals

import logging

from django.conf.urls import patterns, url

from .views import (
    RecipeCreateView, RecipeListView, RecipeEditView, SubRecipeDetailView,
    SubRecipeRenameView, RecipePartsView, RecipeAddPartView
)

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


urlpatterns = patterns(  # pylint: disable=invalid-name
    'recipe.views',
    url(r'^$', RecipeListView.as_view(), name='recipe_home'),
    url(r'^add/?$', RecipeCreateView.as_view(), name='recipe_add'),
    url(r'^(?P<recipe_id>\d+)/?$', 'recipe_view', name='recipe_view'),
    url(r'^(?P<recipe_id>\d+)/edit/?$', RecipeEditView.as_view(), name='recipe_edit'),
    url(r'^(?P<recipe_id>\d+)/parts/?$', RecipePartsView.as_view(), name='recipe_parts'),
    url(r'^(?P<recipe_id>\d+)/parts/add/?$', RecipeAddPartView.as_view(), name='recipe_parts_add'),
    url(r'^(?P<recipe_id>\d+)/export/?$', 'recipe_export', name='recipe_export'),
    url(r'^part/(?P<subrecipe_id>\d+)/?$', SubRecipeDetailView.as_view(), name='subrecipe_edit'),
    url(r'^part/(?P<subrecipe_id>\d+)/rename/?$', SubRecipeRenameView.as_view(), name='subrecipe_rename'),
    url(r'^part/(?P<subrecipe_id>\d+)/ingredient_add/?$', 'subrecipe_edit_ingredient_add', name='subrecipe_edit_ingredient_add'),
    url(r'^part/(?P<subrecipe_id>\d+)/ingredient_delete/?$', 'subrecipe_edit_ingredient_delete', name='subrecipe_edit_ingredient_delete'),
    url(r'^part/(?P<subrecipe_id>\d+)/ingredients/?$', 'subrecipe_edit_ingredients', name='subrecipe_edit_ingredients'),
    url(r'^part/(?P<subrecipe_id>\d+)/step_add/?$', 'subrecipe_edit_step_add', name='subrecipe_edit_step_add'),
    url(r'^part/(?P<subrecipe_id>\d+)/step_delete/?$', 'subrecipe_edit_step_delete', name='subrecipe_edit_step_delete'),
    url(r'^part/(?P<subrecipe_id>\d+)/step_move_up/?$', 'subrecipe_edit_step_move_up', name='subrecipe_edit_step_move_up'),
    url(r'^part/(?P<subrecipe_id>\d+)/step_move_down/?$', 'subrecipe_edit_step_move_down', name='subrecipe_edit_step_move_down'),
    url(r'^part/(?P<subrecipe_id>\d+)/steps/?$', 'subrecipe_edit_steps', name='subrecipe_edit_steps'),
)
