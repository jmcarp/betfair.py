# -*- coding: utf-8 -*-

import pytest

from enum import Enum
from schematics.types import StringType

from betfair.meta.types import EnumType
from betfair.meta.types import ModelType
from betfair.meta.models import BetfairModel


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
    ]
)

@pytest.mark.parametrize(['input', 'expected'], [
    ('val1', 'val1'),
    (FakeEnum.val1, 'val1'),
])
def test_enum_type(input, expected):
    class FakeModel(BetfairModel):
        enum_field = EnumType(FakeEnum)

    datum = FakeModel(enum_field=input)
    datum.validate()
    serialized = datum.serialize()
    assert serialized['enumField'] == expected


def test_nested_model():
    class Child(BetfairModel):
        child_name = StringType()

    class Parent(BetfairModel):
        parent_name = StringType()
        child = ModelType(Child)

    parent = Parent(parent_name='mom', child=dict(child_name='kid'))
    expected = {
        'parentName': 'mom',
        'child': {
            'childName': 'kid',
        },
    }
    assert parent.serialize() == expected
