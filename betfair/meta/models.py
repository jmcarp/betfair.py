# -*- coding: utf-8 -*-

import six
import inflection
from schematics import types
from schematics import models


class BetfairModelMeta(models.ModelMeta):
    """Set default `serialized_name` and `deserialize_from` of Schematics types
    to camel-cased attribute names.
    """
    def __new__(meta, name, bases, attrs):
        for name, attr in six.iteritems(attrs):
            if isinstance(attr, types.BaseType):
                camelized = inflection.camelize(name, uppercase_first_letter=False)
                attr.serialized_name = attr.serialized_name or camelized
                attr.deserialize_from = attr.deserialize_from or camelized
        return super(BetfairModelMeta, meta).__new__(meta, name, bases, attrs)


class BetfairModel(six.with_metaclass(BetfairModelMeta, models.Model)):

    def __init__(self, **data):
        super(BetfairModel, self).__init__()
        self.import_data(data)

    def import_data(self, data, **kwargs):
        kwargs['strict'] = False
        return super(BetfairModel, self).import_data(data, **kwargs)
