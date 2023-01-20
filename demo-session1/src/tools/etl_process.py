import pandas as pd
import os
import shutil
import warnings
from utils import get_data_sql
from datetime import datetime

warnings.filterwarnings("ignore")
    
def clean_data(database: str, table: str) -> pd.DataFrame:
    """This function reads raw data from the database. Converts datatypes to correct format.

    Args:
        database (str): database name
        table (str): table name in the database

    Returns:
        pd.DataFrame: cleaned dataframe
    """
    df = get_data_sql(database=database, table=table)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S')
    return df


def feature_eng(df: pd.DataFrame, column: str = None):
    new_ts = df[column].tolist()
    new_ts = [i.strftime('%Y-%m-%d %H:00:00') for i in new_ts]
    new_ts = [datetime.strptime(i, '%Y-%m-%d %H:00:00') for i in new_ts]
    df[column] = new_ts
    return df

def data_processing(sales_df: pd.DataFrame, stock_df: pd.DataFrame, temp_df: pd.DataFrame, save_files_local: bool = False) -> pd.DataFrame:
    sales_df = feature_eng(sales_df, 'timestamp')
    stock_df = feature_eng(stock_df, 'timestamp')
    temp_df = feature_eng(temp_df, 'timestamp')
    
    sales_agg = sales_df.groupby(['timestamp', 'product_id']).agg({'quantity': 'sum'}).reset_index()
    stock_agg = stock_df.groupby(['timestamp', 'product_id']).agg({'estimated_stock_pct': 'mean'}).reset_index()
    temp_agg = temp_df.groupby(['timestamp']).agg({'temperature': 'mean'}).reset_index()
    
    if save_files_local:
        file_path = "cleaned_data"
        if os.path.exists(file_path):
            shutil.rmtree(file_path)
            #os.rmdir(file_path)
        os.makedirs(file_path)
        sales_agg.to_csv("cleaned_data/sales_agg.csv")
        stock_agg.to_csv("cleaned_data/stock_agg.csv")
        temp_agg.to_csv("cleaned_data/temp_agg.csv") 
    return sales_agg, stock_agg, temp_agg
    

def process():
    
    # step 1
    sales = clean_data("groceries", "sales")
    sensor_stock_levels = clean_data("groceries", "sensor_stock_levels")
    sensor_storage_temperature = clean_data("groceries", "sensor_storage_temperature")
    
    # step 2
    sales_agg, stock_agg, temp_agg = data_processing(sales, sensor_stock_levels, sensor_storage_temperature, save_files_local=False)
    
    return print("ETL PROCESS COMPLETED!")
