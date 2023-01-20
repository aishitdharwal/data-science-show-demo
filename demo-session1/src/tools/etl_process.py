import pandas as pd
import warnings
from utils import get_data_sql

warnings.filterwarnings("ignore")
    
def get_data(database: str, table: str):
    return get_data_sql(database=database, table=table)

def drop_irrelevant_cols(df: pd.DataFrame, cols: list):
    df.drop(columns=[cols], inplace=True, errors='ignore')
    

def process():
    sales = get_data_sql("groceries", "sales")
    sensor_stock_levels = get_data_sql("groceries", "sensor_stock_levels")
    sensor_storage_temperature = get_data_sql("groceries", "sensor_storage_temperature")
    
    
    df_upload = pd.read_csv("data/merged.csv", index_col=0)
    return df_upload
