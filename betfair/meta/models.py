# -*- coding: utf-8 -*-

from schematics import types, models
from six import add_metaclass
import inflection


class AttributeCamelizingModelMeta(models.ModelMeta):
    """A meta class that sets serialied_name and deserialize_from on class
    schemactic type attributes to the camalized name of the attribute (unless
    serialied_name or deserialize_from has already been specified)"""

    def __new__(meta, name, bases, dct):
        for k in dct:
            v = dct[k]
            if isinstance(v, types.BaseType):
                camelized_name = inflection.camelize(k,
                    uppercase_first_letter=False)
                if v.serialized_name is None:
                    v.serialized_name = camelized_name
                if v.deserialize_from is None:
                    v.deserialize_from = camelized_name

        return super(AttributeCamelizingModelMeta, meta).__new__(meta, name,
                                                                 bases, dct)


@add_metaclass(AttributeCamelizingModelMeta)
class BetfairModel(models.Model):

    def __init__(self, **data):
        super(BetfairModel, self).__init__()
        self.import_data(data)

    def import_data(self, data, **kwargs):
        kwargs['strict'] = False
        return super(BetfairModel, self).import_data(data, **kwargs)
