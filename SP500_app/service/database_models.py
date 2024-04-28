"""SQLAlchemy models for SP500app."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Stock(db.Model):
    __tablename__ = 'stock'
    
    symbol = db.Column(db.Text, primary_key=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    industry = db.Column(db.Text, nullable=False)


    # Relationships
    mentions = db.relationship('Mention', backref='stock', lazy=True)
    prices = db.relationship('StockPrice', backref='stock', lazy=True)



class Mention(db.Model):
    __tablename__ = 'mention'
    
    symbol = db.Column(db.Integer, db.ForeignKey('stock.symbol'), primary_key=True)
    dt = db.Column(db.DateTime, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    source = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    
    stock = db.relationship('Stock', backref=db.backref('mentions', lazy=True))


class StockPrice(db.Model):
    __tablename__ = 'stock_price'
   
    symbol = db.Column(db.Text, db.ForeignKey('stock.symbol'), primary_key=True)
    dt = db.Column(db.DateTime, primary_key=True)
    open = db.Column(db.Numeric, nullable=False)
    high = db.Column(db.Numeric, nullable=False)
    low = db.Column(db.Numeric, nullable=False)
    close = db.Column(db.Numeric, nullable=False)
    adjusted_close = db.Column(db.Numeric, nullable=False)
    volume = db.Column(db.Numeric, nullable=False)
    dividend_amount = db.Column(db.Numeric, nullable=False)

    stock = db.relationship('Stock', backref=db.backref('prices', lazy=True))


def connect_db(app):

    db.app = app
    db.init_app(app)