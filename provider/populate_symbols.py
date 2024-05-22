import pandas as pd
from requests_html import HTMLSession
from service.database_models import Stock
from io import StringIO
import yfinance as yf
from service.symbols_service import insert_stocks_data


# Function to fetch S&P 500 symbols and populate the database
def fetch_sp500_symbols(db):
    try:
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        session = HTMLSession()
        response = session.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        # Parsing the first table found in the URL (S&P 500 constituents are typically in the first table)
        table = response.html.find('table', first=True)
        df = pd.read_html(StringIO(table.html))[0]

        # Renaming columns to align with database schema
        df = df.rename(columns={
            'Symbol': 'symbol',
        })

        # Selecting only the required columns
        df = df[['symbol']]

        # Cleaning the 'symbol' column to remove quotation marks
        df['symbol'] = df['symbol'].str.replace("'", "")

        # Insert the data into the database
        insert_stocks_data(df,db)
    except Exception as e:
        print(f"An error occurred: {e}")