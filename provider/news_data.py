import requests
from service.database_models import Stock, StockNews
from datetime import datetime
from sqlalchemy import func
from dateutil.relativedelta import relativedelta

def insert_stock_news(db, headers, base_url):
    try:
        # Clear existing data
        db.session.query(StockNews).delete()
        db.session.commit()

        # Get to date
        to = datetime.today()

        # Format the date as "YYYY-MM-DD"
        formatted_to = to.strftime("%Y-%m-%d")

        # Get from date
        from_ = datetime.today() - relativedelta(months=3)

        # Format the date as "YYYY-MM-DD"
        formatted_from = from_.strftime("%Y-%m-%d") 

        # Get all stock symbols
        symbols = db.session.query(Stock.symbol).all()
        
        for number, symbol_tuple in enumerate(symbols, 1):
            symbol = symbol_tuple[0]
            print(f"Processing symbol {number}: {symbol}")
            page_token = None

            while True:
                url = f"{base_url}/v1beta1/news?start={formatted_from}&end={formatted_to}&sort=desc&symbols={symbol}&include_content=true&exclude_contentless=true"

                if page_token:
                    url += f"&page_token={page_token}"

                response = requests.get(url, headers=headers)
                print("Response Status Code:", response.status_code)
                if response.status_code != 200:
                    print(f"Failed to fetch data for {symbol}: {response.status_code}")
                    print("Response Body:", response.text)  # Additional Debugging

                    break

                data = response.json()
                news_data = data.get('news', [])
                if not news_data:
                    print(f"No data returned for {symbol}.")
                    break
                for news in news_data[0:15]:

                    stock_news = [
                        {
                            "symbol" : symbol
                            , "created" : datetime.strptime(news['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                            , "author" : news['author']
                            , "headline" : news['headline']
                            , "url" : news['url']
                            , "content" : news['summary']
                            , "id" : news['id']
                        }
                    ]

                db.session.bulk_insert_mappings(StockNews, stock_news)
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
                StockNews.symbol,
                func.max(StockNews.created).label('latest_dt')
            ).filter(StockNews.symbol == symbol).group_by(StockNews.symbol).all()
        else:
            # Fetch latest dates for all symbols
            symbol_dates = db.session.query(
                StockNews.symbol, 
                func.max(StockNews.dt).label('latest_dt')
            ).group_by(StockNews.symbol).all()

        for symbol, latest_dt in symbol_dates:
            print(f"Updating data for {symbol} from {latest_dt}")

            if latest_dt.strftime("%Y-%m-%d") == datetime.today():
                return print(f"No new data to update for {symbol}.")
            else:
                # Get to date
                to = datetime.today()

                # Format the date as "YYYY-MM-DD"
                formatted_to = to.strftime("%Y-%m-%d")

                # Get from date
                from_ = latest_dt.strftime("%Y-%m-%d")
                page_token = None

                while True:
                    url = f"{base_url}/v1beta1/news?start={from_}&end={formatted_to}&sort=desc&symbols={symbol}&include_content=true&exclude_contentless=true"

                    if page_token:
                        url += f"&page_token={page_token}"

                    response = requests.get(url, headers=headers)
                    print("Response Status Code:", response.status_code)
                    if response.status_code != 200:
                        print(f"Failed to fetch data for {symbol}: {response.status_code}")
                        print("Response Body:", response.text)  # Additional Debugging

                        break

                    data = response.json()
                    news_data = data.get('news', [])
                    if not news_data:
                        print(f"No data returned for {symbol}.")
                        break
                    for news in news_data[0:15]:

                        stock_news = [
                            {
                                "symbol" : symbol
                                , "created" : datetime.strptime(news['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                                , "author" : news['author']
                                , "headline" : news['headline']
                                , "url" : news['url']
                                , "content" : news['summary']
                                , "id" : news['id']
                            }
                        ]

                    db.session.bulk_insert_mappings(StockNews, stock_news)
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