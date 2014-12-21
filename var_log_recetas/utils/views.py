#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import functools
import logging

from django.http import Http404


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def _view_models():
    from recipe.models import Recipe
    return {
        'recipe': Recipe,
    }


def has_models(view):
    @functools.wraps(view)
    def new_view(*args, **kwargs):
        for key, model in _view_models().items():
            try:
                model_pk = kwargs.pop(key + '_id')
            except KeyError:
                pass
            else:
                try:
                    instance = model.objects.get(pk=model_pk)
                except model.DoesNotExist:
                    raise Http404
                kwargs[key] = instance
        return view(*args, **kwargs)
    return new_view

