import requests
from bs4 import BeautifulSoup as bs
import os
import os.path as osp
import time

data_bej = "http://www.dataharianbei.com"
localdir = "/usr/src/stock/data"

def write_file(localdir,filename,content):
    file_path = osp.join(localdir,filename)
    write_to = open(file_path,"wb")
    write_to.write(content)
    write_to.close()

req = requests.get(data_bej)
soup = bs(req.text,"html.parser")
downloaded_file = [ f for f in os.listdir(localdir) if osp.isfile(osp.join(localdir,f))]
for link in soup.find_all("a"):
    url = link.get("href")
    filename = str(link.string)
    if ".txt" in filename:
        if filename not in downloaded_file:
            print(time.strftime("%H:%M:%S") + '-' + filename)        
            r = requests.get(url)
            write_file(localdir,filename,r.content)
            time.sleep(5)
        
    

