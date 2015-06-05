# -*- coding: utf-8 -*-

import six
import copy
import inflection
import logging

from .meta.field import Field


logger = logging.getLogger(__name__)


class BetfairModel(object):
    """Model base class. Subclasses should define `Field` descriptors, which
    are collected in `_fields`. Note: to avoid circular definitions, the
    `ModelMeta` metaclass is not applied until after `BetrfairModel` has been
    defined.

    Handle conversions between internal (underscore) and external (camel-
    cased) key formatting; handle trailing underscores used to avoid conflicts
    with build-ins (e.g. from_).

    """
    def __init__(self, **kwargs):
        self.unserialize(kwargs)

    def serialize(self):
        return {
            key: value.serialize(self)
            for key, value in six.iteritems(self._fields)
        }

    def unserialize(self, kwargs):
        for key, value in six.iteritems(kwargs):
            if key not in self._fields:
                logger.warn('No field for {0} in model schema'.format(key))
            else:
                self._fields[key].__set__(self, value, safe=True)
        self.check_complete()

    def check_complete(self):
        missing = [
            key for key, value in six.iteritems(self._fields)
            if value.required
            and value.is_null(value.__get__(self, self.__class__))
        ]
        if missing:
            raise ValueError('Missing values on fields {0}'.format(
                ', '.join(missing)
            ))


def copy_fields(bases):
    """Deep-copy and collect `Field` descriptors from base classes.

    :param list bases: Base classes
    :returns: Dictionary of `Field` descriptors

    """
    fields = {}
    for base in bases[::-1]:
        if issubclass(base, BetfairModel):
            fields.update({
                key: copy.deepcopy(value)
                for key, value in six.iteritems(base._fields)
            })
    return fields


class ModelMeta(type):
    """Model metaclass. Collects field descriptors and inherits fields from
    parent.

    """
    def __init__(cls, name, bases, dct):
        cls._fields = copy_fields(bases)

        def serialize_key(key):
            return inflection.camelize(
                key, uppercase_first_letter=False
            ).rstrip('_')

        cls._fields.update({
            serialize_key(key): value
            for key, value in six.iteritems(dct)
            if isinstance(value, Field)
        })
        super(ModelMeta, cls).__init__(name, bases, dct)


# Apply metaclass to `BetfairModel`
BetfairModel = six.add_metaclass(ModelMeta)(BetfairModel)
