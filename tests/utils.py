# -*- coding: utf-8 -*-

import pytest
import responses

import json


noop = lambda *args, **kwargs: None


def response_fixture_factory(url, data=None, status=200):
    @pytest.yield_fixture
    def fixture():
        responses.add(
            responses.POST,
            url,
            status=status,
            body=json.dumps(data or {}),
            content_type='application/json',
        )
        responses.start()
        yield responses
        responses.stop()
        responses.reset()
    return fixture
