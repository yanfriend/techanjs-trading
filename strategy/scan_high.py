import datetime
import getopt
import os

import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from apis.db import MySession, Strategy



if __name__ == "__main__":

    argv = sys.argv[1:]
    date_str = None

    try:
        opts, args = getopt.getopt(argv, 'hs:n:', ['date='])
    except getopt.GetoptError:
        print 'python {} -d <date>'.format(sys.argv[0])
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'python {} -d <date>'.format(sys.argv[0])
            sys.exit()
        elif opt in ('-d', '--date'):
            date_str = int(arg)

    if date_str is None:
        chart_start_date = datetime.datetime(1985,1,1)  # todo, this will change to random
    else:
        chart_start_date = datetime.strptime(date_str, "%Y-%m-%d")

    session = MySession.create()

    random_strategy = Strategy()
    random_strategy.name = 'days high'
    random_strategy.note = '69 days high'

    random_strategy.chart_start_date = datetime.datetime(1985,1,1)  # this will change to random

    symbols = ''
    # todo, for each file, get to the date, in previous 15 days, whether one of them has 69 days high. add it if yes.



    random_strategy.symbols = symbols

    session.add(random_strategy)
    session.commit()
