#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import functools
import logging

from django.http import Http404

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def _view_models():
    from var_log_recetas.recipe.models import (
        Recipe,
        MeasuredIngredient,
        Step,
        SubRecipe,
    )

    return {
        "recipe": Recipe,
        "subrecipe": SubRecipe,
        "measured_ingredient": MeasuredIngredient,
        "step": Step,
    }


class ModelExtractionError(Exception):
    pass


class MissingIdError(ModelExtractionError):
    pass


class MissingObjectError(ModelExtractionError):
    pass


_EXTRACT_MODEL_SENTINEL = object()


def _extract_model(objects, key, pop=True, default=_EXTRACT_MODEL_SENTINEL):
    logger.debug(
        "Extracting model '%s' from %s. pop=%s, default=%s", key, object, pop, default
    )
    try:
        model = _view_models()[key]
    except KeyError:
        raise ValueError("Invalid model key: '{}'".format(key))
    logger.debug("Model: '%s'", model)

    action = objects.pop if pop else objects.__getitem__
    try:
        model_pk = action(key + "_id")
    except KeyError:
        if default != _EXTRACT_MODEL_SENTINEL:
            return default
        raise MissingIdError("Missing {}_id.".format(key))

    try:
        return model.objects.get(pk=model_pk)
    except (model.DoesNotExist, TypeError):
        if default != _EXTRACT_MODEL_SENTINEL:
            return default
        raise MissingObjectError("Invalid {}_id: '{}'".format(key, model_pk))


def _has_models(view):
    def new_view(request, *args, **kwargs):
        logger.debug("_has_models: args:%s, kwargs:%s", args, kwargs)
        for key in _view_models():
            logger.debug("_has_models: checking for key: '%s'", key)
            try:
                instance = _extract_model(kwargs, key)
            except MissingIdError:
                logger.debug("_has_models: missing %s id", key)
            except MissingObjectError:
                logger.debug("_has_models: missing %s object. Raising 404", key)
                raise Http404
            else:
                logger.debug("_has_models: setting kwargs[%s] = %s", key, instance)
                kwargs[key] = instance
        logger.debug(
            "_has_models: calling original view with: args=%s, kwargs=%s", args, kwargs
        )
        return view(request, *args, **kwargs)

    return new_view


def has_models(view):
    return check_relations(_has_models(view))


def check_relations(view):
    @functools.wraps(view)
    def new_view(*args, **kwargs):
        models = {k: kwargs.get(k, None) for k in _view_models()}

        if models["measured_ingredient"]:
            if (
                models["subrecipe"]
                and models["subrecipe"] != models["measured_ingredient"].subrecipe
            ):
                raise Http404
            else:
                models["subrecipe"] = models["measured_ingredient"].subrecipe

        if models["step"]:
            if models["subrecipe"] and models["subrecipe"] != models["step"].subrecipe:
                raise Http404
            else:
                models["subrecipe"] = models["step"].subrecipe

        if models["subrecipe"]:
            if models["recipe"] and models["recipe"] != models["subrecipe"].recipe:
                raise Http404
            else:
                models["recipe"] = models["subrecipe"].recipe

        return view(*args, **kwargs)

    return new_view


def _has_get_models(*expected, **kwargs):
    on_error = kwargs.get("on_error", None)
    own_namespace = kwargs.get("own_namespace", False)

    def decorator(view):
        @_has_models
        def new_view(request, *args, **kwargs):
            logger.debug("_has_get_models: args:%s, kwargs:%s", args, kwargs)
            for model in expected:
                logger.debug("_has_get_models: checking for key: '%s'", model)
                try:
                    instance = _extract_model(request.GET, model, pop=False)
                except ModelExtractionError as err:
                    logger.debug(
                        "_has_get_models: extraction error for %s: %s", model, err
                    )
                    if on_error:
                        return on_error(err, *args, **kwargs)
                    continue
                key = "get_" + model if own_namespace or model in kwargs else model
                logger.debug("_has_get_models: setting kwargs[%s] = %s", key, instance)
                kwargs[key] = instance
            logger.debug(
                "_has_get_models: calling original view with: " "args=%s, kwargs=%s",
                args,
                kwargs,
            )
            return view(request, *args, **kwargs)

        return new_view

    return decorator


def has_get_models(view=None, **kwargs):
    return check_relations(_has_get_models(view, **kwargs))


class GenericFormMixin(object):
    template_name = "generic/form.html"
    title = "Generic form template"

    def get_context_data(self, *args, **kwargs):
        data = super(GenericFormMixin, self).get_context_data(*args, **kwargs)
        data["title"] = self.title
        return data
