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
    dt_months_sorted = dt_months.sort_values("<close>")
    lowest = dt_months_sorted.head(1).iloc[0]["<close>"]
    hihgest = dt_months_sorted.tail(1).iloc[0]["<close>"]
    current = df_ticker_data.tail(1).iloc[0]["<close>"]
    print('current {0} low {1} high {2}'.format(current,lowest,highest))      
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
