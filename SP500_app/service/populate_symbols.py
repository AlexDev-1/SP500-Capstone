from sqlalchemy.exc import IntegrityError
import pandas as pd
from requests_html import HTMLSession
from service.database_models import Stock
from app import db

db.session.query(Stock).delete()
db.session.commit()

# Function to fetch S&P 500 symbols and populate the database
def fetch_sp500_symbols():
    try:
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        session = HTMLSession()
        response = session.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        # Parsing the first table found in the URL (S&P 500 constituents are typically in the first table)
        table = response.html.find('table', first=True)
        df = pd.read_html(table.html)[0]

        # Renaming columns to align with database schema
        df = df.rename(columns={
            'Symbol': 'symbol_id',
        })

        # Selecting only the required columns
        df = df[['symbol_id']]

        # Insert the data into the database
        insert_stocks_data(df)
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to insert data into the database using SQLAlchemy
def insert_stocks_data(df):
    try:
        for index, row in df.iterrows():
            stock = Stock(
                symbol_id=row['symbol_id'],
            )
            db.session.add(stock)
        db.session.commit()
    except IntegrityError:
        # Handle integrity errors for duplicate primary keys
        db.session.rollback()
        print("IntegrityError: Duplicate symbol_id detected. Skipping insertion.")

# Execute the main function
if __name__ == "__main__":
    fetch_sp500_symbols()