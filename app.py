import csv
import datetime
import fnmatch
import json
import os
import random
from os import listdir
from os.path import isfile, join

from flask import Flask, request
from flask import render_template

from strategy import util
from apis.db import Game, Strategy, GameView, MySession, Round

from strategy.defs import BEFORE_WINDOW, WINDOW, AFTER_WINDOW
from strategy.filter import WindowHighFilter

app = Flask(__name__, static_folder='data')


@app.route("/")
def index():
    start_file = request.args.get('start_file')

    if start_file is None:
        start_file='index.html'
    return render_template(start_file)


@app.route("/buy")
def buy():
    print 'you are in buy web service: write into db.'
    return 'OK'


@app.route("/sell/<row_data>")
def sell(row_data):
    print 'in sell: '+row_data # now get the data ok, log to db.

    row_data = json.loads(row_data)
    rounds = []

    for a_row in row_data:
        round = Round(
            symbol=a_row.get('symbol',''),

            entry_date = datetime.datetime.strptime(a_row['entry date'][0:10],'%Y-%m-%d'),
            exit_date=datetime.datetime.strptime(a_row['exit date'][0:10], '%Y-%m-%d'),
            holding_days = a_row['Holding Days'],

            # current_date = Column(DateTime)  # reserved

            entry_price = a_row['Entry Price'],
            exit_price = a_row['Exit Price'],

            buy_sell = a_row['buysell'][0:1],
            # position = Column(Integer)  # reserved ?

            # start_fund = Column(Float)
            # end_fund = Column(Float)

            max_drawdown = a_row['Max Drawdown%'],
            max_profit = a_row['Max profit%'],
            profit_percentage = a_row['Gain%'],

            # game_id = Column(Integer, ForeignKey('game.id'))
        )
        rounds.append(round)

    create_round(rounds)
    return 'OK'

@app.route("/new_game")
def new_game():
    print 'you are in new game web service: write into db.not in real use yet.'
    return 'OK'


@app.route("/reload_or_newgame")
def reload_or_newgame():
    """
    reload or new game depending on last status.
    :return:
    """
    print 'you are in reload_or_newgame web service: write into db.'

    # get last fund,
    # generate symbol according to strategy
    # write status to db.

    # if no last situation, return new_game()

    fund = 100000
    symbol, start_date_str, game_id = random_strategy()

    strategies = get_strategies() # only for name to populate select options

    game_view = GameView(fund=fund,
                         symbol=symbol,
                         game_id=game_id,
                         start_date_str=start_date_str, # '2010-01-01',
                         strategies=strategies,
                         )
    print json.dumps(game_view.__dict__)
    return json.dumps(game_view.__dict__)


@app.route("/get_strategies")
def get_strategies():
    session = MySession.create()

    strategies = session.query(Strategy.id, Strategy.name) \
        .filter(Strategy.removed_at.is_(None)) \
        .order_by(Strategy.created.desc(), Strategy.id.desc()) \
        .all()

    return strategies # array of tuples


@app.route('/get_game_candidates/<strategy_id>')  # should have a strategy parameter, use id is better!!!
def get_game_candidates(strategy_id):
    session = MySession.create()

    s1 = session.query(Strategy).get(strategy_id)
    symbols = s1.symbols
    window_end_date = s1.window_end_date.strftime("%Y-%m-%d")
    print symbols

    sym_list = symbols.split(',')
    return json.dumps({'symbols':sym_list, 'window_end_date':window_end_date})


@app.route('/list_all_symbols') # add date, strategy, i.e. filter ?
def list_all_symbols():
    allsymbols = util.list_all_symbols()
    return json.dumps(allsymbols);


def create_game(symbol, window_end_date):
    session = MySession.create()
    game = Game(symbol=symbol, window_end_date=window_end_date)
    session.add(game)
    session.commit()
    return game.id

def create_round(rounds):
    if len(rounds)==0:
        return
    session = MySession.create()
    session.add_all(rounds)
    session.commit()

def random_strategy(fix_period=False): # not a random as added new high judge.
    # got all filenames, random select one.
    folder = './data'
    all_names = []
    for file in os.listdir(folder):
        if fnmatch.fnmatch(file, '*.csv'):
            all_names.append(file)  # ZG.csv

    print(len(all_names))

    while (True):
        a_file = random.choice(all_names)
        print(a_file)

        with open(os.path.join(folder, a_file)) as f:
            my_list = [row for row in csv.DictReader(f)]

        row_count = len(my_list) # - 1;
        window_len = BEFORE_WINDOW + WINDOW + AFTER_WINDOW
        if row_count < window_len:
            continue

        start_index = random.randint(0, row_count - window_len+1)  # after start_index, there must be enough bars to play
        start_date_str = my_list[start_index]['Date']
        end_date_str = my_list[start_index + (BEFORE_WINDOW + WINDOW)]['Date']  # cut to show window

        if not WindowHighFilter(a_file[:-4], end_date_str).filter():
            continue

        symbol = a_file.replace('.csv','')
        game_id = create_game(symbol=symbol, window_end_date=datetime.datetime.strptime(end_date_str, "%Y-%m-%d"))
        return symbol, start_date_str, game_id

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000, debug=True)
