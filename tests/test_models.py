# -*- coding: utf-8 -*-

import pytest

from enum import Enum
from schematics.models import Model
from schematics.types import StringType
from schematics.types.compound import ModelType
from six import with_metaclass

from betfair.meta.types import EnumType
from betfair.meta.models import BetfairModel
from betfair.meta.models import BetfairModelMeta


class FakeModel(with_metaclass(BetfairModelMeta, Model)):
    unchanged = StringType()
    camelized_field = StringType()
    serialize_override = StringType(serialized_name='abc')
    deserialize_override = StringType(deserialize_from='def')
    both_override = StringType(serialized_name='hij', deserialize_from='klm')


@pytest.mark.parametrize(('attr', 'value'), [
    (FakeModel.unchanged.serialized_name, 'unchanged'),
    (FakeModel.unchanged.deserialize_from, 'unchanged'),
    (FakeModel.camelized_field.serialized_name, 'camelizedField'),
    (FakeModel.camelized_field.deserialize_from, 'camelizedField'),
    (FakeModel.serialize_override.serialized_name, 'abc'),
    (FakeModel.serialize_override.deserialize_from, 'serializeOverride'),
    (FakeModel.deserialize_override.serialized_name, 'deserializeOverride'),
    (FakeModel.deserialize_override.deserialize_from, 'def'),
    (FakeModel.both_override.serialized_name, 'hij'),
    (FakeModel.both_override.deserialize_from, 'klm'),
])
def test_model_meta(attr, value):
    assert attr == value


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
