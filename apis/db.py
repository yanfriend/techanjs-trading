import datetime
from sqlalchemy import create_engine, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)

    username = Column(Text, default='baifriend')
    fund = Column(Float, default=100000)


class Strategy(Base):
    __tablename__ = 'strategy'

    id = Column(Integer, primary_key=True)

    name = Column(Text)  # with created, as select index
    created = Column(DateTime, default=func.now())
    removed_at = Column(DateTime)

    note = Column(Text)  # secret comment
    symbols = Column(Text)  # use csv format

    window_end_date = Column(DateTime)

    chart_end_date = Column(DateTime) # the two reserved
    game_start_date = Column(DateTime)


class Game(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=func.now())

    symbol = Column(String(10))

    chart_start = Column(DateTime)
    chart_end = Column(DateTime)
    game_start = Column(DateTime)  # time in chart.

    player_id = Column(Integer, ForeignKey('strategy.id'))


class Round(Base):
    __tablename__ = 'round'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=func.now())
    symbol = Column(String(10))  # this is duplicates

    round_start = Column(DateTime)
    round_current = Column(DateTime)

    buy_sell = Column(String(1))
    entry_price = Column(Float)
    exit_price = Column(Float)
    position = Column(Integer)

    max_drawdown = Column(Float)
    profit_percentage = Column(Float)

    game_id = Column(Integer, ForeignKey('game.id'))
    # Use cascade='delete,all' to propagate the deletion of a Game onto its Rounds
    game = relationship(
        Game,
        backref=backref('rounds',
                        uselist=True,
                        cascade='delete,all'))
    # Game accesses rounds use list


class GameView(object):
    def __init__(self, **kwargs):
        self.fund = kwargs.get('fund', 100000)
        self.symbol = kwargs.get('symbol', 'IBM')
        self.start_index = kwargs.get('start_index', 1000)
        self.end_index = kwargs.get('end_index', 1000000)
        self.strategies = kwargs.get('strategies', [])
        self.start_date_str = kwargs.get('start_date_str', '2010-01-01')


class MySession:
    my_session = None

    @classmethod
    def create(self):
        if self.my_session is not None:
            return self.my_session

        engine = create_engine('mysql://root:@localhost:3306/chartgame', echo=True)
        Session = sessionmaker()
        Session.configure(bind=engine)
        Base.metadata.create_all(engine)
        self.my_session = Session()
        return self.my_session


if __name__ == "__main__":
    session = MySession.create()

    random_strategy = Strategy()
    random_strategy.name = 'big index'
    random_strategy.note = 'test'
    random_strategy.symbols = 'IBM,SPY,DIA'
    random_strategy.window_end_date = datetime.datetime(1985,1,1) # this will change to random

    session.add(random_strategy)
    session.commit()


    ibm = Game(symbol='IBM')
    round1 = Round(symbol='IBM')
    round1.game = ibm
    session.add(round1)
    session.commit()

    round = session.query(Game) \
        .filter(Game.symbol == 'IBM') \
        .order_by(Game.id.desc()) \
        .first()

    print ibm.rounds
    print ibm.rounds[0].symbol

    # session.delete(it)
    # session.commit()
