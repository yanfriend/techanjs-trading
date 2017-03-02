from strategy import util
from strategy.filters.basic_filter import WindowHighFilter
from strategy.filters.basic_filter import BasicFilter
import talib
import pandas as pd
import os


class QuantitativeMomentum(BasicFilter):
    name = 'Quantitative Momentum'
    note = 'high return, low volatility'

    selected_symbols = []


    def __init__(self, window_enddate_str):
        print 'in QM'

        symbols = util.list_all_symbols()

        basic_symbols = []
        for symbol in symbols:
            if BasicFilter(symbol, window_enddate_str).filter():
                basic_symbols.append(symbol)

        # calculate return to its 252 days, and store for comparison
        return_list = []
        for symbol in basic_symbols:
            self.df = pd.read_csv(os.path.join('./data', symbol + '.csv'), index_col='Date', parse_dates=True)
            self.df = self.df.ix[:window_enddate_str]  # cut off
            try:
                ret = self.df.ix[-1]['Adj Close'] / self.df.ix[-252]['Adj Close']
            except IndexError:
                continue
            return_list.append((symbol, ret))

        return_list.sort(key=lambda tup:tup[1], reverse=True)
        return_list = return_list[:100]  # top 100 only.

        vol_list = []
        for tup in return_list:
            print symbol
            symbol = tup[0]
            self.df = pd.read_csv(os.path.join('./data', symbol + '.csv'), index_col='Date', parse_dates=True)
            self.df = self.df.ix[:window_enddate_str]  # cut off
            self.df = self.df[-251:]
            up_day = sum(self.df.Close > self.df.Open)
            down_day = sum(self.df.Close < self.df.Open)
            volatility = (up_day - down_day)/len(self.df.Close)
            vol_list.append((symbol, volatility))

        vol_list.sort(key=lambda tup:tup[1], reverse=True)
        vol_list = vol_list[:50]  # only get first 50 among 100

        self.selected_symbols = [tup[0] for tup in vol_list]

