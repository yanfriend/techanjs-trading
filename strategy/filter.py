import datetime
import getopt
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), '../'))


from strategy.filters.basic_filter import WindowHighFilter
from strategy.filters.landry_adx_filter import LandryAdxFilter
from strategy.filters.adx_variant_filter import AdxVariantFilter
from strategy.filters.bowing_tie import BowingTieFilter
from strategy.filters.he_filter import HEFilter

from strategy.filters.linear_regression import LinearRegression
from strategy.filters.quan_momentum import QuantitativeMomentum


from strategy import util
from apis.db import MySession, Strategy


if __name__ == "__main__":
    print 'run in whole project root foler'
    print WindowHighFilter('SH', '2010-01-01').filter() # For test, False
    print WindowHighFilter('IBM', '2010-01-01').filter() # pass True

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
    ThisFilter = QuantitativeMomentum # LinearRegression  # QuantitativeMomentum,  BowingTieFilter  # change here for different Filter Class
    qualifed_symbols = ThisFilter(date_str).selected_symbols  # for whole scan
    # qualifed_symbols = [symbol for symbol in symbols if ThisFilter(symbol, date_str).filter()]

    random_strategy = Strategy()
    random_strategy.name = ThisFilter.name
    random_strategy.note = ThisFilter.note

    random_strategy.window_end_date = window_enddate # todo, calculate to change it to start date.
    # this is window end date, but stored as chart start

    random_strategy.symbols = ','.join(qualifed_symbols)

    session.add(random_strategy)
    session.commit()
