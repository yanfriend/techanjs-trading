from strategy import util
from strategy.filters.basic_filter import WindowHighFilter
from strategy.filters.basic_filter import BasicFilter
import talib
import pandas as pd
import os


class LinearRegression(BasicFilter):
    name = 'Linear Regression'
    note = 'as close as an upward line'

    selected_symbols = []


    def __init__(self, window_enddate_str):
        print 'in LR'

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
        return_list = return_list[:1000]  # all around 5000 stocks

        vol_list = []

        for tup in return_list:
            print symbol
            symbol = tup[0]
            self.df = pd.read_csv(os.path.join('./data', symbol + '.csv'), index_col='Date', parse_dates=True)
            self.df = self.df.ix[:window_enddate_str]  # cut off
            self.df = self.df[-251:]

            # import ipdb; ipdb.set_trace()
            # self.df['jDate'] = self.df.index.to_julian_date() # one way to use variant of date index
            # pd.ols(y=self.df['Adj Close'], x=self.df.jDate)

            self.df['ind'] = range(0, len(self.df))
            model = pd.ols(y=self.df['Adj Close'], x=self.df.ind)
            deviation = sum((model.resid/self.df['Adj Close'])**2)
            vol_list.append((symbol, deviation))

        vol_list.sort(key=lambda tup:tup[1])
        vol_list = vol_list[:50]  # only get first 50 stable ones

        self.selected_symbols = [tup[0] for tup in vol_list]

