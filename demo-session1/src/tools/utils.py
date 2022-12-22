import pathlib
from typing import Tuple

import pandas as pd


def get_data(input_data: pathlib.Path) -> pd.DataFrame:
    """Returns csv data as a dataframe

    Args:
        input_data (pathlib.Path): provide path to input data

    Returns:
        pd.DataFrame: dataframe
    """
    df = pd.read_csv(input_data, index_col=False, delimiter = ',')
    df.drop(columns=['Unnamed: 0'], inplace=True)
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