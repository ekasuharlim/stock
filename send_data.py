import os.path as osp
import ftplib

host = "ftp.properti-info.com"
user = "stockpi@properti-info.com"
ktkun = "Bm(czz^^f7E^"

with ftplib.FTP(host) as ftp:
    ftp.login(user,ktkun)    
    localdir = "/usr/src/stock/"    
    with open(osp.join(localdir,"buy_stock.html"),"rb") as file_object:
        ftp.storbinary("STOR index.html",file_object)
    ftp.dir()
    print("Done")

