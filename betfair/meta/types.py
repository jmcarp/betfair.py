# -*- coding: utf-8 -*-

from schematics.types import BaseType
from schematics.exceptions import ConversionError
from schematics.exceptions import ValidationError


class EnumType(BaseType):

    MESSAGES = {'choices': u'Value must belong to enum {0}.'}

    def __init__(self, enum, *args, **kwargs):
        super(EnumType, self).__init__(*args, **kwargs)
        self.enum = enum

    def _to_name(self, value, error):
        if isinstance(value, self.enum):
            return value.name
        try:
            self.enum[value]
        except KeyError:
            message = self.messages['choices'].format(self.enum.__name__)
            raise error(message)

    def validate_choice(self, value):
        self._to_name(value, ValidationError)

    def to_native(self, value, context=None):
        return self._to_name(value, ConversionError)
