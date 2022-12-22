import os
import argparse
from pathlib import Path

import mysql.connector as msql
from dotenv import load_dotenv
from mysql.connector import Error

from utils import get_data, create_db_schema

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--input_data", help="provide path to input data", required=True, type=str)
parser.add_argument("-db", "--create_db", help="create db or not", default=False, type=bool)
parser.add_argument("-t", "--table_name", help="provide table name", type=str)
args = parser.parse_args()

# define variables
input_data = Path(args.input_data)
table_name = args.table_name

# get data and create db schema
df = get_data(input_data)
col_type, values = create_db_schema(df)

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
