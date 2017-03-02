from strategy import util
from strategy.filters.basic_filter import WindowHighFilter
from strategy.filters.basic_filter import BasicFilter
import talib


class BowingTieFilter(WindowHighFilter): # window high is better than basic filter, not to say few candidates
    name = 'Bowing Tie filter'
    note = 'three moving averages cross'

    def filterMVs(self):
        """
        1. The market should make a significant low. Longer term or ideally all-time lows are the best.
            This helps to ensure that the most amount of people are on the wrong side of the market
            when the new trend begins to emerge.
        2. Referring to Figure 3, the moving averages should converge and spread out again,
            shifting from proper downtrend order (10 SMA < 20 EMA < 30 EMA) to proper
            uptrend order (10 SMA > 20 EMA > 30 EMA). Ideally, this should happen over a period of three to four days.
            This creates the appearance of a Bowtie in the averages.
        3. The market must make a lower low and a lower high. In other words, it must make at least a one-bar pullback.
            Note, in some cases, markets that only make a lower high (vs. a lower low and a lower high) may be
            considered. This is especially true when the previous day is a wide-range bar
            and/or when the trend is turning fast.
        4.  Once qualifications for (2) have been met,go long above the high of (2).
        :return boolean
        """

        close = self.df.Close[-200:].as_matrix()  # Adj close is more accurate, factored

        sma10 = talib.SMA(close, timeperiod=10)
        ema20 = talib.EMA(close, timeperiod=20)
        ema30 = talib.EMA(close, timeperiod=30)

        up_tie = False
        down_tie = False

        for i in range(1, 7):  # 1-6, last six
            if not up_tie:
                if sma10[close.size-i] > ema20[close.size-i] > ema30[close.size-i]: # -1 is the last one
                    up_tie = True
                    continue
            else:  # in up bowing tie.
                if sma10[close.size-i] < ema20[close.size-i] < ema30[close.size-i]:
                    down_tie = True
                    break

        # import ipdb; ipdb.set_trace()
        # check value.

        return up_tie and down_tie
