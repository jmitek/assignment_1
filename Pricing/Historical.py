from datetime import datetime
import math


class YieldCurve:
    def __init__(self):
        self.rates = []
        self.durations = []

    def load2(self, filename):
        with open(filename, 'r') as f:
            # skip to the relevant header
            f.readline()
            f.readline()
            header = [s for s in f.readline().strip().split(',') if s != '']
            self.durations = list(map(lambda x: float(x), header[1:]))
            for l in f:
                l = l.strip()
                parts = [s for s in l.split(',') if s != '']
                if len(parts) == 0:
                    continue
                date = datetime.strptime(parts[0], '%d/%m/%Y')
                yields = list(map(lambda x: float(x) / 100, parts[1:]))
                self.rates.append((date, yields))

    def load3(self, filename):
        with open(filename, 'r') as f:
            # skip to the relevant header
            f.readline()
            header = [s for s in f.readline().strip().split(',') if s != '']
            self.durations = list(map(lambda x: float(x[2:4]) + float(x[-2:]) / 12, header[1:]))
            f.readline()
            for l in f:
                l = l.strip()
                parts = [s for s in l.split(',') if s != '']
                if len(parts) == 0:
                    continue
                date = datetime.strptime(parts[0], '%d/%m/%Y')
                yields = list(map(lambda x: float(x) / 100, parts[1:]))
                self.rates.append((date, yields))

    def find_yield(self, date, duration):
        firstIndex = ([index for index, i in enumerate(self.durations) if i >= duration])[0]
        if firstIndex == len(self.durations) - 1 and duration > self.durations(firstIndex):
            raise ValueError('Duration = ', duration, ' yrs exceed the maximum in data')
        row = None
        for d, v in self.rates:
            if d < date:
                continue
            if d > date:
                raise ValueError('Date {} is out of range'.format(date))
            if d == date:
                row = v
                break
        if row is None:
            raise ValueError("Could not find yield for {}".format(date))
        if math.isclose(self.durations[firstIndex], duration):
            return row[firstIndex]
        total_d = self.durations[firstIndex] - self.durations[firstIndex - 1]
        left_weight = (self.durations[firstIndex] - duration) / total_d
        right_weight = (duration - self.durations[firstIndex - 1]) / total_d
        return left_weight * row[firstIndex - 1] + right_weight * row[firstIndex]


# yc = YieldCurve()
# yc.load2('C:\\Users\Jarek\OneDrive\Risk Management\\au_yield_curve.csv')
# print('Loaded')
# test_date = datetime.strptime('26/09/2017', '%d/%m/%Y')
# print('Yield for 3 yr on ', test_date, ' is ', yc.find_yield(test_date, 3))
# print('Yield for 3 mth on ', test_date, ' is ', yc.find_yield(test_date, 3./12))
# print('Yield for 4.5 mth on ', test_date, ' is ', yc.find_yield(test_date, 4.5/12))
# print('Yield for 5 mth on ', test_date, ' is ', yc.find_yield(test_date, 5./12))

class Spot:
    def __init__(self, currency, to_ccy=None):
        self.to_ccy = to_ccy
        self.currency = currency
        self.index_values = None

    def load(self, filename, column):
        self.index_values = []
        with open(filename, 'r') as f:
            # skip to the relevant header
            f.readline()
            f.readline()
            for l in f:
                l = l.strip()
                parts = [s for s in l.split(',') if s != '']
                if len(parts) == 0:
                    continue
                parts = l.split(',')
                date = datetime.strptime(parts[0], '%d/%m/%Y')
                value = float(parts[column])
                self.index_values.append((date, value))

    def find(self, date):
        if self.index_values is None:
            return 1.
        for d, v in self.index_values:
            if date == d:
                return v
        raise ValueError("Couldn't find {} in historical data".format(date))
