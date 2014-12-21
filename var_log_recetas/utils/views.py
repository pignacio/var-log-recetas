#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import functools
import logging

from django.http import Http404


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def _view_models():
    from recipe.models import Recipe, MeasuredIngredient
    return {
        'recipe': Recipe,
        'measured_ingredient': MeasuredIngredient,
    }


def has_models(view):
    @functools.wraps(view)
    @check_relations
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


def check_relations(view):
    @functools.wraps(view)
    def new_view(*args, **kwargs):
        models = {k: kwargs.get(k, None) for k in _view_models()}

        if models['measured_ingredient']:
            if (models['recipe'] and
                    models['recipe'] != models['measured_ingredient'].recipe):
                raise Http404
            else:
                models['recipe'] = models['measured_ingredient'].recipe

        return view(*args, **kwargs)
    return new_view
