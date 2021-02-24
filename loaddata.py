import pandas as pd
import os.path as osp
import os

def load_daily_data(datadir,filename,dt_all_data):
    new_data = pd.read_csv(osp.join(datadir,filename)) 
    return pd.concat([dt_all_data,new_data],ignore_index = True)

localdir = "C:\Eka\stock\data"
localdir_result = "C:\\Eka\\stock\\result"

dt_all_data = pd.DataFrame()
downloaded_file = [ f for f in os.listdir(localdir) if osp.isfile(osp.join(localdir,f))]
for daily_file in downloaded_file:
    print(daily_file)
    dt_all_data = load_daily_data(localdir,daily_file,dt_all_data)    

dt_all_data.to_csv(osp.join(localdir_result,"alldata.csv"))
