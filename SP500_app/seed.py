from app import db
from service.populate_symbols import fetch_sp500_symbols
from service.database_models import Stock

db.drop_all()
db.create_all()

db.session.commit()

fetch_sp500_symbols()

print(Stock.query.first().name)