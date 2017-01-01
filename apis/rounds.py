from sqlalchemy import create_engine, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Strategy(Base):
    __tablename__ = 'strategy'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=func.now())

    user_name = Column(String(16), default='baifriend')
    fund = Column(Float, default=100000)  # 100k initial funding

    note = Column(Text)
    symbols = Column(Text)


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


if __name__ == "__main__":
    engine = create_engine('mysql://root:@localhost:3306/chartgame', echo=True)

    Session = sessionmaker()
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)
    session = Session()

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
