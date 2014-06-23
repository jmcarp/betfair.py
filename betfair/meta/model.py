# -*- coding: utf-8 -*-

import six
import copy

from .field import Field


class Model(object):
    """Model base class. Subclasses should define `Field` descriptors, which
    are collected in `_fields`. Note: to avoid circular definitions, the
    `ModelMeta` metaclass is not applied until after `Model` has been defined.

    """
    def __init__(self, **kwargs):
        self.unserialize(kwargs)

    def serialize_key(self, key):
        return key

    def unserialize_key(self, key):
        return key

    def serialize(self):
        return {
            self.serialize_key(key): value.serialize(self)
            for key, value in six.iteritems(self._fields)
        }
        
    def unserialize(self, kwargs):
        for key, value in six.iteritems(kwargs):
            key = self.unserialize_key(key)
            if key not in self._fields:
                raise ValueError('Key {0} not in model schema'.format(key))
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
        if issubclass(base, Model):
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
        cls._fields.update({
            key: value
            for key, value in six.iteritems(dct)
            if isinstance(value, Field)
        })
        super(ModelMeta, cls).__init__(name, bases, dct)


# Apply metaclass to `Model`
Model = six.add_metaclass(ModelMeta)(Model)
