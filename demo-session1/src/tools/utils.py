import datetime
import importlib
import os
import pathlib
from io import BytesIO, StringIO
from pathlib import Path, PurePath
from typing import List, Tuple, Union

import boto3
import gspread
import pandas as pd
import yaml
import mysql.connector as msql
from mysql.connector import Error
from dotenv import load_dotenv
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

# read mysql password --------------------------------------------------------------
env_path = Path("./.env")
load_dotenv(dotenv_path=env_path)
mysql_pass = os.getenv("MYSQL_PASS")

# helper functions --------------------------------------------------------------
def get_data_sql(database: str, table: str) -> pd.DataFrame:
    try:
        conn = msql.connect(host='localhost',
                            user='root',
                            password=mysql_pass,
                            database=database)
        if conn.is_connected():
            query = f'SELECT * FROM {table}'
            print(f"Fetching {table} from {database} database")
            df = pd.read_sql(query, con=conn)
    except Error as e:
        print("Error while connecting to MySQL", e)
    return df


def get_data(input_data: pathlib.Path) -> pd.DataFrame:
    """Returns csv data as a dataframe

    Args:
        input_data (pathlib.Path): provide path to input data

    Returns:
        pd.DataFrame: dataframe
    """
    df = pd.read_csv(input_data, index_col=False, delimiter = ',')
    df.drop(columns=['Unnamed: 0'], inplace=True, axis=1, errors='ignore')
    return df


def create_db_schema(df: pd.DataFrame) -> Tuple[str, str]:
    """Creates SQL column parameters and datatype from pandas dataframe.
    Creates a placeholder for each row in the dataframe. The placeholder can
    then be used in an SQL `INSERT` statement in `VALUES`

    Args:
        df (pd.DataFrame): provide input dataframe

    Returns:
        Tuple[str, str]: tuple(`column_name datatype`), and placeholder %s
    """
    types = []
    for i in df.dtypes:
        if i == 'object':
            types.append('VARCHAR(255)')
        elif i == 'float64':
            types.append('DECIMAL(6,2)')
        elif i == 'int':
            types.append('INT')
    col_type = list(zip(df.columns.values, types))
    col_type = tuple([" ".join(i) for i in col_type])
    col_type = ', '.join(col_type)
    values = ', '.join(['%s' for _ in range(len(df.columns))])
    return col_type, values


def load_yaml(file_path: str):
    """This function loads a yaml file and outputs the file as a dict

    Args:
        file_path (str): path of the name where yaml file is
        
    Output:
        returns a dict of params
    """
    with open(file_path, 'r') as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def get_path(*args: Union[str, os.PathLike]) -> str:
    """Build a path from path fragments.

    Args:
        Args: should be of type str or one of pathlib.Path flavors.
        
    Returns:
        str: normalized path
    """
    return PurePath(*args).as_posix()


def aws_auth():
    """Authenticate aws

    Returns:
        _type_: returns info
    """
    env_path = Path("./.env")
    load_dotenv(dotenv_path=env_path)
    session=boto3.Session(region_name="us-east-1")
    bucket = os.getenv("BUCKET")
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    return session, bucket, aws_access_key_id, aws_secret_access_key


def upload_df_to_s3(df: pd.DataFrame, filename_prefix: str):
    """Upload dataframe to S3 as CSV

    Args:
        df (pd.DataFrame): dataframe to upload
        filename_prefix (str): filename prefix

    Returns:
        _type_: Status Code
    """
    
    _, bucket, _, _ = aws_auth()
    key = filename_prefix + datetime.datetime.now().strftime("%Y-%m-%d") + ".csv"
    
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    client = boto3.client('s3')
    response = client.put_object(
        ACL = 'private',
        Body=csv_buffer.getvalue(),
        Bucket = bucket,
        Key=key
    )
    return response['ResponseMetadata']['HTTPStatusCode']


def import_from_s3(filename: str) -> pd.DataFrame:
    """Import data from S3

    Args:
        filename (str): object to import

    Returns:
        pd.DataFrame: returned as dataframe
    """
    _, bucket, aws_access_key_id, aws_secret_access_key = aws_auth()
    region_name = "us-east-1"
    s3 = boto3.resource(
        service_name="s3",
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    
    obj = s3.Bucket(bucket).Object(filename)
    data=obj.get()['Body'].read()
    df = pd.read_csv(BytesIO(data), header=0, delimiter=",", low_memory=False)\
        .drop(columns=['Unnamed: 0'], axis=1, errors='ignore')
    return df


def check_all_files_s3() -> List:
    """Check objects in S3 bucket

    Returns:
        List: list of files that exist in S3
    """
    _, bucket, aws_access_key_id, aws_secret_access_key = aws_auth()
    region_name = "us-east-1"
    s3 = boto3.resource(
        service_name="s3",
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    bucket = s3.Bucket('ds-project-demo1')   
    files = [filename.key for filename in bucket.objects.filter(Prefix='')]
    return files


def gsheet_auth():
    """Authenticate google sheet

    Returns:
        creds, client: connection object
    """
    SCOPES = [
        "https://spreadsheets.google.com/feeds",
        'https://www.googleapis.com/auth/spreadsheets',
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]
    
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", SCOPES)
    client = gspread.authorize(creds)
    return creds, client

   
def import_from_gsheet(filename: str) -> List:
    """Import data from gsheet

    Args:
        filename (str): google file name

    Returns:
        data (list): data from gsheet
    """
    _, client = gsheet_auth()
    sheet = client.open(filename).sheet1  
    data = sheet.get_all_records()      
    return data
    

def export_to_gsheet(spreedsheetId: str, df: pd.DataFrame, clear_sheet: bool=False):
    """Export data to google sheets

    Args:
        spreedsheetId (str): google sheet ID
        df (pd.DataFrame): dataframe to write to gsheet
        clear_sheet (bool, optional): clear sheet or not. Defaults to False.
    """
    creds, _ = gsheet_auth()
    service = build("sheets", "v4", credentials=creds)
    df.fillna("", inplace=True)
    #myspreadsheets = service.spreadsheets().get(spreadsheetId=spreedsheetId).execute()
    if clear_sheet:
        service.spreadsheets().values().clear(
            spreadsheetId=spreedsheetId,
            range="A1:AA1000000",
        ).execute()
    else:
        service.spreadsheets().values().update(
            spreadsheetId=spreedsheetId,
            valueInputOption="USER_ENTERED",
            range="A1:AA1000000",
            body=dict(
                majorDimension="ROWS",
                values=df.T.reset_index().T.values.tolist()
            ),
        ).execute()


def process(task: str) -> dict:
    """Import task file to process the data from src/tools folder

    Args:
        task (str): name of the task to process

    Returns:
        dict: processed_data
    """
    lib = importlib.import_module(f"src.tools.{task}")
    return lib.process()
