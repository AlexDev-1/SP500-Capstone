import requests
from service.database_models import Stock, StockPrice
from datetime import datetime
from sqlalchemy import func
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
                url = f"{base_url}/v2/stocks/{symbol}/bars?&timeframe=1M&start={formatted_from}&end={formatted_to}&adjustment=all&feed=sip&sort=asc"
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
        if symbol:
            # Fetch latest date only for the specified symbol
            symbol_dates = db.session.query(
                StockPrice.symbol,
                func.max(StockPrice.dt).label('latest_dt')
            ).filter(StockPrice.symbol == symbol).group_by(StockPrice.symbol).all()
        else:
            # Fetch latest dates for all symbols
            symbol_dates = db.session.query(
                StockPrice.symbol, 
                func.max(StockPrice.dt).label('latest_dt')
            ).group_by(StockPrice.symbol).all()

        for symbol, latest_dt in symbol_dates:
            print(f"Updating data for {symbol} from {latest_dt}")

            # Calculate the next day after the latest date
            next_day = latest_dt + relativedelta(days=1)
            formatted_next_day = next_day.strftime("%Y-%m-%d")
            # Get yesterday's date
            to = datetime.today() - relativedelta(months=1)
            # Format the date as "YYYY-MM-DD"
            formatted_today = to.strftime("%Y-%m-%d")

            url = f"{base_url}/v2/stocks/{symbol}/bars?timeframe=1M&start={formatted_next_day}&end={formatted_today}&adjustment=all&feed=sip&sort=asc"
            response = requests.get(url, headers=headers)
            response = requests.get(url, headers=headers)
            print("Response Status Code:", response.status_code)
            if response.status_code != 200:
                print(f"Failed to fetch data for {symbol}: {response.status_code}")
                print("Response Body:", response.text)  # Additional Debugging
            
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