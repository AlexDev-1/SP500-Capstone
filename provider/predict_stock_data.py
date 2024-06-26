from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor


def predict_stock(df, target):
    # Display the DataFrame
    print(df.head())

    # Prepare and fit the predictor
    ts_df = TimeSeriesDataFrame.from_data_frame(df, timestamp_column='dt', id_column='symbol')
    predictor = TimeSeriesPredictor(prediction_length=6, target=target, freq='M', log_to_file=False,
                                    cache_predictions=False, quantile_levels=[0.1, 0.5, 0.9], eval_metric='WAPE')
    predictor.fit(ts_df, presets='high_quality', time_limit=10)
    forecast = predictor.predict(ts_df)

    # Display the forecast
    print('------------------------------------------------------------------------------------------------------------')
    print(forecast)

    # Convert forecast DataFrame to custom dictionary format
    forecast_results = []
    for index, row in forecast.iterrows():
        forecast_results.append({
            "symbol": index[0],
            "dt": index[1].strftime('%Y-%m-%d'),
            "mean": round(row['mean'], 2),
            "0.1": round(row['0.1'], 2),
            "0.5": round(row['0.5'], 2),
            "0.9": round(row['0.9'], 2)
        })

    return forecast_results

