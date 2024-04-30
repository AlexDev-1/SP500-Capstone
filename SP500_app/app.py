import os
from urllib import response
from dotenv import load_dotenv

from flask import Flask, render_template, request, flash, redirect, session, g, abort, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from provider.predict_stock_data import predict_stock
from provider.price_data import fetch_incremental_stock_prices
from sqlalchemy import create_engine
import pandas as pd

from service.database_models import db, connect_db, Stock, StockPrice

CURR_USER_KEY = "curr_user"

load_dotenv()

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_ECHO'] = True
toolbar = DebugToolbarExtension(app)

base_url = os.environ.get('APCA_API_BASE_URL')

headers = {
    "accept": "application/json",
    "APCA-API-KEY-ID": os.environ.get('APCA-API-KEY-ID'),
    "APCA-API-SECRET-KEY": os.environ.get('APCA-API-SECRET-KEY')
}

connect_db(app)

@app.route('/')
def homepage():
    return render_template('base.html')

@app.route('/stocks')
def all_stocks():
    stocks = Stock.query.all()
    stock_list = [stock.to_dict() for stock in stocks]
    return jsonify(stock_list)

@app.route('/price_data/<string:symbol>')
def stock_data(symbol):
    data_price = StockPrice.query.filter_by(symbol=symbol)
    price_list = [price.to_dict() for price in data_price]
    return jsonify(price_list)

@app.route('/predict')
def stock_prediction():
    # Get query parameters
    symbol = request.args.get('symbol', default=None)
    value = request.args.get('value', default='close')  # Default to 'close' if not specified

    if not symbol:
        return jsonify({'error': 'The symbol parameter is required.'}), 400

    engine = create_engine(os.environ.get('DATABASE_URL'))
    query = db.session.query(StockPrice).filter_by(symbol=symbol).statement
    df = pd.read_sql(query, engine)

    if value not in df.columns:
        return jsonify({'error': f"'{value}' is not a valid column in the dataset."}), 400

    data_prediction = predict_stock(df, value)
    return data_prediction

@app.route('/price_data/<string:symbol>/refresh')
def refresh_stock_data(symbol):
    fetch_incremental_stock_prices(db, headers, base_url,symbol)
    data_price = StockPrice.query.filter_by(symbol=symbol)
    price_list = [price.to_dict() for price in data_price]
    return jsonify(price_list)