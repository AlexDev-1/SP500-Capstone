import os
import pandas as pd
from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor
from app import db
from service.database_models import StockPrice
from sqlalchemy import create_engine


def predict_stock(symbol, target='close'):

    engine = create_engine(os.environ.get('DATABASE_URL'))
    query = db.session.query(StockPrice).filter_by(symbol=symbol).statement
    df = pd.read_sql(query, engine)

    # Display the DataFrame
    print(df.head())

    # Prepare and fit the predictor
    ts_df = TimeSeriesDataFrame.from_data_frame(df, timestamp_column='dt',id_column='symbol')  # Assuming a single time series (no item_id column needed)
    predictor = TimeSeriesPredictor(prediction_length=6, target=target, freq='M', quantile_levels=[0.1,0.5,0.9] , eval_metric='WAPE')
    predictor.fit(ts_df, presets='high_quality', time_limit=60)
    forecast = predictor.predict(ts_df)

    # Display the forecast
    print('------------------------------------------------------------------------------------------------------------')
    return forecast.to_json()
