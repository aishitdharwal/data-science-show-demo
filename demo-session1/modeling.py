# -*- coding: utf-8 -*-

import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

df = pd.read_csv('data/merged.csv')
df.index = pd.to_datetime(df['timestamp'])
df['quantity'].fillna(0, inplace=True)

for product in df['product_id'].unique():
    prod_df = df[df['product_id']==product]
    train = prod_df[prod_df.index < pd.to_datetime('2022-03-07')]
    test = prod_df[prod_df.index >= pd.to_datetime('2022-03-07')]
    y = train['quantity']
    ARMAmodel = SARIMAX(y, order = (1, 0, 1))
    ARMAmodel = ARMAmodel.fit()
    y_pred = ARMAmodel.get_forecast(len(test.index))
    y_pred_df = y_pred.conf_int(alpha = 0.05)
    y_pred_df["Predictions"] = ARMAmodel.predict(start = y_pred_df.index[0], end = y_pred_df.index[-1])
    y_pred_df.index = test.index
    y_pred_out = y_pred_df["Predictions"]
    plt.plot(y_pred_out, color='green', label = 'Predictions')
    plt.legend()