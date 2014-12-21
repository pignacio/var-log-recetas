#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
from __future__ import absolute_import, unicode_literals

import logging

from django.conf.urls import patterns, url


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


urlpatterns = patterns(  # pylint: disable=invalid-name
    'recipe.views',
    url(r'^$', 'home', name='recipe_home'),
    url(r'^add/?$', 'recipe_add', name='recipe_add'),
    url(r'^(?P<recipe_id>\d+)/?$', 'recipe_edit', name='recipe_recipe_edit'),
    url(r'^(?P<recipe_id>\d+)/ingredient_add/?$', 'recipe_edit_ingredient_add', name='recipe_recipe_edit_ingredient_add'),
    url(r'^(?P<recipe_id>\d+)/ingredient_delete/?$', 'recipe_edit_ingredient_delete', name='recipe_recipe_edit_ingredient_delete'),
    url(r'^(?P<recipe_id>\d+)/ingredients/?$', 'recipe_edit_ingredients', name='recipe_recipe_edit_ingredients'),
)
