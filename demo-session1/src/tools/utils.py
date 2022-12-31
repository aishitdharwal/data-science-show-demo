import pathlib
import yaml
from typing import Tuple
from pathlib import PurePath

import pandas as pd


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

def get_path(*args):
    return PurePath(*args).as_posix()
        