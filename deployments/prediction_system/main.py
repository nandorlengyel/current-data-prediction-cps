#!/usr/bin/python3
import sched
import time
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from prophet import Prophet
import pandas as pd
import os

s = sched.scheduler(time.time, time.sleep)
org=os.environ['INFLUXDB_V2_ORG']

client = InfluxDBClient(url=os.environ['INFLUXDB_V2_URL'], org=org, token=os.environ['INFLUXDB_V2_TOKEN'], debug=True)

def predict_data(sc):
	df = query_data()
	prediction = run_prophet(df)
	write_data(prediction)
	s.enter(3, 1, predict_data, (sc,))

def query_data():	
	query = '''from(bucket: "MEASUREMENTS") 
	|> range(start:-5m, stop: now())
	|> filter(fn: (r) => r._measurement == "CurrentData" or r._measurement == "ActivityData")
	|> window(every: 5m)
  	|> mean()
	|> duplicate(column: "_stop", as: "ds")
	'''

	df = client.query_api().query_data_frame(query=query)
	df.drop(columns=['result', 'table','_start','_stop','_field'], inplace= True)
	df = df.pivot(index="ds",columns='_measurement', values='_value')
	df.rename(columns={"CurrentData": "y"}, inplace=True)
	df = pd.DataFrame(df.to_records())
	print(df.head())
	return df

def get_activity(ds):
    date = pd.to_datetime(ds)
	# TODO: Change values 0,1
    if date.weekday() < 5 and (date.hour < 18 and date.hour > 8):
        return 0
    else:
        return 1

def run_prophet(df):
	m = Prophet()
	m.add_regressor('ActivityData')
	m.fit(df)

	future = m.make_future_dataframe(periods=1, freq='min')
	future['ActivityData'] = future['ds'].apply(get_activity)
	
	print(future.tail())
	forecast = m.predict(future)
	print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
	return forecast[['ds', 'yhat']]

def write_data(df):
	df.rename(columns={"ds": "_time", "yhat":"value"}, inplace=True)
	df = df.set_index("_time")
	print(df)	
	write_api = client.write_api(write_options=SYNCHRONOUS)
	print(write_api.write("PREDICTIONS",org, df, data_frame_measurement_name="CurrentPrediction"))

s.enter(3, 1, predict_data, (s,))
s.run()