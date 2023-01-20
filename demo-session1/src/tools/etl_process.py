import pandas as pd
import os
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

def data_processing(sales_df: pd.DataFrame, stock_df: pd.DataFrame, temp_df: pd.DataFrame, save_files: bool = False) -> pd.DataFrame:
    sales_df = feature_eng(sales_df, 'timestamp')
    stock_df = feature_eng(stock_df, 'timestamp')
    temp_df = feature_eng(temp_df, 'timestamp')
    
    sales_agg = sales_df.groupby(['timestamp', 'product_id']).agg({'quantity': 'sum'}).reset_index()
    stock_agg = stock_df.groupby(['timestamp', 'product_id']).agg({'estimated_stock_pct': 'mean'}).reset_index()
    temp_agg = temp_df.groupby(['timestamp']).agg({'temperature': 'mean'}).reset_index()
    
    if save_files:
        #file_path = "cleaned_data"
        #if not os.path.exists(file_path):
         #   os.mkdir(file_path)
        # Create the path for the folder
        path = os.path.join(os.getcwd(), 'cleaned_data')
        # Check if the folder exists, if not create it
        if not os.path.exists(path):
            os.mkdir(path)
        sales_agg.to_csv(os.path.join(path, "sales_agg.csv"), index=False)
        stock_agg.to_csv(os.path.join(path, "stock_agg.csv"))
        temp_agg.to_csv(os.path.join(path, "temp_agg.csv"))
        # Commit and push the changes to GitHub
        os.system('git add .')
        os.system('git commit -m "added cleaned data"')
        os.system('git push origin main')
    return sales_agg, stock_agg, temp_agg
    

def process():
    
    # step 1
    sales = clean_data("groceries", "sales")
    sensor_stock_levels = clean_data("groceries", "sensor_stock_levels")
    sensor_storage_temperature = clean_data("groceries", "sensor_storage_temperature")
    
    # step 2
    sales_agg, stock_agg, temp_agg = data_processing(sales, sensor_stock_levels, sensor_storage_temperature, save_files=False)
    
    return print("ETL PROCESS COMPLETED!")
