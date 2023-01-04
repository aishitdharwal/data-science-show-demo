# -*- coding: utf-8 -*-


# Task 1 - Exploratory Data Analysis

"""---
## Section 1 - Import modules
"""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import FuncFormatter

plt.style.use('ggplot')


"""---
## Section 2 - Data loading
"""

path = "data/sales.csv"
df = pd.read_csv(path)
df.drop(columns=["Unnamed: 0"], inplace=True, errors='ignore')
print(df.head())


"""---
## Section 3 - Descriptive statistics
"""
print(df.info()) # no missing values, need to change datatype: timestamp

print(df.describe()) # do have some skewness

# which are the top 5 selling categories
print(df.head())

top_10 = df.groupby('category')['quantity', 'total'].agg({'quantity': 'count', 'total': 'sum'}).sort_values(by='total', ascending=False)[:10].reset_index()
print(top_10)

df['timestamp'] = pd.to_datetime(df['timestamp'])

df['hour'] = df['timestamp'].dt.hour

df['hour'].value_counts()



"""---
## Section 4 - Visualisation
"""

def currency(x, pos):
    'The two args are the value and tick position'
    if x >= 1000000:
        return '${:1.1f}M'.format(x*1e-6)
    return '${:1.0f}K'.format(x*1e-3)

formatter = FuncFormatter(currency)

fig, (ax1, ax2) = plt.subplots(figsize=(10,6), nrows=1, ncols=2, sharey=True)
top_10.plot(kind='barh', x='category', y='total', ax=ax1)
ax1.set_title("Revenue by top 10 categories")
ax1.set_xlabel('Category')
ax1.set_ylabel('Total revenue')
formatter = FuncFormatter(currency)
ax1.xaxis.set_major_formatter(formatter)
ax1.legend("");


top_10.plot(kind='barh', x='category', y='quantity', ax=ax2)
ax2.set_title("Quantities")
ax2.set_xlabel('Total units sold')
ax2.legend("");


def plot_continuous_distribution(data: pd.DataFrame = None, column: str = None, height: int = 8):
  _ = sns.displot(data, x=column, kde=True, height=height, aspect=height/5).set(title=f'Distribution of {column}');

def get_unique_values(data, column):
  num_unique_values = len(data[column].unique())
  value_counts = data[column].value_counts()
  print(f"Column: {column} has {num_unique_values} unique values\n")
  print(value_counts)

def plot_categorical_distribution(data: pd.DataFrame = None, column: str = None, height: int = 8, aspect: int = 2):
  _ = sns.catplot(data=data, x=column, kind='count', height=height, aspect=aspect).set(title=f'Distribution of {column}');

def correlation_plot(data: pd.DataFrame = None):
  corr = df.corr()
  corr.style.background_gradient(cmap='coolwarm')

plot_continuous_distribution(data=df, column='unit_price') 
# skewness: positive, there are lots of products with low price than high price,

plot_continuous_distribution(data=df, column='quantity') 
# only 4 unique quantites with equal distribution - each quantity is equaly sold

plot_continuous_distribution(data=df, column='total')
# skewness: positive, as expected since there are lots of cheap products -> high revenue in cheaper products than expensive ones

plot_categorical_distribution(data=df, column='category', height=10, aspect=3.5)
# fruits & vegetables are the most frequent purchased product

plot_categorical_distribution(data=df, column='customer_type')
#5 unique customer_types

plot_categorical_distribution(data=df, column='payment_type')
#4 unique payment_types - cash is the most frequent way of payment

plot_categorical_distribution(df, column='hour')

corr = df.corr()
corr.style.background_gradient(cmap='coolwarm')



path = "data/sales.csv"

sales_df = pd.read_csv(path)
sales_df.drop(columns=["Unnamed: 0"], inplace=True, errors='ignore')
print(sales_df.head())

stock_df = pd.read_csv("data/sensor_stock_levels.csv")
stock_df.drop(columns=["Unnamed: 0"], inplace=True, errors='ignore')
print(stock_df.head())

temp_df = pd.read_csv("data/sensor_storage_temperature.csv")
temp_df.drop(columns=["Unnamed: 0"], inplace=True, errors='ignore')
print(temp_df.head())

"""Now it's up to you, refer back to the steps in your strategic plan to complete this task. Good luck!



---
## Section 3 - Data cleaning
"""

print(sales_df.info())

def convert_to_datetime(data: pd.DataFrame, column: str):
  data[column] = pd.to_datetime(data[column])
  return data

sales_df = convert_to_datetime(sales_df, 'timestamp')
print(sales_df.info())

print(stock_df.info())

stock_df = convert_to_datetime(stock_df, 'timestamp')
print(stock_df.info())

temp_df = convert_to_datetime(temp_df, 'timestamp')
print(temp_df.info())

def convert_timestamp_to_hourly(data: pd.DataFrame, column: str):
  new_ts = data[column].tolist()
  new_ts = [i.to_period(freq='H') for i in new_ts]
  data[column] = new_ts
  return data

print(sales_df.shape)

sales_df = convert_timestamp_to_hourly(sales_df, 'timestamp')
print(sales_df)

stock_df = convert_timestamp_to_hourly(stock_df, 'timestamp')
print(stock_df)

temp_df = convert_timestamp_to_hourly(temp_df, 'timestamp')
print(temp_df)

print(stock_df.info())

print(sales_df.info())

print(temp_df.info())

print(sales_df.head())

sales_agg = sales_df.groupby(['timestamp', 'product_id']).agg({'quantity': 'sum'}).reset_index()

stock_agg = stock_df.groupby(['timestamp', 'product_id']).agg({'estimated_stock_pct': 'mean'}).reset_index()

temp_agg = temp_df.groupby(['timestamp']).agg({'temperature': 'mean'}).reset_index()

merged_df = pd.merge(stock_agg, sales_agg, how='left', on = ['timestamp', 'product_id'])
print(merged_df)

merged_df = pd.merge(merged_df, temp_agg, how='left', on=['timestamp'])

print(merged_df)

merged_df.to_csv('data/merged.csv', index=False)

# train/test -> retrain on whole data -> generate future 7 days data -> forecast on future data


