#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
from __future__ import absolute_import, unicode_literals

import logging

from django.conf.urls import patterns, url


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


urlpatterns = patterns(  # pylint: disable=invalid-name
    'recipe.views',
    url(r'^(?P<recipe_id>\d+)/?$', 'recipe_show', name='recipe_recipe_show')
    url(r'^$', 'home', name='recipe_home'),
)
