import argparse
import os
from pathlib import Path

import mysql.connector as msql
from dotenv import load_dotenv
from mysql.connector import Error
from utils import create_db_schema, get_data, load_yaml, get_path

# extract the arguments --------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("-db", "--create_db", help="create db or not", default=False, type=bool)
parser.add_argument("-db_name", "--db_name", help="database name", default=False, type=str)
parser.add_argument("-t", "--task", help="this will point to a task \
                    location into the config.yaml file.", type=str)
args = parser.parse_args()

# load tasks from config --------------------------------------------------------------
config = load_yaml("./config/config.yaml")

# read mysql password --------------------------------------------------------------
env_path = Path("./.env")
load_dotenv(dotenv_path=env_path)
mysql_pass = os.getenv("MYSQL_PASS")

# Main --------------------------------------------------------------
# create a database -----------
if args.create_db:
    try:
        conn = msql.connect(host='localhost',
                            user='root',
                            password=mysql_pass)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(f'DROP DATABASE IF EXISTS {args.db_name}')
            cursor.execute(f'CREATE DATABASE {args.db_name}')
            print(f"Database is created: {args.db_name}")
            cursor.execute('SHOW DATABASES')
            record = cursor.fetchall()
            print("Databases exist: ", record)
    except Error as e:
        print("Error while connecting to MySQL", e)
# create a table in the database -----------
else:
    # loop through each task in config.yaml 
    args_task = 'csv-to-database'
    config_import = config[args.task]["import"]
    for i in range(len(config_import)):
        input_data = get_path(config_import[i]["import"]["dirpath"], 
                config_import[i]["import"]["prefix_filename"]+ '.' +
                config_import[i]["import"]["file_extension"])
        table_name = os.path.basename(input_data).split('.')[0]
        # get data and create db schema
        df = get_data(input_data)
        col_type, values = create_db_schema(df)
        try:
            conn = msql.connect(host='localhost',
                                user='root',
                                password=mysql_pass)
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute(f'USE {args.db_name}')
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

