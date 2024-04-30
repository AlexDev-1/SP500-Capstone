import pandas as pd
from requests_html import HTMLSession
from service.database_models import Stock
from io import StringIO
import yfinance as yf


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

# Function to insert data into the database using SQLAlchemy
def insert_stocks_data(df,db):
    stocks_data = []
    for index, row in df.iterrows():
        out = yahoo_company_info(row['symbol'])
        if out:  # Only add to batch if out is not empty
            stock_data = {
                'symbol': row['symbol'],
                'name': out.get('longName', ''),
                'industry': out.get('industry', ''),
                'sector': out.get('sector', '')
            }
            stocks_data.append(stock_data)

    if stocks_data:  # Only attempt to insert if there's data to insert
        try:
            with db.session.begin():
                db.session.bulk_insert_mappings(Stock, stocks_data)
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred during database commit: {e}")
        finally:
            db.session.close()

def yahoo_company_info(ticker):
    try:
        symbol_info_company = yf.Ticker(ticker)
        company_info = symbol_info_company.info
        company_information_layout = ["longName", "sector", "industry"]

        if 'error' in company_info:
            print(f"Error retrieving data for {ticker}: {company_info['error']}")
            return {}  # Return an empty dict if there's an error in the response

        out = {v: company_info[v] for v in company_information_layout if v in company_info}
        return out
    except Exception as e:
        print(f"An exception occurred while fetching data for {ticker}: {e}")
        return {}  # Return an empty dict to handle any exceptions gracefully