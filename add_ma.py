import pandas as pd
import os.path as osp
import os
import talib
import math

from datetime import datetime

def calculate_ma(df_ticker_data):
    df_ticker_data = df_ticker_data.sort_values("<tgl>")
    df_ticker_data = df_ticker_data[["<open>","<close>","<high>","<low>","<volume>","<ticker>","<tgl>"]]
    df_ticker_data["<MA100>"]  = talib.SMA(df_ticker_data["<close>"],100)
    df_ticker_data["<MA200>"]  = talib.SMA(df_ticker_data["<close>"],200)
    df_ticker_data["<MA30>"]  = talib.SMA(df_ticker_data["<close>"],30)
    df_ticker_data["<MA10>"]  = talib.SMA(df_ticker_data["<close>"],10)
    df_ticker_data["<EMA8>"]  = talib.EMA(df_ticker_data["<close>"],8)
    return df_ticker_data

def pct_diff(a,b):
    return (abs(a-b) / ((a + b) / 2)) * 100 

localdir_result = "/usr/src/stock/result/"
df_all_data = pd.read_csv(osp.join(localdir_result,"alldata.csv"))
df_all_data["<tgl>"] = pd.to_datetime(df_all_data["<date>"])

all_ticker = df_all_data["<ticker>"].drop_duplicates().sort_values()
for current_ticker in all_ticker:
    df_current_ticker = df_all_data[df_all_data["<ticker>"] == current_ticker]
    df_current_ticker = calculate_ma(df_current_ticker)
    df_last_data = df_current_ticker.tail(1)
    df_last_10_data = df_current_ticker.tail(10)
    df_last_5_data = df_current_ticker.tail(3)
    ma10 = df_last_data.iloc[0]["<MA10>"]
    ma30 = df_last_data.iloc[0]["<MA30>"]
    lastma10 = df_last_10_data.iloc[0]["<MA10>"]
    lastma30 = df_last_10_data.iloc[0]["<MA30>"]
    last5ma10 = df_last_5_data.iloc[0]["<MA10>"]
    last5ma30 = df_last_5_data.iloc[0]["<MA30>"]

    if(not math.isnan(ma10) and not math.isnan(ma30) and not math.isnan(lastma10) and not math.isnan(lastma30)):
        pct_ma30_diff = pct_diff(ma10,ma30)
        pct_last_ma30_diff = pct_diff(lastma10,lastma30)
        pct_last_5days_ma_diff = pct_diff(last5ma10,last5ma30)
        if pct_ma30_diff < 0.5 and pct_ma30_diff > 0 and pct_last_ma30_diff > 10:
        #if pct_last_5days_ma_diff > 0 and pct_last_5days_ma_diff < 1 and last5ma10 < last5ma30 and pct_last_ma30_diff > pct_last_5days_ma_diff:
            print('{} - diff {} - ma10 {} - ma30 {} last ma10 {}'.format(current_ticker,pct_ma30_diff,ma10,ma30,lastma10))




#om bokeh.plotting import figure, output_file, sh
#tput_file("line.html")    
#p = figure(plot_width=800, plot_height=400, x_axis_type="datetime")
#p.line(df_current_ticker["<tgl>"],df_current_ticker["<MA200>"],line_color="black",legend="MA200")
#p.line(df_current_ticker["<tgl>"],df_current_ticker["<MA100>"],line_color="green",legend="MA100")
#p.line(df_current_ticker["<tgl>"],df_current_ticker["<MA50>"],line_color="blue",legend="MA50")
#p.line(df_current_ticker["<tgl>"],df_current_ticker["<EMA8>"],line_color="red",legend="EMA8")

    
    
#show(p)
