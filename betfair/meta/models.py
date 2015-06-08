# -*- coding: utf-8 -*-

import functools

import six
import inflection
from schematics import models


def convert_value(value, converter=None):
    return converter(value) if converter else value


def convert_dict(data, key_converter=None, value_converter=None):
    return {
        convert_value(key, key_converter): convert_value(value, value_converter)
        for key, value in six.iteritems(data)
    }


unserialize_dict = functools.partial(convert_dict, key_converter=inflection.underscore)
camelize = functools.partial(inflection.camelize, uppercase_first_letter=False)
serialize_dict = functools.partial(convert_dict, key_converter=camelize)


class BetfairModel(models.Model):

    def __init__(self, **data):
        data = unserialize_dict(data)
        return super(BetfairModel, self).__init__(data)

    def serialize(self, *args, **kwargs):
        data = super(BetfairModel, self).serialize(*args, **kwargs)
        return serialize_dict(data)
