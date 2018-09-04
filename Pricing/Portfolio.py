import math
import numpy as np
from datetime import timedelta


def get_bond_prices(bond, from_date, to_date, yield_curve):
    prices = []
    begin = from_date
    while begin <= to_date:
        if begin.weekday() in (5, 6):
            begin += timedelta(days=1)
            continue
        price = bond.price(begin, yield_curve)
        prices.append(price)
        begin += timedelta(days=1)
    return prices


def get_bond_returns(bond, from_date, to_date, bus_days, yield_curve):
    begin = from_date
    returns = []
    while begin <= to_date:
        if begin.weekday() in (5, 6):
            begin += timedelta(days=1)
            continue
        days_to_skip = bus_days
        until = begin
        while days_to_skip > 0:
            until = until + timedelta(days=1)
            if until.weekday() in (5, 6):
                continue
            days_to_skip -= 1
        if until > to_date:
            break
        s_price = bond.price(begin, yield_curve)
        e_price = bond.price(until, yield_curve)
        ret = math.log(e_price / s_price)
        returns.append(ret)
        begin = until
    print('There are', len(returns), 'samples when calculating var')
    return returns


def get_cash_returns(asset, from_date, to_date, bus_days, to_ccy=None, fx=None):
    assert((to_ccy is None and fx is None) or (to_ccy is not None and fx is not None))
    begin = from_date
    returns = []
    while begin <= to_date:
        if begin.weekday() in (5, 6):
            begin += timedelta(days=1)
            continue
        days_to_skip = bus_days
        until = begin
        while days_to_skip > 0:
            until = until + timedelta(days=1)
            if until.weekday() in (5, 6):
                continue
            days_to_skip -= 1
        if until > to_date:
            break
        s_price = asset.price(begin, to_ccy, fx)
        e_price = asset.price(until, to_ccy, fx)
        ret = math.log(e_price / s_price)
        returns.append(ret)
        begin = until
    print('There are', len(returns), 'samples when calculating returns')
    return returns


def get_returns(prices, days):
    returns = []
    i = 0
    while i < len(prices) - days:
        # returns.append(math.log(prices[i+1]/prices[i]))
        returns.append(prices[i+days]/prices[i] - 1)
        i += days
    return returns


def varfiance(returns):
    sum = np.sum(returns)
    mean = sum / len(returns)
    var = 0.
    for r in returns:
        var += math.pow(r - mean, 2)
    return var / (len(returns) - 1)

