import pandas as pd
import os.path as osp
import os
import talib
import math

from datetime import datetime

def calculate_low(df_ticker_data):
    df_ticker_data = df_ticker_data.sort_values("<tgl>")
    df_ticker_data = df_ticker_data[["<open>","<close>","<high>","<low>","<volume>","<ticker>","<tgl>"]]
    df_months = df_ticker_data.tail(180)
    df_months_sorted = df_months.sort_values("<close>")
    lowest = df_months_sorted.head(1).iloc[0]["<close>"]
    highest = df_months_sorted.tail(1).iloc[0]["<close>"]
    current = df_ticker_data.tail(1).iloc[0]["<close>"]
    name = df_ticker_data.tail(1).iloc[0]["<ticker>"]
    pctHigh =  pct_diff(current,highest)
    pctLow = pct_diff(current,lowest)
    if pctLow > 10  and pctLow < 20 and pctHigh > 60 :
       print('name {0} current {1} low {2} high {3}'.format(name,current,lowest,highest))      
    return df_ticker_data

def pct_diff(a,b):
    return (abs(a-b) / ((a + b) / 2)) * 100 

localdir_result = "/home/Kiasemoto/dev/stock/result/"
df_all_data = pd.read_csv(osp.join(localdir_result,"alldata.csv"))
df_all_data["<tgl>"] = pd.to_datetime(df_all_data["<date>"])

all_ticker = df_all_data["<ticker>"].drop_duplicates().sort_values()
for current_ticker in all_ticker:
    df_current_ticker = df_all_data[df_all_data["<ticker>"] == current_ticker]
    df_current_ticker = calculate_low(df_current_ticker)
