import pandas as pd


def process():
    df = pd.read_csv("data/prediction_data.csv")
    df.fillna("", inplace=True)
    return df
