# -*- coding: utf-8 -*-


# Task 1 - Exploratory Data Analysis

"""---
## Section 1 - Import modules
"""

import pandas as pd

"""---
## Section 2 - Data loading
"""

path = "data/sales.csv"
sales_df = pd.read_csv(path)
sales_df.drop(columns=["Unnamed: 0"], inplace=True, errors='ignore')


"""---
## Section 3 - Descriptive statistics
"""
top_10 = sales_df.groupby('category')['quantity', 'total'].agg({'quantity': 'count', 'total': 'sum'}).sort_values(by='total', ascending=False)[:10].reset_index()
sales_df['timestamp'] = pd.to_datetime(sales_df['timestamp'])
sales_df['hour'] = sales_df['timestamp'].dt.hour

"""---
## Section 4 - Visualisation
"""



sales_df.drop(columns=["Unnamed: 0"], inplace=True, errors='ignore')
stock_df = pd.read_csv("data/sensor_stock_levels.csv")
stock_df.drop(columns=["Unnamed: 0"], inplace=True, errors='ignore')
temp_df = pd.read_csv("data/sensor_storage_temperature.csv")
temp_df.drop(columns=["Unnamed: 0"], inplace=True, errors='ignore')

"""
---
## Section 3 - Data cleaning
"""
def convert_to_datetime(data: pd.DataFrame, column: str):
  data[column] = pd.to_datetime(data[column])
  return data

sales_df = convert_to_datetime(sales_df, 'timestamp')
stock_df = convert_to_datetime(stock_df, 'timestamp')
temp_df = convert_to_datetime(temp_df, 'timestamp')


def convert_timestamp_to_hourly(data: pd.DataFrame, column: str):
  new_ts = data[column].tolist()
  new_ts = [i.to_period(freq='H') for i in new_ts]
  data[column] = new_ts
  return data


sales_df = convert_timestamp_to_hourly(sales_df, 'timestamp')
stock_df = convert_timestamp_to_hourly(stock_df, 'timestamp')
temp_df = convert_timestamp_to_hourly(temp_df, 'timestamp')
sales_agg = sales_df.groupby(['timestamp', 'product_id']).agg({'quantity': 'sum'}).reset_index()
stock_agg = stock_df.groupby(['timestamp', 'product_id']).agg({'estimated_stock_pct': 'mean'}).reset_index()
temp_agg = temp_df.groupby(['timestamp']).agg({'temperature': 'mean'}).reset_index()
sales_agg.to_csv('cleaned_data/sales_agg.csv', index=False)
stock_agg.to_csv('cleaned_data/stock_agg.csv', index=False)
temp_agg.to_csv('cleaned_data/temp_agg.csv', index=False)


