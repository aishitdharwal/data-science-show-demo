# -*- coding: utf-8 -*-

import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

# read data
df = pd.read_csv('data/merged.csv')

df.index = pd.to_datetime(df['timestamp'])
df['quantity'].fillna(0, inplace=True)

prediction_df_list = []
# loop on each product
for product in df['product_id'].unique():
    
    # filter out product
    prod_df = df[df['product_id']==product]
    
    # train on the first 6 days
    train = prod_df[prod_df.index < pd.to_datetime('2022-03-07')]
    # test on the 7th day
    test = prod_df[prod_df.index >= pd.to_datetime('2022-03-07')]
    
    y = train['quantity']
    
    # initialize SARIMAX model with exogenous variable
    ARMAmodel = SARIMAX(y, order = (1, 0, 1), exog=train['temperature'])
    ARMAmodel = ARMAmodel.fit()
    
    y_pred = ARMAmodel.get_forecast(len(test.index), exog=test['temperature'])
    y_pred_df = y_pred.conf_int(alpha = 0.05)
    y_pred_df["predictions"] = ARMAmodel.predict(start = y_pred_df.index[0], end = y_pred_df.index[-1], exog=test['temperature'])
    y_pred_df.index = test.index
    y_pred_out = y_pred_df[["predictions"]]
    plt.plot(y_pred_out, color='green', label = 'predictions')
    plt.legend()
    y_pred_out['product_id'] = product
    y_pred_out.reset_index(inplace=True)
    
    prediction_df_list.append(y_pred_out)

prediction_df = pd.concat(prediction_df_list)

prediction_df.to_csv('prediction_data.csv', index=False)
