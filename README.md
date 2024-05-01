# [SP500-Capstone](https://sp500-capstone.onrender.com/)

This application provides interactive features for analyzing and predicting stock prices within the S&P 500 index. It enables users to fetch real-time and historical stock data, view stock-related news, and use predictive models to forecast future stock price movements.

## Features

- **Stock Data Retrieval**: Fetch real-time and historical data for any stock in the S&P 500.
- **Price Predictions**: Utilize advanced machine learning models to predict future stock prices.
- **Stock News**: Access and display recent news articles related to specific stocks.
- **Data Visualization**: Interactive charts to visualize stock price trends over time.

## Technologies Used

- **Python & Flask**: For backend API and server-side logic.
- **SQLAlchemy**: ORM for database transactions.
- **PostgreSQL**: Database for storing stock data.
- **AutoGluon**: Machine learning library for time series forecasting.
- **yfinance & Alpaca API**: To fetch stock data from Yahoo Finance and Alpaca Markets.
- **Bootstrap & Chart.js**: For frontend styling and data visualization.

## Usage

- Access the web interface at **https://sp500-capstone.onrender.com/**.
- Use the search bar to select a stock and view detailed information, including stock prices, predictions, and news.
- Interact with the stock chart to view different data points.

## API Endpoints

- `GET /stocks`: Retrieves a list of all S&P 500 stocks.
- `GET /price_data/<symbol>`: Retrieves historical price data for the specified stock symbol using the Alpaca Market Data API.
- `GET /price_data/<symbol>/refresh`: Uses the Alpaca API to update the price data for the specified stock symbol with the most recent information.
- `GET /get_news/<symbol>`: Retrieves recent news articles related to the specified stock symbol, also facilitated by the Alpaca News API.
