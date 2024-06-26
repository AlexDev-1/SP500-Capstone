"""SQLAlchemy models for SP500app."""

from operator import index
from flask_sqlalchemy import SQLAlchemy
from sympy import true

db = SQLAlchemy()

class Stock(db.Model):
    __tablename__ = 'stock'
    
    symbol = db.Column(db.Text, primary_key=True, nullable=False, index=True)
    name = db.Column(db.Text )
    industry = db.Column(db.Text)
    sector = db.Column(db.Text)


    # Relationships
    prices = db.relationship('StockPrice', backref='prices_stock', lazy=True)
    news = db.relationship('StockNews', backref='stock_news', lazy=True)

    def to_dict(self):
        return {
            "symbol" : self.symbol
            , "name" : self.name
            , "industry" : self.industry
            , "sector" : self.sector
        }


class StockPrice(db.Model):
    __tablename__ = 'stock_price'
   
    symbol = db.Column(db.Text, db.ForeignKey('stock.symbol'), index=True, primary_key=True)
    dt = db.Column(db.Date, index = True, primary_key=True)
    open = db.Column(db.Numeric, nullable=False)
    high = db.Column(db.Numeric, nullable=False)
    low = db.Column(db.Numeric, nullable=False)
    close = db.Column(db.Numeric, nullable=False)
    volume = db.Column(db.Numeric, nullable=False)

    def to_dict(self):
        return {
            "symbol" : self.symbol
            , "dt" : self.dt
            , "open" : self.open
            , "high" : self.high
            , "low" : self.low
            , "close" : self.close
            , "volume" : self.volume
        }
    
class StockNews(db.Model):
    __tablename__ = 'stock_news'

    symbol = db.Column(db.Text, db.ForeignKey('stock.symbol'), index=True, primary_key=True)
    created = db.Column(db.DateTime, index = True, primary_key=True)
    author = db.Column(db.Text, nullable=False)
    headline = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    id = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "symbol" : self.symbol
            , "created" : self.created
            , "author" : self.author
            , "headline" : self.headline
            , "url" : self.url
            , "content" : self.content
        }


def connect_db(app):

    db.app = app
    db.init_app(app)