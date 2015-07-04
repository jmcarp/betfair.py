# -*- coding: utf-8 -*-

from __future__ import absolute_import

import six
import json
import datetime
import collections

import enum
import decorator
from six.moves import http_client as httplib

from betfair import exceptions
from betfair.meta import utils
from betfair.meta.models import BetfairModel


def get_chunks(sequence, chunk_size):
    """Split sequence into chunks.

    :param list sequence:
    :param int chunk_size:
    """
    return [
        sequence[idx:idx + chunk_size]
        for idx in range(0, len(sequence), chunk_size)
    ]


def get_kwargs(kwargs):
    """Get all keys and values from dictionary where key is not `self`.

    :param dict kwargs: Input parameters
    """
    return {
        key: value for key, value in six.iteritems(kwargs)
        if key != 'self'
    }


def check_status_code(response, codes=None):
    """Check HTTP status code and raise exception if incorrect.

    :param Response response: HTTP response
    :param codes: List of accepted codes or callable
    :raises: ApiError if code invalid
    """
    codes = codes or [httplib.OK]
    checker = (
        codes
        if callable(codes)
        else lambda resp: resp.status_code in codes
    )
    if not checker(response):
        raise exceptions.ApiError(response, response.json())


def result_or_error(response):
    """Get `result` field from Betfair response or raise exception if not
    found.

    :param Response response:
    :raises: ApiError if no results passed
    """
    data = response.json()
    result = data.get('result')
    if result is not None:
        return result
    raise exceptions.ApiError(response, data)


def process_result(result, model=None):
    """Cast response JSON to Betfair model(s).

    :param result: Betfair response JSON
    :param BetfairModel model: Deserialization format; if `None`, return raw
        JSON
    """
    if model is None:
        return result
    if isinstance(result, collections.Sequence):
        return [model(**item) for item in result]
    return model(**result)


class BetfairEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        if isinstance(o, BetfairModel):
            o.validate()
            return o.serialize()
        if isinstance(o, enum.Enum):
            return o.name
        return super(BetfairEncoder, self).default(o)


def make_payload(base, method, params):
    """Build Betfair JSON-RPC payload.

    :param str base: Betfair base ("Sports" or "Account")
    :param str method: Betfair endpoint
    :param dict params: Request parameters
    """
    payload = {
        'jsonrpc': '2.0',
        'method': '{base}APING/v1.0/{endpoint}'.format(**locals()),
        'params': utils.serialize_dict(params),
        'id': 1,
    }
    return payload


@decorator.decorator
def requires_login(func, *args, **kwargs):
    """Decorator to check that the user is logged in. Raises `BetfairError`
    if instance variable `session_token` is absent.
    """
    self = args[0]
    if self.session_token:
        return func(*args, **kwargs)
    raise exceptions.NotLoggedIn()
