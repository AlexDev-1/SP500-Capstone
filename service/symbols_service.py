from service.database_models import Stock
import yfinance as yf

# Function to insert data into the database using SQLAlchemy
def insert_stocks_data(df,db):
    stocks_data = []
    for index, row in df.iterrows():
        out = yahoo_company_info(row['symbol'])
        stock_data = {
            'symbol': row['symbol'],
            'name': out.get('longName', ''),
            'industry': out.get('industry', ''),
            'sector': out.get('sector', '')
        }
        stocks_data.append(stock_data)

    try:
        with db.session.begin():
            db.session.bulk_insert_mappings(Stock, stocks_data)
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred during database commit: {e}")
    finally:
        db.session.close()

def yahoo_company_info(ticker):
    symbol_info_company = yf.Ticker(ticker)
    company_info = symbol_info_company.info
    company_information_layout = ["longName", "sector", "industry"]
    out = {v: company_info[v] for v in company_information_layout if v in company_info}
    return out