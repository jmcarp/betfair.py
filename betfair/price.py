# -*- coding: utf-8 -*-

from decimal import Decimal, ROUND_HALF_UP


def nearest_price(price):
    """Returns the nearest Betfair odds value to price.

    Adapted from Anton Zemlyanov's AlgoTrader project (MIT licensed).
    https://github.com/AlgoTrader/betfair-sports-api/blob/master/lib/betfair_price.js

    :param float price: Approximate Betfair price (i.e. decimal odds value)
    :returns: The nearest Betfair price
    :rtype: float
    """
    if price < 1.01:
        return 1.01

    decimal_price = Decimal(str(price))

    def to_bf_price(price, inc_recip):
        return float((price * inc_recip).quantize(2, ROUND_HALF_UP) / inc_recip)

    if price < 2:
        return to_bf_price(decimal_price, Decimal(100))
    elif price < 3:
        return to_bf_price(decimal_price, Decimal(50))
    elif price < 4:
        return to_bf_price(decimal_price, Decimal(20))
    elif price < 6:
        return to_bf_price(decimal_price, Decimal(10))
    elif price < 10:
        return to_bf_price(decimal_price, Decimal(5))
    elif price < 20:
        return to_bf_price(decimal_price, Decimal(2))
    elif price < 30:
        return to_bf_price(decimal_price, Decimal(1))
    elif price < 50:
        return to_bf_price(decimal_price, Decimal(0.5))
    elif price < 100:
        return to_bf_price(decimal_price, Decimal(0.2))
    elif price < 1000:
        return to_bf_price(decimal_price, Decimal(0.1))
    else:
        return 1000.0
