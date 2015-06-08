# -*- coding: utf-8 -*-

import pytest

from schematics.types import StringType

from betfair.meta.models import BetfairModel


@pytest.fixture
def model():
    class TestModel(BetfairModel):
        underscore_separated_field = StringType()
    return TestModel


def test_field_inflection(model):
    record = model(underscoreSeparatedField='test')
    assert record.underscore_separated_field == 'test'
    serialized = record.serialize()
    assert 'underscoreSeparatedField' in serialized
    assert serialized['underscoreSeparatedField'] == 'test'
