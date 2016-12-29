# -*- coding: utf-8 -*-

import pytest

import os

from betfair import betfair
from tests.utils import response_fixture_factory


@pytest.fixture
def client():
    return betfair.Betfair(app_key='test', cert_file='path/to/cert')


@pytest.fixture
def logged_in_client(client):
    client = betfair.Betfair(app_key='test', cert_file='path/to/cert')
    client.session_token = 'secret'
    return client


login_success = response_fixture_factory(
    os.path.join(betfair.IDENTITY_URLS[None], 'certlogin'),
    {
        'loginStatus': 'SUCCESS',
        'sessionToken': 'secret',
    },
)

login_failure = response_fixture_factory(
    os.path.join(betfair.IDENTITY_URLS[None], 'certlogin'),
    {'loginStatus': 'INVALID_USERNAME_OR_PASSWORD'},
)

login_bad_code = response_fixture_factory(
    os.path.join(betfair.IDENTITY_URLS[None], 'certlogin'),
    status=422,
)

keepalive_success = response_fixture_factory(
    os.path.join(betfair.IDENTITY_URLS[None], 'keepAlive'),
    {'status': 'SUCCESS'},
)

keepalive_failure = response_fixture_factory(
    os.path.join(betfair.IDENTITY_URLS[None], 'keepAlive'),
    {
        'status': 'FAIL',
        'error': 'NO_SESSION',
    },
)

logout_success = response_fixture_factory(
    os.path.join(betfair.IDENTITY_URLS[None], 'logout'),
    {'status': 'SUCCESS'},
)

logout_failure = response_fixture_factory(
    os.path.join(betfair.IDENTITY_URLS[None], 'logout'),
    {
        'status': 'FAIL',
        'error': 'NO_SESSION',
    },
)

login_required_methods = [
    'keep_alive',
    'logout',
    'list_event_types',
    'list_competitions',
    'list_time_ranges',
    'list_events',
    'list_market_types',
    'list_countries',
    'list_venues',
    'list_market_catalogue',
    'list_market_book',
    'list_market_profit_and_loss',
    'list_current_orders',
    'list_cleared_orders',
    'place_orders',
    'cancel_orders',
    'replace_orders',
    'update_orders',
]
