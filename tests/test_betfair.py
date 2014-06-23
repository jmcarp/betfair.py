# -*- coding: utf-8 -*-

import pytest

import inspect
import requests
import itertools

from betfair import betfair
from betfair import exceptions

from tests import utils

from tests import fixtures
from tests.fixtures import client, logged_in_client
from tests.fixtures import login_success, login_failure
from tests.fixtures import keepalive_success, keepalive_failure
from tests.fixtures import logout_success, logout_failure


def test_client_init(client):
    assert client.app_key == 'test'
    assert client.cert_file == 'path/to/cert'
    assert client.content_type == 'application/json'
    assert isinstance(client.session, requests.Session)
    assert client.session_token is None


def test_headers(client):
    headers = client.headers
    expected = {
        'X-Application': client.app_key,
        'X-Authentication': client.session_token,
        'Content-Type': client.content_type,
        'Accept': 'application/json',
    }
    assert headers == expected


def test_login_success(client, login_success):
    client.login('name', 'pass')
    assert client.session_token == 'secret'


def test_login_error(client, login_failure):
    with pytest.raises(exceptions.BetfairLoginError) as excinfo:
        client.login('name', 'wrong')
    error = excinfo.value
    assert error.message == 'INVALID_USERNAME_OR_PASSWORD'


def test_keepalive_success(logged_in_client, keepalive_success):
    logged_in_client.keep_alive()


def test_keepalive_failure(logged_in_client, keepalive_failure):
    with pytest.raises(exceptions.BetfairAuthError) as excinfo:
        logged_in_client.keep_alive()
    error = excinfo.value
    assert error.message == 'NO_SESSION'


def test_logout_success(logged_in_client, logout_success):
    logged_in_client.logout()
    assert logged_in_client.session_token is None


def test_logout_failure(logged_in_client, logout_failure):
    with pytest.raises(exceptions.BetfairAuthError) as excinfo:
        logged_in_client.logout()
    error = excinfo.value
    assert error.message == 'NO_SESSION'


@pytest.mark.parametrize('method_name', fixtures.login_required_methods)
def test_requires_login(method_name, client, logged_in_client, monkeypatch):
    monkeypatch.setattr(betfair.Betfair, 'make_auth_request', utils.noop)
    monkeypatch.setattr(betfair.Betfair, 'make_api_request', utils.noop)
    monkeypatch.setattr(itertools, 'chain', utils.noop)
    method = getattr(client, method_name)
    argspec = inspect.getargspec(method)
    args = [None] * (len(argspec.args) - 1)
    with pytest.raises(exceptions.BetfairError):
        method(*args)
    logged_in_method = getattr(logged_in_client, method_name)
    logged_in_method(*args)
