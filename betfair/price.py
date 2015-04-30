# -*- coding: utf-8 -*-

from __future__ import division

from decimal import Decimal, ROUND_HALF_UP


CUTOFFS = (
    (2, 100),
    (3, 50),
    (4, 20),
    (6, 10),
    (10, 5),
    (20, 2),
    (30, 1),
    (50, 0.5),
    (100, 0.2),
    (1000, 0.1),
)


MIN_PRICE = 1.01
MAX_PRICE = 1000


def as_dec(value):
    return Decimal(str(value))


def arange(start, stop, step):
    while start < stop:
        yield start
        start += step


def make_prices(min_price, cutoffs):
    prices = []
    cursor = as_dec(min_price)
    for cutoff, step in cutoffs:
        prices.extend(arange(as_dec(cursor), as_dec(cutoff), as_dec(1 / step)))
        cursor = cutoff
    prices.append(as_dec(MAX_PRICE))
    return prices


PRICES = make_prices(MIN_PRICE, CUTOFFS)


def nearest_price(price, cutoffs=CUTOFFS):
    """Returns the nearest Betfair odds value to price.

    Adapted from Anton Zemlyanov's AlgoTrader project (MIT licensed).
    https://github.com/AlgoTrader/betfair-sports-api/blob/master/lib/betfair_price.js

    :param float price: Approximate Betfair price (i.e. decimal odds value)
    :param tuple cutoffs: Optional tuple of (cutoff, step) pairs
    :returns: The nearest Befair price
    :rtype: float
    """
    if price <= MIN_PRICE:
        return MIN_PRICE
    if price > MAX_PRICE:
        return MAX_PRICE

    price = as_dec(price)
    for cutoff, step in cutoffs:
        if price < cutoff:
            break
    step = as_dec(step)
    return float((price * step).quantize(2, ROUND_HALF_UP) / step)


def ticks_difference(price_1, price_2):
    """Returns the absolute difference in terms of "ticks" (i.e. individual
    price increments) between two Betfair prices.

    :param float price_1: An exact, valid Betfair price
    :param float price_2: An exact, valid Betfair price
    :returns: The absolute value of the difference between the prices in "ticks"
    :rtype: int
    """
    price_1_index = PRICES.index(as_dec(price_1))
    price_2_index = PRICES.index(as_dec(price_2))
    return abs(price_1_index - price_2_index)


def price_ticks_away(price, n_ticks):
    """Returns an exact, valid Betfair price that is n_ticks "ticks" away from
    the given price. n_ticks may positive, negative or zero (in which case the
    same price is returned) but if there is no price n_ticks away from the
    given price then an exception will be thrown.

    :param float price: An exact, valid Betfair price
    :param float n_ticks: The number of ticks away from price the new price is
    :returns: An exact, valid Betfair price
    :rtype: float
    """
    price_index = PRICES.index(as_dec(price))
    return float(PRICES[price_index + n_ticks])
