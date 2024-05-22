import requests
from service.database_models import StockPrice,StockNews
from sqlalchemy import func


def fetch_dates_for_stocks(db,symbol):

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

    return symbol_dates


def get_bars_data(base_url,symbol,formatted_from,formatted_to,headers,page_token=None):
    
    url = f"{base_url}/v2/stocks/{symbol}/bars?timeframe=1M&start={formatted_from}&end={formatted_to}&adjustment=all&feed=sip&sort=asc"
    
    if page_token:
        url += f"&page_token={page_token}"

    response = requests.get(url, headers=headers)
    print("Response Status Code:", response.status_code)

    if response.status_code != 200:
        print(f"Failed to fetch data for {symbol}: {response.status_code}")
        print("Response Body:", response.text)  # Additional Debugging
    
    return response

def get_news_data(base_url,symbol,formatted_from,formatted_to,headers,page_token=None):
    url = f"{base_url}/v1beta1/news?start={formatted_from}&end={formatted_to}&sort=desc&symbols={symbol}&include_content=true&exclude_contentless=true"

    if page_token:
        url += f"&page_token={page_token}"

    response = requests.get(url, headers=headers)
    print("Response Status Code:", response.status_code)

    return response

def fetch_dates_for_news(db,symbol):
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

        return symbol_dates