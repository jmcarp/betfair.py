# -*- coding: utf-8 -*-

import datetime
from dateutil.parser import parse as parse_date

from .meta.datatype import DataType


class EnumType(DataType):

    def serialize(self, value):
        return value.name if value else None

    def unserialize(self, value):
        processed = self.preprocess(value)
        if isinstance(processed, self.type):
            return processed
        try:
            return self.type[processed]
        except KeyError:
            raise ValueError('Value {0} is not a member of Enum {1}'.format(
                value,
                self.type,
            ))


class ModelType(DataType):

    def serialize(self, value):
        return value.serialize() if value else None

    def unserialize(self, value):
        value = self.preprocess(value)
        return self.type(**value)


def preprocess_date(date):
    if isinstance(date, datetime.datetime):
        return date
    return parse_date(date)

datetime_type = DataType(datetime.datetime, preprocessor=preprocess_date)
