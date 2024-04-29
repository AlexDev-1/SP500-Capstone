import requests
from app import db, headers, base_url
from service.database_models import Stock, StockPrice
from datetime import datetime, timedelta
from sqlalchemy import func

def insert_stock_prices():
    try:
        # Clear existing data
        db.session.query(StockPrice).delete()
        db.session.commit()

        # Get yesterday's date
        to = datetime.today() - timedelta(days=1)

        # Format the date as "YYYY-MM-DD"
        formatted_to = to.strftime("%Y-%m-%d")

        # Get yesterday's date
        from_ = datetime.today() - timedelta(days=1835)

        # Format the date as "YYYY-MM-DD"
        formatted_from = from_.strftime("%Y-%m-%d")

        # Get all stock symbols
        symbols = db.session.query(Stock.symbol).all()
        
        for number, symbol_tuple in enumerate(symbols, 1):
            symbol = symbol_tuple[0]
            print(f"Processing symbol {number}: {symbol}")
            page_token = None

            while True:
                url = f"{base_url}/v2/stocks/{symbol}/bars?&timeframe=1Day&start={formatted_from}&end={formatted_to}&adjustment=raw&feed=sip&sort=asc"
                if page_token:
                    url += f"&page_token={page_token}"

                response = requests.get(url, headers=headers)
                print("Response Status Code:", response.status_code)
                if response.status_code != 200:
                    print(f"Failed to fetch data for {symbol}: {response.status_code}")
                    print("Response Body:", response.text)  # Additional Debugging

                    break

                data = response.json()
                bars_data = data.get('bars', [])
                if not bars_data:
                    print(f"No data returned for {symbol}.")
                    break

                stock_prices = [
                    {
                        'symbol': symbol,
                        'dt': datetime.strptime(price['t'], '%Y-%m-%dT%H:%M:%SZ'),
                        'open': price['o'],
                        'high': price['h'],
                        'low': price['l'],
                        'close': price['c'],
                        'volume': price['v']
                    }
                    for price in bars_data
                ]

                db.session.bulk_insert_mappings(StockPrice, stock_prices)
                db.session.commit()

                page_token = data.get('next_page_token')
                if not page_token:
                    break

    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.session.close()
        print("Database session closed.")

if __name__ == "__main__":
    insert_stock_prices()
