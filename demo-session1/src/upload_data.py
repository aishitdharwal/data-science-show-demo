import pandas as pd
import mysql.connector as msql
from mysql.connector import Error
from dotenv import load_dotenv
from pathlib import Path
import os

# read data
storage_df = pd.read_csv('data/sensor_storage_temperature.csv', index_col=False, delimiter = ',')
storage_df.drop(columns=['Unnamed: 0'], inplace=True)
storage_df.head()

# read mysql password
env_path = Path("./.env")
load_dotenv(dotenv_path=env_path)
mysql_pass = os.getenv("MYSQL_PASS")

# create a database 
try:
    conn = msql.connect(host='localhost', 
                        user='root',  
                        password=mysql_pass)
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("DROP DATABASE IF EXISTS groceries") 
        cursor.execute("CREATE DATABASE groceries")
        print("Database is created")
        cursor.execute("SHOW DATABASES")
except Error as e:
    print("Error while connecting to MySQL", e)
    
try:
    conn = msql.connect(host='localhost', 
                        user='root',  
                        password=mysql_pass)
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("USE groceries;")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS sensor_storage_temp;')
        print('Creating table....')
        cursor.execute("CREATE TABLE sensor_storage_temp(id VARCHAR(255),timestamp TIMESTAMP,temperature DECIMAL(6,2))")
        print("Table is created....")
        
        #loop through the data frame
        for i,row in storage_df.iterrows():
            #here %S means string values 
            sql = "INSERT INTO groceries.sensor_storage_temp VALUES (%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            # the connection is not auto committed by default, so we must commit to save our changes
            conn.commit()
except Error as e:
            print("Error while connecting to MySQL", e)
    
    