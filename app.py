import datetime
import json

from flask import Flask
from flask import render_template

from apis.rounds import Game, Strategy, GameView

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
    print 'you are in new game web service: write into db.'
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
    print 'you are in reload_or_newgame web service: write into db.'

    # passs in a different symbol, and date? to init a new game.
    game_view = GameView(fund=100000,
                         symbol='IBM')

    return json.dumps(game_view.__dict__)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000, debug=True)
