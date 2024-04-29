import os
from dotenv import load_dotenv

from flask import Flask, render_template, request, flash, redirect, session, g, abort, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from service.database_models import db, connect_db, Stock, Mention, StockPrice

CURR_USER_KEY = "curr_user"

load_dotenv()

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
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