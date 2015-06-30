# -*- coding: utf-8 -*-

import pytest

from enum import Enum
from schematics.models import Model
from schematics.types import StringType
from schematics.types.compound import ModelType
from six import with_metaclass

from betfair.meta.types import EnumType
from betfair.meta.models import AttributeCamelizingModelMeta, BetfairModel


def test_attribute_camalizing_model_meta():
    class FakeModel(with_metaclass(AttributeCamelizingModelMeta, Model)):
        unchanged = StringType()
        camelized_field = StringType()
        serialized_name_override = StringType(serialized_name='abc')
        deserialize_from_override = StringType(deserialize_from='def')
        both_overriden = StringType(serialized_name='hij',
                                    deserialize_from='klm')
    assert FakeModel.unchanged.serialized_name == 'unchanged'
    assert FakeModel.unchanged.deserialize_from == 'unchanged'
    assert FakeModel.camelized_field.serialized_name == 'camelizedField'
    assert FakeModel.camelized_field.deserialize_from == 'camelizedField'
    assert FakeModel.serialized_name_override.serialized_name == 'abc'
    assert FakeModel.serialized_name_override.deserialize_from \
        == 'serializedNameOverride'
    assert FakeModel.deserialize_from_override.serialized_name \
        == 'deserializeFromOverride'
    assert FakeModel.deserialize_from_override.deserialize_from == 'def'
    assert FakeModel.both_overriden.serialized_name == 'hij'
    assert FakeModel.both_overriden.deserialize_from == 'klm'


def test_field_inflection():
    class FakeModel(BetfairModel):
        underscore_separated_field = StringType()

    record = FakeModel(underscoreSeparatedField='test')
    assert record.underscore_separated_field == 'test'
    serialized = record.serialize()
    assert 'underscoreSeparatedField' in serialized
    assert serialized['underscoreSeparatedField'] == 'test'


FakeEnum = Enum(
    'TestEnum', [
        'val1',
        'val2',
        'SOME_VALUE'
    ]
)

@pytest.mark.parametrize(['input', 'expected'], [
    ('val1', 'val1'),
    (FakeEnum.val1, 'val1'),
    (FakeEnum.SOME_VALUE, 'SOME_VALUE')
])
def test_enum_type(input, expected):
    class FakeModel(BetfairModel):
        enum_field = EnumType(FakeEnum)

    datum = FakeModel(enum_field=input)
    datum.validate()
    serialized = datum.serialize()
    assert serialized['enumField'] == expected


class Child(BetfairModel):
    child_name = StringType()

class Parent(BetfairModel):
    parent_name = StringType()
    first_child = ModelType(Child)


def test_nested_model():
    parent = Parent(parent_name='mom', first_child=dict(child_name='kid'))
    expected = {
        'parentName': 'mom',
        'firstChild': {
            'childName': 'kid',
        },
    }
    assert parent.serialize() == expected


def test_nested_model_unserialize_rogue():
    Parent(parent_name='dad', child=dict(child_name='kid', rogue='rogue'))
