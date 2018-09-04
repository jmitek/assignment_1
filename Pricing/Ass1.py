import math

import matplotlib as matplotlib
import numpy as np
from datetime import datetime
from scipy.stats import norm
import matplotlib.pyplot as pl

import Portfolio
from Bond import Bond
from Cash import CashAssets
from Historical import YieldCurve, Spot


def calculate_bond_returns(days, historical_date, valuation_date, yc, bonds):
    returns = [Portfolio.get_bond_returns(b, historical_date, valuation_date, days, yc) for b in bonds]
    mtm = [b.price(valuation_date, yc) for b in bonds]
    return returns, mtm


def diversified_VaR(returns, prices, mtm, days, significance):
    cov = np.cov(returns, ddof=0)
    print(cov)
    w = np.divide(mtm, np.sum(mtm))
    print('Weights are', w)
    print('Mark-to-market=', np.sum(mtm))
    print('Correlations')
    print(np.corrcoef(returns))
    print('\n\n***** Analytic *******\n\n')
    # we know cov matrix is symmetric, validate it's positive definite
    np.linalg.cholesky(cov)  # throws exception if it can't be factorised
    port_volatility = np.sqrt(np.dot(w, cov).dot(w))
    print('Portfolio {}-day variance = {}'.format(days, port_volatility))
    quantile = norm.ppf(1 - significance / 100.)
    print('Quantile = {}'.format(quantile))
    port_VaR = math.fabs(port_volatility * quantile) * np.sum(mtm)
    print('{}-Day diversified VaR={} or {}%'.format(days, port_VaR, port_VaR / np.sum(mtm) * 100.))

    print('\n\n***** Historical *******\n\n')
    pnl = np.sum(prices, axis=0)[::days]  # take every n-days
    pnl_diffs = [y - x for x, y in zip(pnl, pnl[1:])]  # compare neighbouring elements
    sorted_pnl_diffs = sorted(pnl_diffs)
    # round conservatively to the next index, if the level falls between to observations
    # then strictly, the loss will not exceed that larger number
    item = math.floor(len(sorted_pnl_diffs) * (100 - significance) / 100.)
    print('{} percentile corresponds to {}-th return'.format(significance, item))
    print('Historical VaR is', math.fabs(sorted_pnl_diffs[item]))

# yc = YieldCurve()
# yc.load2('C:\\Users\Jarek\OneDrive\Risk Management\\au_yield_curve.csv')
# valuation_date = datetime(year=2017, month=12, day=21)
# historical_date = datetime(year=2016, month=12, day=21)
# face = 2E6
# maturity = datetime(year=2018, month=12, day=21)
# bond1 = Bond(face, maturity, 2, 0.04)
# bond2 = Bond(face, datetime(year=2019, month=12, day=21), 2, 0.02)
# calculate_bond_VaR(10, 90., historical_date, valuation_date, yc, [bond1, bond2])

# def portfolio_var(days):
#     yc = YieldCurve()
#     yc.load2('C:\\Users\Jarek\OneDrive\Risk Management\\au_yield_curve.csv')
#     valuation_date = datetime(year=2017, month=12, day=21)
#     historical_date = datetime(year=2016, month=12, day=21)
#     face = 2E6
#     maturity = datetime(year=2018, month=12, day=21)
#     bond1 = Bond(face, maturity, 2, 0.04)
#     price1 = bond1.price(valuation_date, yc)
#     returns_bond1 = Portfolio.get_bond_returns(bond1, historical_date, valuation_date, days, yield_curve=yc)
#     bond2 = Bond(face, datetime(year=2019, month=12, day=21), 2, 0.02)
#
#
#     price2 = bond2.price(valuation_date, yc)
#     returns_bond2 = Portfolio.get_bond_returns(bond2, historical_date, valuation_date, days, yield_curve=yc)
#     significance = 95.
#     quantile = norm.ppf(1 - significance / 100.)
#     # entire portfolio
#     asx200 = Spot('AUD')
#     asx200.load('C:\\Users\\Jarek\OneDrive\Risk Management\indicies_fx.csv', 1)
#     spus = Spot('USD')
#     spus.load('C:\\Users\\Jarek\OneDrive\Risk Management\indicies_fx.csv', 2)
#     audusd = Spot('AUD', 'USD')
#     audusd.load('C:\\Users\\Jarek\OneDrive\Risk Management\indicies_fx.csv', 3)
#     usdHoldings = CashAssets(4E6, Spot('USD'))
#     asxHoldings = CashAssets(1000, asx200)
#     spusHoldings = CashAssets(-2500, spus)
#     returns_1day_spus = Portfolio.get_cash_returns(spusHoldings, historical_date, valuation_date, days, 'AUD', audusd)
#     returns_1day_asx = Portfolio.get_cash_returns(asxHoldings, historical_date, valuation_date, days)
#     returns_1day_usd = Portfolio.get_cash_returns(usdHoldings, historical_date, valuation_date, days, 'AUD', audusd)
#     print('Bond1={}, Bond2={}, SPUS={}, ASX={}, USD={}'.format(len(returns_bond1), len(returns_bond2),
#                                                                len(returns_1day_spus), len(returns_1day_asx),
#                                                                len(returns_1day_usd)))
#     covPortfolio = np.cov([returns_bond1, returns_bond2, returns_1day_spus, returns_1day_asx, returns_1day_usd])
#     # we know it's symmetric for sure, but now
#     # make sure it is positive definite
#     np.linalg.cholesky(covPortfolio)
#     print('Portfolio {}-day cov is'.format(days))
#     print(covPortfolio)
#     x = np.array([price1, price2, spusHoldings.price(valuation_date, 'AUD', audusd), asxHoldings.price(valuation_date),
#                   usdHoldings.price(valuation_date, 'AUD', audusd)])
#     print('Portfolio market value', np.sum(x))
#     print(x)
#     w = np.divide(x, np.sum(x))
#     print(w)
#     print('Sums to ', np.sum(w))
#     portfolio_volatility = np.sqrt(np.dot(np.dot(w, covPortfolio), w))
#     print('Portfolio volatility is {}'.format(portfolio_volatility))
#     portVar = math.fabs(quantile * portfolio_volatility) * np.sum(x)
#     print("Portfolio {}-day VaR at alpha={} is {} or {}%".format(days, quantile, portVar, portVar / np.sum(x)))


