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


class BasicFilter(object):
    name = 'Basic strategy'
    note = 'window high'

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


class HEFilter(BasicFilter):
    def filter(self):
        ret = super(HEFilter, self).filter()
        if not ret:
            return False

        ret = self.second_filter_cycle()  # not use it in online chat show, its too slow.
        if ret:
            reversed_index = [a[0] for a in ret]
            return self.second_filter_dry_up_volume(reversed_index)
        return ret

    def second_filter_cycle(self):
        """
        it has 5-6 cycle in half a year, each up 20%
        Focus on stocks that regularly exhibit 6 to 8 day cycles of 20% price movement
        :return:
        """
        index = 1
        cycle = 0
        ret = []

        while index < 128:  # half an year.
            if index >= len(self.df):
                print 'too short in {}'.format(self.symbol)
                return False
            highest = self.df.ix[-index]['High'].max()
            lowest = self.df.ix[-index-8:-index]['Low'].min()  # not include the last one.
            if highest/lowest > 1.2:  # 20%+ up
                cycle += 1
                low_date_index = self.df.ix[-index-8:-index]['Low'].idxmin()
                low_index = self.df.index.get_loc(low_date_index)  # number index, location actually

                index = len(self.df) - low_index  # move to the lowest bar.
                ret.append((index, low_date_index))
            else:
                index += 1 # move to next one
        if cycle >=5:
            # import ipdb; ipdb.set_trace()
            return ret
        else:
            return False

    def second_filter_dry_up_volume(self, reversed_index):
        """
        for each index, calculate five day low volume, include the index day.
        get average volume.
        if last volume < 1.5 * avg volume, then return True as in dry volume state; otherwise False.
        :param reversed_index:
        :return:
        """
        vol = 0
        count = 0
        for ind in reversed_index:
            vol += self.df.ix[-ind-4: -ind+1]['Volume'].min()  # [:-1] always not include the last one, but cant use 0
            count += 1
        avg_vol = vol*1.0/count
        return self.df.ix[-1]['Volume'] < 1.5 * avg_vol


class LandryFilter(BasicFilter):
    name = 'David Landry filter'
    note = 'adx, dmi etc'
    def filterAdx(self):
        """
        filter by adx and dmi; others, HV
        :return: boolean
        """

        close = self.df.Close[-28:].as_matrix()  # Adj close is more accurate, factored
        high = self.df.High[-28:].as_matrix()
        low = self.df.Low[-28:].as_matrix()

        adx = talib.ADX(high, low, close, 14) # high, low, close, timeperiod=14

        last_adx = adx[-1]

        if last_adx < 25:
            return False

        last_dm_pluse = talib.PLUS_DM(high, low)[-1]
        last_dm_minus = talib.MINUS_DM(high, low)[-1]

        if last_dm_pluse < last_dm_minus:
            return False

        """
        50 days hv>40%
        6 days HV/100 days HV < 50%, it tend to have explosive movement.
        doubt this will filter recent plat stocks
        """

        hv50 = util.historical_volatility(self.df.Close, 50)
        if hv50 < 0.4:
            return False

        hv6 = util.historical_volatility(self.df.Close, 6)
        hv100 = util.historical_volatility(self.df.Close, 100)
        if hv6/hv100 > 0.5:
            return False

        return True


if __name__ == "__main__":
    print 'run in whole project root foler'
    print BasicFilter('SH', '2010-01-01').filter() # For test, False
    print BasicFilter('IBM', '2010-01-01').filter() # pass True

    argv = sys.argv[1:]
    date_str = None

    try:
        opts, args = getopt.getopt(argv, 'hd:', ['date='])
    except getopt.GetoptError:
        print 'python {} -d <date>'.format(sys.argv[0])
        sys.exit(1)

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

    symbols = util.list_all_symbols()
    qualifed_symbols = [symbol for symbol in symbols if LandryFilter(symbol, date_str).filter()]

    random_strategy = Strategy()
    random_strategy.name = LandryFilter.name
    random_strategy.note = LandryFilter.note

    random_strategy.window_end_date = window_enddate # todo, calculate to change it to start date.
    # this is window end date, but stored as chart start

    random_strategy.symbols = ','.join(qualifed_symbols)

    session.add(random_strategy)
    session.commit()
