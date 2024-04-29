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


class StockPrice(db.Model):
    __tablename__ = 'stock_price'
   
    symbol = db.Column(db.Text, db.ForeignKey('stock.symbol'), index=True, primary_key=True)
    dt = db.Column(db.Date, index = True, primary_key=True)
    open = db.Column(db.Numeric, nullable=False)
    high = db.Column(db.Numeric, nullable=False)
    low = db.Column(db.Numeric, nullable=False)
    close = db.Column(db.Numeric, nullable=False)
    volume = db.Column(db.Numeric, nullable=False)


def connect_db(app):

    db.app = app
    db.init_app(app)