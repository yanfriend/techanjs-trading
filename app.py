import datetime
import fnmatch
import json
import os
import random

from flask import Flask
from flask import render_template

from apis.db import Game, Strategy, GameView, MySession

BEFORE_WINDOW = 602
WINDOW = 69
AFTER_WINDOW = 87


app = Flask(__name__, static_folder='data')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/buy")
def buy():
    print 'you are in buy web service: write into db.'
    return 'OK'


@app.route("/sell")
def sell():
    print 'you are in sell web service: write into db.'
    return 'OK'


@app.route("/new_game")
def new_game():
    print 'you are in new game web service: write into db.not in real use yet.'
    # if no game record, generate a game.

    game = Game(
        symbol = 'IBM',
        chart_start = datetime.datetime(1980,1,1),
        chart_end = datetime.datetime(2016,1,1),
        game_start = datetime.datetime(1981,1,1),
    )
    strategy = Strategy()  # get fund

    # round start, current, all none.
    # create a GameView

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
    symbol, start_index, end_index = random_strategy()

    strategies = get_strategies()

    game_view = GameView(fund=fund,
                         symbol=symbol,
                         start_date_str='2010-01-01',
                         start_index=start_index,
                         end_index=end_index,
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
    chart_start_date = s1.chart_start_date.strftime("%Y-%m-%d")
    print symbols

    sym_list = symbols.split(',')
    return json.dumps({'symbols':sym_list, 'chart_start_date':chart_start_date})


def random_strategy(fix_period=False):
    # got all filenames, random select one.
    folder = './data'
    all_names = []
    for file in os.listdir(folder):
        if fnmatch.fnmatch(file, '*.csv'):
            all_names.append(file)  # ZG.csv

    print(len(all_names))

    while(True):
        a_file = random.choice(all_names)
        print(a_file)

        with open(os.path.join(folder, a_file)) as f:
            for row_count, l in enumerate(f): # row_count if rows -1
                pass

        window_len = BEFORE_WINDOW + WINDOW + AFTER_WINDOW
        if row_count < window_len:
            continue

        start_index = random.randint(0, row_count - window_len)
        end_index = start_index+window_len if fix_period else row_count-1
        return a_file.replace('.csv',''), start_index, end_index


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000, debug=True)
