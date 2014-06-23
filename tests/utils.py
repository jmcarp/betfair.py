# -*- coding: utf-8 -*-

import pytest
import responses

import json


noop = lambda *args, **kwargs: None


def response_fixture_factory(url, data):
    @pytest.yield_fixture
    def fixture():
        responses.add(
            responses.POST,
            url,
            body=json.dumps(data),
            content_type='application/json',
        )
        responses.start()
        yield responses
        responses.stop()
        responses.reset()
    return fixture
