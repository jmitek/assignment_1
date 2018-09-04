import math


class CommGovBill:
    def __init__(self, F, maturity, r=None):
        self.maturity = maturity
        self.F = F
        self.r = r  # rate 1% = 1.0
        self.days_per_year = 365

    def duration(self, date):
        return (self.maturity - date).days / self.days_per_year

    def present_value(self, date):
        t = self.duration(date)
        return self.F * math.exp(-self.r * t)
