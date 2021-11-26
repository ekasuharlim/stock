import pandas as pd
import os.path as osp
import os
import talib
import math

from datetime import datetime
from colorama import Fore

def calculate_ma(df_ticker_data):
    df_ticker_data = df_ticker_data.sort_values(by="<tgl>",ascending=False)
    df_ticker_data = df_ticker_data[["<open>","<close>","<high>","<low>","<volume>","<ticker>","<tgl>"]]
    df_ticker_data["<MA100>"]  = talib.SMA(df_ticker_data["<close>"],100)
    df_ticker_data["<MA200>"]  = talib.SMA(df_ticker_data["<close>"],200)
    df_ticker_data["<MA30>"]  = talib.SMA(df_ticker_data["<close>"],30)
    df_ticker_data["<MA10>"]  = talib.SMA(df_ticker_data["<close>"],10)
    df_ticker_data["<EMA8>"]  = talib.EMA(df_ticker_data["<close>"],8)
    return df_ticker_data

def pct_diff(a,b):
    return (abs(a-b) / ((a + b) / 2)) * 100 

localdir = "/usr/src/stock/"
df_all_data = pd.read_csv(osp.join(localdir,"result/alldata.csv"))
f_ma_result = open(osp.join(localdir,"ma_result.txt"),"w")
f_ma_result.write('current_ticker,pct_ma30_diff,ma10,ma30,last10ma10,price\n')
df_all_data["<tgl>"] = pd.to_datetime(df_all_data["<date>"])

all_ticker = df_all_data["<ticker>"].drop_duplicates().sort_values()
for current_ticker in all_ticker:
    df_current_ticker = df_all_data[df_all_data["<ticker>"] == current_ticker]
    df_current_ticker = calculate_ma(df_current_ticker)
    df_last_data = df_current_ticker.tail(1)
    df_last_10_data = df_current_ticker.tail(10)
    df_last_5_data = df_current_ticker.tail(5)
    price  = df_last_data.iloc[0]["<close>"]
    ma10 = df_last_data.iloc[0]["<MA10>"]
    ma30 = df_last_data.iloc[0]["<MA30>"]
    last10ma10 = df_last_10_data.iloc[0]["<MA10>"]
    last10ma30 = df_last_10_data.iloc[0]["<MA30>"]
    last5ma10 = df_last_5_data.iloc[0]["<MA10>"]
    last5ma30 = df_last_5_data.iloc[0]["<MA30>"]

    if(not math.isnan(ma10) and not math.isnan(ma30) and not math.isnan(last10ma10) and not math.isnan(last10ma30)):
        pct_ma30_diff = pct_diff(ma10,ma30)
        pct_last_ma30_diff = pct_diff(last10ma10,last10ma30)
        pct_last_5days_ma_diff = pct_diff(last5ma10,last5ma30)
        if pct_ma30_diff < 0.5 and pct_ma30_diff > 0 and pct_last_ma30_diff > 10:
        #if pct_last_5days_ma_diff > 0 and pct_last_5days_ma_diff < 1 and last5ma10 < last5ma30 and pct_last_ma30_diff > pct_last_5days_ma_diff:
            print('{} - diff {} - ma10 {} - ma30 {} last 10 ma10 {} price {}'.format(current_ticker,pct_ma30_diff,ma10,ma30,last10ma10,price))
            f_ma_result.write('{},{:.4f},{:.2f},{:.2f},{:.2f},{:.0f}\n'.format(current_ticker,pct_ma30_diff,ma10,ma30,last10ma10,price))
f_ma_result.close()
print('---------------------------------------------------------------------')
df_target = pd.read_csv(osp.join(localdir,"targetbuy.txt"))
all_target = df_target["ticker"].sort_values()
f_buy_result = open(osp.join(localdir,"buy_result.txt"),"w")
f_buy_result.write('refdate,ticker,close,target,pct,status\n')
for target_ticker in all_target:    
    df_current_ticker = df_all_data[df_all_data["<ticker>"] == target_ticker]
    df_last_data = df_current_ticker.tail(1)
    ref_date = df_last_data.iloc[0]["<date>"]
    df_target_data = df_target[df_target["ticker"] == target_ticker]
    close_price = df_last_data.iloc[0]["<close>"]
    target_buy_price = df_target_data.iloc[0]["buy"]
    pct_target_buy = pct_diff(close_price,target_buy_price)
    if pct_target_buy <= 5: 
       f_buy_result.write('{},{},{:.0f},{:.0f},{:.2f},1\n'.format(ref_date,target_ticker,close_price,target_buy_price,pct_target_buy))
       print(Fore.GREEN + '{}-{}-close-{}-target-{}-pct-{:.2f}'.format(ref_date,target_ticker,close_price,target_buy_price,pct_target_buy))
    else:
       f_buy_result.write('{},{},{:.0f},{:.0f},{:.2f},0\n'.format(ref_date,target_ticker,close_price,target_buy_price,pct_target_buy))
       print(Fore.WHITE + '{}-{}-close-{}-target-{}-pct-{:.2f}'.format(ref_date,target_ticker,close_price,target_buy_price,pct_target_buy))
f_buy_result.close()
print(Fore.WHITE + 'Done')
print('---------------------------------------------------------------------')
f_sell_result = open(osp.join(localdir,"sell_result.txt"),"w")
f_sell_result.write('refdate,ticker,close,target,pct,status\n')
df_target = pd.read_csv(osp.join(localdir,"targetsell.txt"))
all_target = df_target["ticker"].sort_values()
for target_ticker in all_target:    
    df_current_ticker = df_all_data[df_all_data["<ticker>"] == target_ticker]
    df_last_data = df_current_ticker.tail(1)
    df_target_data = df_target[df_target["ticker"] == target_ticker]
    close_price = df_last_data.iloc[0]["<close>"]
    target_sell_price = df_target_data.iloc[0]["sell"]
    pct_target_sell = pct_diff(close_price,target_sell_price)
    if pct_target_sell <= 5: 
       f_sell_result.write('{},{},{:.0f},{:.0f},{:.2f},1\n'.format(ref_date,target_ticker,close_price,target_sell_price,pct_target_sell))
       print(Fore.RED + '{}-close-{}-target-{}-pct-{:.2f}'.format(target_ticker,close_price,target_sell_price,pct_target_sell))
    else:
       f_sell_result.write('{},{},{:.0f},{:.0f},{:.2f},0\n'.format(ref_date,target_ticker,close_price,target_sell_price,pct_target_sell))
       print(Fore.WHITE + '{}-close-{}-target-{}-pct-{:.2f}'.format(target_ticker,close_price,target_buy_price,pct_target_buy))
print(Fore.WHITE + 'Done')
f_sell_result.close()



#om bokeh.plotting import figure, output_file, sh
#tput_file("line.html")    
#p = figure(plot_width=800, plot_height=400, x_axis_type="datetime")
#p.line(df_current_ticker["<tgl>"],df_current_ticker["<MA200>"],line_color="black",legend="MA200")
#p.line(df_current_ticker["<tgl>"],df_current_ticker["<MA100>"],line_color="green",legend="MA100")
#p.line(df_current_ticker["<tgl>"],df_current_ticker["<MA50>"],line_color="blue",legend="MA50")
#p.line(df_current_ticker["<tgl>"],df_current_ticker["<EMA8>"],line_color="red",legend="EMA8")

    
    
#show(p)
