# -*- coding: utf-8 -*-

import pytest

import json
import datetime

from schematics.exceptions import ValidationError

from betfair import models
from betfair import constants
from betfair.utils import BetfairEncoder
from betfair.utils import make_payload


def test_encode_enum():
    raw = {'enum': constants.MarketProjection.COMPETITION}
    encoded = json.loads(json.dumps(raw, cls=BetfairEncoder))
    assert encoded['enum'] == 'COMPETITION'


def test_encode_datetime():
    raw = {'date': datetime.datetime.now()}
    encoded = json.loads(json.dumps(raw, cls=BetfairEncoder))
    assert encoded['date'] == raw['date'].isoformat()


def test_encode_model():
    raw = {'model': models.PriceSize(price=1, size=2)}
    encoded = json.loads(json.dumps(raw, cls=BetfairEncoder))
    assert encoded['model'] == {'price': 1, 'size': 2}


def test_encode_model_invalid():
    raw = {'model': models.MarketDescription()}
    with pytest.raises(ValidationError):
        json.dumps(raw, cls=BetfairEncoder)


def test_make_payload():
    result = make_payload('Sports', 'listMarketBook', {'some_param': 123})
    assert result == {
        'jsonrpc': '2.0',
        'method': 'SportsAPING/v1.0/listMarketBook',
        'params': {'someParam': 123},
        'id': 1,
    }
