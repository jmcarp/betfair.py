# -*- coding: utf-8 -*-

import json
import datetime

from betfair import models
from betfair import constants
from betfair.utils import BetfairEncoder


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
