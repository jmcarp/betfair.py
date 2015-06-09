# -*- coding: utf-8 -*-

import pytest

from betfair.price import nearest_price, price_ticks_away, ticks_difference


@pytest.mark.parametrize(('price', 'expected'), [
    (0.1, 1.01), (1, 1.01), (1000.1, 1000), (2000, 1000.0), (1.01, 1.01), (2.02, 2.02),
    (3.05, 3.05), (4.1, 4.1), (6.2, 6.2), (10.5, 10.5), (21, 21), (32, 32), (55, 55),
    (110, 110), (1.014, 1.01), (1.015, 1.02), (2.029, 2.02), (2.03, 2.04),
    (3.074, 3.05), (3.075, 3.1), (4.14, 4.1), (4.15, 4.2), (6.29, 6.2), (6.3, 6.4),
    (10.74, 10.5), (10.75, 11), (21.4, 21), (21.5, 22), (32.9, 32), (33, 34), (57.4, 55),
    (57.5, 60), (114, 110), (115, 120), (float('inf'), 1000.0)
])
def test_nearest_price(price, expected):
    assert nearest_price(price) == expected


@pytest.mark.parametrize(('price_1', 'price_2', 'expected'), [
    (1.01, 1.01, 0), (1.01, 1.02, 1), (2.0, 2.02, 1), (3.00, 3.05, 1),
    (4.0, 4.1, 1), (6.0, 6.2, 1), (10, 10.5, 1), (20, 21, 1), (30, 32, 1),
    (50, 55, 1), (100, 110, 1), (1.01, 1000.0, 349)
])
def test_ticks_difference(price_1, price_2, expected):
    assert ticks_difference(price_1, price_2) == expected


@pytest.mark.parametrize(('price', 'n_ticks', 'expected'), [
    (1.01, 0, 1.01), (1.01, 1, 1.02), (2.0, 1, 2.02), (3.00, 1, 3.05),
    (4.0, 1, 4.1), (6.0, 1, 6.2), (10, 1, 10.5), (20, 1, 21), (30, 1, 32),
    (50, 1, 55), (100, 1, 110), (1.02, -1, 1.01), (2.02, -1, 2.00),
    (3.05, -1, 3.00), (4.1, -1, 4.0), (6.2, -1, 6.0), (10.5, -1, 10),
    (21, -1, 20), (32, -1, 30), (55, -1, 50), (110, -1, 100)
])
def test_price_ticks_away(price, n_ticks, expected):
    assert price_ticks_away(price, n_ticks) == expected
