from strategy import util
from strategy.filters.basic_filter import BasicFilter
import talib


class QuantitativeMomentum(BasicFilter):
    name = 'Quantitative Momentum'
    note = 'high return, low volatility'

    def filterMomentum(self):
        """
        :return: boolean
        """

        #todo, write new below


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