# print('---------------------------')
# print('------1 Day VaR -----------')
# print('---------------------------')
# portfolio_var(1)
# print('\n\n\n---------------------------')
# print('------10 Day VaR ----------')
# print('---------------------------')
# portfolio_var(10)

def portfolio_1():
    yc = YieldCurve()
    yc.load3(r'C:\Users\Jarek\OneDrive\Risk Management\assignment\aus_zero_curve.csv')
    bonds = [
        Bond(6e6, datetime(year=2019, month=3, day=15), 2, 0.0525),
        Bond(8e6, datetime(year=2020, month=4, day=15), 2, 0.045),
        Bond(10e6, datetime(year=2021, month=5, day=15), 2, 0.0575),
        Bond(8e6, datetime(year=2022, month=7, day=15), 2, 0.0575),
        Bond(10e6, datetime(year=2023, month=4, day=21), 2, 0.055)]
    historical_date = datetime(year=2017, month=8, day=6)
    valuation_date = datetime(year=2018, month=8, day=6)
    returns, mtm = calculate_bond_returns(1, historical_date, valuation_date, yc, bonds)
    prices = [Portfolio.get_bond_prices(b, historical_date, valuation_date, yc) for b in bonds]
    diversified_VaR(returns, prices, mtm, 1, 90.)
    returns, mtm = calculate_bond_returns(10, historical_date, valuation_date, yc, bonds)
    diversified_VaR(returns, prices, mtm, 10, 90.)


portfolio_1()

def portfolio_2():
    print('Portfolio 2')
    


# print('-----------------------------')
# print('------Portfolio 1 -----------')
# print('-----------------------------')
# portfolio_1()

# do Jeff's examples
ratesFtse = []
ratesAssd = []
ratesBarc = []


def load_uk():
    with open(r'C:\Users\Jarek\OneDrive\Risk Management\BASICS_V2\Basics\Excel\JeffsVaRexamples.csv', 'r') as f:
            # skip to the relevant header
            f.readline()
            f.readline()
            for l in f:
                l = l.strip()
                parts = [s for s in l.split(',') if s != '']
                if len(parts) == 0:
                    continue
                date = datetime.strptime(parts[0], '%d/%m/%Y')
                if date < datetime(year=1997, month=1, day=17):
                    continue
                if date > datetime(year=1998, month=1, day=1):
                    break
                ratesAssd.append(float(parts[1]))
                ratesBarc.append(float(parts[2]))
                ratesFtse.append(float(parts[3]))


# load_uk()
# # print('Var of Assd is', np.var(ratesAssd))
#
# returns_assd = Portfolio.get_returns(ratesAssd)
# returns_barc = Portfolio.get_returns(ratesBarc)
# returns_ftse = Portfolio.get_returns(ratesFtse)
# print('Corr(ASSD, BARC) =,', np.corrcoef(returns_assd, returns_barc))
# print('Corr(ASSD, FTSE) =,', np.corrcoef(returns_assd, returns_ftse))
# print('Corr(BARC, FTSE) =,', np.corrcoef(returns_barc, returns_ftse))
# print('Var assd =', np.var(returns_assd), 'VS mine =', Portfolio.varfiance(returns_assd))
# print('Var barc =', np.var(returns_barc))
# print('Var ftse =', np.var(returns_ftse))
# diversified_VaR([returns_assd, returns_barc, returns_ftse], [3550000, 8090000, 5224100], 1, 90.)

