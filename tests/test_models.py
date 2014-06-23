# -*- coding: utf-8 -*-

import pytest

from betfair.models import BetfairModel
from betfair.meta import DataType, Field


@pytest.fixture
def model():
    class TestModel(BetfairModel):
        underscore_separated_field = Field(DataType(str))
        underscore_trailing_field_ = Field(DataType(str))
    return TestModel


def test_field_inflection(model):
    record = model(underscoreSeparatedField='test')
    assert record.underscore_separated_field == 'test'
    serialized = record.serialize()
    assert 'underscoreSeparatedField' in serialized
    assert serialized['underscoreSeparatedField'] == 'test'


def test_field_trailing_underscore(model):
    record = model(underscoreTrailingField='test')
    assert record.underscore_trailing_field_ == 'test'
    serialized = record.serialize()
    assert 'underscoreTrailingField' in serialized
    assert 'underscoreTrailingField_' not in serialized
    assert serialized['underscoreTrailingField'] == 'test'
