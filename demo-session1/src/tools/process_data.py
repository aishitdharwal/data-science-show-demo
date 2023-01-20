import pandas as pd

def process():
    df_upload = pd.read_csv("data/merged.csv", index_col=0)
    return df_upload