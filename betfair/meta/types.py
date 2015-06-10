# -*- coding: utf-8 -*-

from schematics import types
from schematics.types import compound
from schematics.exceptions import ConversionError
from schematics.exceptions import ValidationError

from . import utils


class DateTimeType(types.DateTimeType):

    DEFAULT_FORMATS = (
        '%Y-%m-%dT%H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%S.%fZ',
        '%Y-%m-%dT%H:%M:%S',
    )


class ModelType(compound.ModelType):

    def export_loop(self, *args, **kwargs):
        return utils.serialize_dict(super(ModelType, self).export_loop(*args, **kwargs))


class EnumType(types.BaseType):

    MESSAGES = {'choices': u'Value must belong to enum {0}.'}

    def __init__(self, enum, *args, **kwargs):
        super(EnumType, self).__init__(*args, **kwargs)
        self.enum = enum

    def _to_name(self, value, error):
        if isinstance(value, self.enum):
            return value.name
        try:
            return self.enum[value].name
        except KeyError:
            message = self.messages['choices'].format(self.enum.__name__)
            raise error(message)

    def validate_choice(self, value):
        self._to_name(value, ValidationError)

    def to_native(self, value, context=None):
        return self._to_name(value, ConversionError)
