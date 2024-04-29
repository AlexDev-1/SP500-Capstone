from app import db
from provider.populate_symbols import fetch_sp500_symbols
from provider.price_data import insert_stock_prices
from service.database_models import Stock,StockPrice

db.drop_all()
db.create_all()

db.session.commit()

fetch_sp500_symbols()
print(Stock.query.first().name)
insert_stock_prices()
print("done")

