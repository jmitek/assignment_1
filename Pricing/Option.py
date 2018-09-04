import math
from mitekj.distributions import Normal


class PricingParams:
    def __init__(self, S, r, y, v, T):
        self.S = S
        self.v = v
        self.T = T
        self.r = r
        self.y = y

    def valid(self):
        return self.S > 0 and self.v != 0 and self.T > 0


class CallOption:
    def __init__(self, K):
        self.K = K

    def payoff(self, S):
        if S < self.K:
            return 0
        return S - self.K

    def price(self, params):
        if not params.valid() or self.K <= 0:
            return 0

        term1 = math.log(params.S / self.K) + (params.r - params.y) * params.T
        term2 = params.v * params.v * params.T
        term3 = math.sqrt(term2)
        term2 = term2 / 2
        dPlus = (term1 + term2) / term3
        dMinus = (term1 - term2) / term3
        return params.S * math.exp(-params.y * params.T) * Normal.normal_c(dPlus) - self.K * math.exp(
            -params.r * params.T) * Normal.normal_c(dMinus)

    def delta(self, params):
        if not params.valid() or self.K <= 0:
            return 0
        term1 = math.log(params.S / params.K) + (params.r - params.y) * params.T
        term2 = params.v * params.v * params.T
        term3 = math.sqrt(term2)
        term2 = term2 / 2
        dPlus = (term1 + term2) / term3
        return math.exp(-params.y * params.T) * Normal.normal_c(dPlus)

    def gamma(self, params):
        if not params.valid() or self.K <= 0:
            return 0
        term1 = math.log(params.S / self.K) + (params.r - params.y) * params.T
        term2 = params.v * params.v * params.T
        term3 = math.sqrt(term2)
        term2 = term2 / 2
        dPlus = (term1 + term2) / term3
        return math.exp(-params.y * params.T) * Normal.normal_d(dPlus) / (params.S * term3)

    def theta(self, params):
        if not params.valid() or self.K <= 0:
            return 0
        term1 = math.log(params.S / self.K) + (params.r - params.y) * params.T
        term2 = params.v * params.v * params.T
        term3 = math.sqrt(term2)
        term2 = term2 / 2

        dPlus = (term1 + term2) / term3
        dMinus = (term1 - term2) / term3

        return params.y * math.exp(-params.y * params.T) * params.S * Normal.normal_c(dPlus) - \
               params.r * math.exp(-params.r * params.T) * self.K * Normal.normal_c(dMinus) - \
               math.sqrt(params.v * params.v / (4 * params.T)) * params.S * math.exp(-params.y * params.T) \
               * Normal.normal_d(dPlus)

    def vega(self, params):
        if not params.valid() or self.K <= 0:
            return 0
        term1 = math.log(params.S / params.K) + (params.r - params.y) * params.T
        term2 = params.v * params.v * params.T
        term3 = math.sqrt(term2)
        term2 = term2 / 2
        dPlus = (term1 + term2) / term3
        return params.S * math.exp(-params.y * params.T) * math.sqrt(params.T) * Normal.normal_d(dPlus)

    def rho(self, params):
        if not params.valid() or self.K <= 0:
            return 0
        term1 = math.log(params.S / self.K) + (params.r - params.y) * params.T
        term2 = params.v * params.v * params.T
        term3 = params.sqrt(term2)
        term2 = term2 / 2
        dMinus = (term1 - term2) / term3
        return params.T * self.K * math.exp(-params.r * params.T) * Normal.normal_c(dMinus)

    def rhoy(self, params):
        if not params.valid() or self.K <= 0:
            return 0

        term1 = math.log(params.S / self.K) + (params.r - params.y) * params.T
        term2 = params.v * params.v * params.T
        term3 = params.sqrt(term2)
        term2 = term2 / 2
        dMinus = (term1 - term2) / term3
        return -params.T * self.K * math.exp(-params.r * params.T) * Normal.normal_c(dMinus)

    def calculate(self, params, func):
        if not params.valid() or self.K <= 0:
            return 0
        term1 = math.log(params.S / self.K) + (params.r - params.y) * params.T
        term2 = params.v * params.v * params.T
        term3 = params.sqrt(term2)
        term2 = term2 / 2
        return func(term1, term2, term3)

    # sensitivity to strike
    def dVdK(self, params):
        def deriv(term1, term2, term3):
            d_minus = (term1 - term2) / term3
            return -math.exp(-params.r * params.T) * Normal.normal_c(d_minus)

        return self.calculate(params, deriv)

    def d2Vd2K(self, params):
        def second_deriv(term1, term2, term3):
            d_minus = (term1 - term2) / term3
            return -math.exp(-params.r * params.T) * Normal.normal_d(d_minus) / (term3 * self.K)

        return self.calculate(params, second_deriv)

    # sensitivity of delta of volatility, dD/dv
    def dDdv(self, params):
        def func(term1, term2, term3):
            d_plus = (term1 + term2) / term3
            d_minus = (term1 - term2) / term3
            return -d_minus * math.exp(-params.y * params.T) * Normal.normal_d(d_plus) / params.v

        return self.calculate(params, func)

    # sensitivity of delta to risk-free rate, dD/dr
    def dDdr(self, params):
        def func(term1, term2, term3):
            d_plus = (term1 + term2) / term3
            return -math.sqrt(params.T) * math.exp(-params.y * params.T) * Normal.normal_d(d_plus) / params.v

        return self.calculate(params, func)
