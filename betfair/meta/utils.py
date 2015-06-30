# -*- coding: utf-8 -*-

import functools

import six
import inflection


def convert_value(value, converter=None):
    return converter(value) if converter else value


def convert_dict(data, key_converter=None, value_converter=None):
    return {
        convert_value(key, key_converter): convert_value(value, value_converter)
        for key, value in six.iteritems(data)
    }


camelize = functools.partial(inflection.camelize, uppercase_first_letter=False)
serialize_dict = functools.partial(convert_dict, key_converter=camelize)
