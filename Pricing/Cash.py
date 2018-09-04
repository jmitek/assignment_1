class CashAssets:
    def __init__(self, amount, historical=None):
        self.amount = amount
        self.historical = historical

    def price(self, date, to_ccy=None, fx_spot=None):
        historical_price = self.amount
        if self.historical is not None:
            historical_price *= self.historical.find(date)
        if to_ccy is None or to_ccy == self.historical.currency:
            return historical_price
        spot_fx = fx_spot.find(date)
        # work out which way to convert
        if fx_spot.currency == self.historical.currency and fx_spot.to_ccy == to_ccy:
            return spot_fx * historical_price
        elif fx_spot.currency == to_ccy and fx_spot.to_ccy == self.historical.currency:
            return historical_price / spot_fx
        raise ValueError("No way to convert from {} to {}".format(self.historical.currency, to_ccy))
