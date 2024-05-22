from service.database_models import Stock, StockPrice
from service.alpaca_request import get_bars_data, fetch_dates_for_stocks
from datetime import datetime
from dateutil.relativedelta import relativedelta

def insert_stock_prices(db, headers, base_url):
    try:
        # Clear existing data
        db.session.query(StockPrice).delete()
        db.session.commit()

        # Get to date
        to = datetime.today() - relativedelta(weeks=1)

        # Format the date as "YYYY-MM-DD"
        formatted_to = to.strftime("%Y-%m-%d")

        # Get from date
        from_ = datetime.today() - relativedelta(months=120)

        # Format the date as "YYYY-MM-DD"
        formatted_from = from_.strftime("%Y-%m-%d") 

        # Get all stock symbols
        symbols = db.session.query(Stock.symbol).all()
        
        for number, symbol_tuple in enumerate(symbols, 1):
            symbol = symbol_tuple[0]
            print(f"Processing symbol {number}: {symbol}")
            page_token = None

            while True:
                
                response = get_bars_data(base_url,symbol,formatted_from,formatted_to,headers,page_token)

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
                        'dt': datetime.strptime(price['t'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d'),
                        'open': round(price['o'],2),
                        'high': round(price['h'],2),
                        'low': round(price['l'],2),
                        'close': round(price['c'],2),
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


def fetch_incremental_stock_prices(db, headers, base_url,symbol=None):
    try:

        symbol_dates = fetch_dates_for_stocks(db,symbol)

        for symbol, latest_dt in symbol_dates:
            print(f"Updating data for {symbol} from {latest_dt}")

            # Calculate the next day after the latest date
            next_day = latest_dt + relativedelta(days=1)
            formatted_next_day = next_day.strftime("%Y-%m-%d")

            # Get to date
            to = datetime.today() - relativedelta(months=1)

            # Format the date as "YYYY-MM-DD"
            formatted_today = to.strftime("%Y-%m-%d")

            # API call to Alpaca for specific symbol
            response = get_bars_data(base_url,symbol,formatted_next_day,formatted_today,headers)
            
            if response.status_code == 200:
                data = response.json()
                bars_data = data.get('bars', [])
                if bars_data:
                    # Insert new data
                    stock_prices = [
                        {
                            'symbol': symbol,
                            'dt': datetime.strptime(price['t'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d'),
                            'open': round(price['o'], 2),
                            'high': round(price['h'], 2),
                            'low': round(price['l'], 2),
                            'close': round(price['c'], 2),
                            'volume': price['v']
                        }
                        for price in bars_data
                    ]
                    db.session.bulk_insert_mappings(StockPrice, stock_prices)
                    db.session.commit()
                else:
                    print(f"No new data to update for {symbol}.")
            else:
                print(f"Failed to fetch data for {symbol}: {response.status_code}")

    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.session.close()
        print("Database session closed.")