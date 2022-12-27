import argparse
import os
from pathlib import Path

import mysql.connector as msql
from dotenv import load_dotenv
from mysql.connector import Error
from utils import create_db_schema, get_data, load_yaml, get_path

parser = argparse.ArgumentParser()
#parser.add_argument("-d", "--input_data", help="provide path to input data", type=str)
parser.add_argument("-db", "--create_db", help="create db or not", default=False, type=bool)
#parser.add_argument("-t", "--table_name", help="provide table name", type=str)

parser.add_argument("-t", "--task", help="this will point to a task \
                    location into the config.yaml file.", type=str)
args = parser.parse_args()


# read mysql password
env_path = Path("./.env")
load_dotenv(dotenv_path=env_path)
mysql_pass = os.getenv("MYSQL_PASS")

# create a database
if args.create_db:
    try:
        conn = msql.connect(host='localhost',
                            user='root',
                            password=mysql_pass)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('DROP DATABASE IF EXISTS groceries')
            cursor.execute('CREATE DATABASE groceries')
            print("Database is created")
            cursor.execute('SHOW DATABASES')
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            #cursor.close()
            #conn.close()
    except Error as e:
        print("Error while connecting to MySQL", e)
# create a table in the database
else:
    # define variables
    # NEW ADDITION TO CODE -----------------------------------
    config = load_yaml("/Users/mits/Desktop/coursera/weekly_projects/data-science-show-demo/demo-session1/config/config.yaml")
    args_task = 'csv-to-database'
    config_import = config[args.task]["import"]
    config_import[0]["import"]

    input_data = get_path(config_import[0]["import"]["dirpath"], 
            config_import[0]["import"]["prefix_filename"]+ '.' +
            config_import[0]["import"]["file_extension"])
    table_name = os.path.basename(input_data).split('.')[0]
    #----------------------------------------------------------------------
    #input_data = Path(args.input_data)
    #table_name = args.table_name

    # get data and create db schema
    df = get_data(input_data)
    col_type, values = create_db_schema(df)
    try:
        conn = msql.connect(host='localhost',
                            user='root',
                            password=mysql_pass)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('USE groceries')
            cursor.execute(f'DROP TABLE IF EXISTS {table_name};')
            print(f"Creating table {table_name}....")
            cursor.execute(f'CREATE TABLE {table_name}({col_type})')
            print("Table is created....")
            
            #loop through the data frame
            for i,row in df.iterrows():
                sql = f'INSERT INTO groceries.{table_name} VALUES ({values})'
                cursor.execute(sql, tuple(row))                
                conn.commit()
            print("Record inserted")
    except Error as e:
        print("Error while connecting to MySQL", e)
