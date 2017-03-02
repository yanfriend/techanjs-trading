import datetime
import getopt
import os
import sys

import pandas as pd
import numpy as np

from strategy.defs import BEFORE_WINDOW, WINDOW, AFTER_WINDOW, NEW_HIGH_WINDOW, MIN_PRICE, VOLUME_PERIOD, MIN_VOLUME

from strategy import util
from apis.db import MySession, Strategy


class BasicFilter(object):
    name = 'Basic strategy'
    note = 'basic price and vol only'

    def __init__(self, symbol, window_enddate_str):
        # self.date = datetime.datetime.strptime(datestr, '%Y-%m-%d')
        self.symbol = symbol

        self.df = pd.read_csv(os.path.join('./data', symbol + '.csv'), index_col='Date', parse_dates=True)
        self.df = self.df.ix[:window_enddate_str]  # cut off

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

    def filter(self, batch=False):
        if len(self.df) <= WINDOW:
            return False
        print self.symbol, # print to monitor progress

        ret = True
        for method in dir(self):
            if callable(getattr(self, method)) and method.startswith('filter') and len(method)>len('filter'):
                ret = ret and getattr(self, method)()

        if not ret:
            return False
        else:
            return ret


# todo, to another file
class WindowHighFilter(BasicFilter):
    name = 'Window high strategy'
    note = 'window high'

    def filter_window_high(self):
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

    # def filter(self, batch=False):
    #     if len(self.df) <= WINDOW:
    #         return False
    #     print self.symbol, # print to monitor progress
    #
    #     ret = True
    #     for method in dir(self):
    #         if callable(getattr(self, method)) and method.startswith('filter') and len(method)>len('filter'):
    #             ret = ret and getattr(self, method)()
    #
    #     if not ret:
    #         return False
    #     else:
    #         return ret
