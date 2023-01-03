import pandas as pd
from src.tools.utils import load_yaml, upload_df_to_s3


def process():
    df_upload = pd.read_csv("data/prediction_data.csv", index_col=0)
    return df_upload
