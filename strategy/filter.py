import datetime
import getopt
import os
import sys
import talib

import pandas as pd
import numpy as np

from defs import BEFORE_WINDOW, WINDOW, AFTER_WINDOW, NEW_HIGH_WINDOW, MIN_PRICE, VOLUME_PERIOD, MIN_VOLUME

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from strategy import util
from apis.db import MySession, Strategy


class Filter(object):
    def __init__(self, symbol, window_enddate_str):
        # self.date = datetime.datetime.strptime(datestr, '%Y-%m-%d')
        self.symbol = symbol

        self.df = pd.read_csv(os.path.join('./data', symbol + '.csv'), index_col='Date', parse_dates=True)
        self.df = self.df.ix[:window_enddate_str]  # cut off

    def filter(self):
        if len(self.df) <= WINDOW:
            return False
        print self.symbol, # print to monitor progress
        return self.filter_price() \
               and self.filter_volume() \
               and self.high_in_window()

    def filter_price(self):
        """
        price must higher than $4.
        """
        return self.df.ix[-1].Close >= 4

    def filter_volume(self):
        """
        65 day vol larger than 100k
        :return:
        """
        tmp_pd = self.df.ix[-VOLUME_PERIOD:].Volume
        last_vol_avg = tmp_pd.rolling(window=VOLUME_PERIOD).mean()[-1]
        return last_vol_avg > MIN_VOLUME

    def high_in_window(self):
        """
        for high in window, for previous close, check if the close is highest in window size days.
        """
        # leave it for panda expression
        # for i in range(15): # recent 15 close, is higher than recent 65 close
        #     current_price = self.df.ix[-i-1].Close
        #     if len(self.df[-65:][self.df['Close'] >= current_price])<=1:
        #         return True
        max_recent_close = self.df.ix[-NEW_HIGH_WINDOW:]['Adj Close'].max()
        max_window_close = self.df.ix[-WINDOW:]['Adj Close'].max()

        return max_recent_close >= max_window_close




if __name__ == "__main__":
    print 'run in whole project root foler'
    print Filter('SH', '2010-01-01').filter() # For test, False
    print Filter('IBM','2010-01-01').filter() # pass True

    argv = sys.argv[1:]
    date_str = None

    try:
        opts, args = getopt.getopt(argv, 'hd:', ['date='])
    except getopt.GetoptError:
        print 'python {} -d <date>'.format(sys.argv[0])
        sys.exit(1)

    import ipdb; ipdb.set_trace()

    for opt, arg in opts:
        if opt == '-h':
            print 'python {} -d <date>'.format(sys.argv[0])
            sys.exit(2)
        elif opt in ('-d', '--date'):
            date_str = arg

    if date_str is None:
        print 'python {} -d "%Y-%m-%d"'
        sys.exit(3)
    else:
        window_enddate = datetime.datetime.strptime(date_str, "%Y-%m-%d")

    session = MySession.create()

    random_strategy = Strategy()
    random_strategy.name = 'days high'
    random_strategy.note = '69 days high'

    random_strategy.window_end_date = window_enddate # todo, calculate to change it to start date.
    # this is window end date, but stored as chart start

    symbols = util.list_all_symbols()
    qualifed_symbols = [symbol for symbol in symbols if Filter(symbol, date_str).filter()]

    import ipdb; ipdb.set_trace()
    random_strategy.symbols = ','.join(qualifed_symbols)

    session.add(random_strategy)
    session.commit()
