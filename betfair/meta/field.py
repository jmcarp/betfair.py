# -*- coding: utf-8 -*-

import weakref
import collections

from . import exceptions


class Field(object):

    def __init__(self, data_type, required=False):
        self.data_type = data_type
        self.required = required
        self.data = weakref.WeakKeyDictionary()

    def __get__(self, instance, owner):
        try:
            return self.data[instance]
        except KeyError:
            self.data[instance] = self.missing_value()
            return self.data[instance]

    def __set__(self, instance, value, safe=False):
        value = self.data_type.unserialize(value)
        if self.required and self.is_null(value) and not safe:
            raise exceptions.MissingValueError('Value must not be `None`')
        self.data[instance] = value

    def missing_value(self):
        return None

    def is_null(self, value):
        return value is None

    def serialize(self, instance):
        value = self.__get__(instance, None)
        return self.data_type.serialize(value)


class ListContainer(collections.MutableSequence):

    def __init__(self, data_type, value=None):
        self.data = []
        self.data_type = data_type
        for item in (value or []):
            self.append(item)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = self.data_type.unserialize(value)

    def __delitem__(self, key):
        del self.data[key]

    def __len__(self):
        return len(self.data)

    def insert(self, key, value):
        self.data.insert(key, self.data_type.unserialize(value))


class ListField(Field):

    def __set__(self, instance, value, safe=False):
        if self.required and self.is_null(value) and not safe:
            raise ValueError
        if not isinstance(value, collections.MutableSequence):
            raise ValueError
        self.data[instance] = ListContainer(self.data_type, value)

    def missing_value(self):
        return ListContainer(self.data_type)

    def is_null(self, value):
        return not value

    def serialize(self, instance):
        value = self.__get__(instance, None)
        return [
            self.data_type.serialize(item)
            for item in value
        ]
