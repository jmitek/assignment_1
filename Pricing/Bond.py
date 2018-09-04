from datetime import datetime
from Bill import CommGovBill


class Bond:
    def __init__(self, face, maturity, k, c):
        self.face = face
        self.maturity = maturity
        self.k = k  # frequency
        self.c = c  # coupon rate
        self.day_per_year = 365

    def get_coupon_dates(self, from_date):
        next_coupon = self.maturity
        month_per_coupon = 12 / self.k
        while next_coupon > from_date:
            yield next_coupon
            month = next_coupon.month - month_per_coupon
            year = next_coupon.year
            if month < 1:
                month += 12
                year -= 1
            next_coupon = datetime(year=year, month=int(month), day=next_coupon.day)

    def decompose(self, date, yield_curve):
        coupon = self.c / self.k * self.face
        for cd in self.get_coupon_dates(date):
            bill = CommGovBill(coupon, cd)
            bill.r = yield_curve.find_yield(date, bill.duration(date))
            yield bill

    def price(self, date, yield_curve):
        px = 0.
        for bill in self.decompose(date, yield_curve):
            px += bill.present_value(date)
        b = CommGovBill(self.face, self.maturity)
        b.r = yield_curve.find_yield(date, b.duration(date))
        face_pv = b.present_value(date)
        return px + face_pv
