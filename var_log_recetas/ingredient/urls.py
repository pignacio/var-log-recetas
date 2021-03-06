#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
from __future__ import absolute_import, unicode_literals

import logging

from django.conf.urls import patterns, url

from .views import (
    IngredientAddView, IngredientListView, IngredientModalAddView,
    IngredientUpdateView,
    MeasureUnitAddView, MeasureUnitListView,
    MeasureUnitGroupListView, MeasureUnitGroupAddView,
    MeasureUnitGroupUpdateView,
)


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

urlpatterns = patterns(  # pylint: disable=invalid-name
    'ingredient.views',
    url(r'^ingredient/?$', IngredientListView.as_view(), name='ingredient_list'),
    url(r'^ingredient/add/?$', IngredientAddView.as_view(), name='ingredient_add'),
    url(r'^ingredient/add/modal/?$', IngredientModalAddView.as_view(), name='ingredient_add_modal'),
    url(r'^ingredient/add/modal/submit/?$', IngredientModalAddView.as_view(partial=True), name='ingredient_add_modal_submit'),
    url(r'^ingredient/(?P<ingredient_id>\d+)/?$', IngredientUpdateView.as_view(), name='ingredient_update'),
    url(r'^unit/?$', MeasureUnitListView.as_view(), name='unit_list'),
    url(r'^unit/add/?$', MeasureUnitAddView.as_view(), name='unit_add'),
    url(r'^unit_group/?$', MeasureUnitGroupListView.as_view(), name='unit_group_list'),
    url(r'^unit_group/add/?$', MeasureUnitGroupAddView.as_view(), name='unit_group_add'),
    url(r'^unit_group/(?P<unit_group_id>\d+)/?$', MeasureUnitGroupUpdateView.as_view(), name='unit_group_update'),
)


