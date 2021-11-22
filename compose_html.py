import pandas as pd
import os.path as osp
import os
import datetime

localdir = "/usr/src/stock/"
#create html 
df_buy_target = pd.read_csv(osp.join(localdir,"buy_result.txt"))
f_html = open(osp.join(localdir,"buy_stock.html"),"w")
f_html.write("<html>")
f_html.write("<head>")
f_html.write('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">')
f_html.write('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>')
f_html.write("</head>")
f_html.write("<body>")
f_html.write("<div class='col-md-4'>")
f_html.write("<table class='table table-striped table-dark'>")
f_html.write("<thead>")
f_html.write("<tr>")
f_html.write("<th scope='col'>Date</th>")
f_html.write("<th scope='col'>Ticker</th>")
f_html.write("<th scope='col'>Close</th>")
f_html.write("<th scope='col'>Target</th>")
f_html.write("<th scope='col'>Pct</th>")
f_html.write("</tr>")
f_html.write("</thead>")


for index,row in df_buy_target.iterrows():    
  row_class = "table_info"
  if(row['status'] == 1 ):
    row_class = "bg-success"

  f_html.write("<tr class='{}'>".format(row_class))
  f_html.write("<td>{}</td>".format(row['refdate']))
  f_html.write("<td>{}</td>".format(row['ticker']))
  f_html.write("<td>{}</td>".format(row['close']))
  f_html.write("<td>{}</td>".format(row['target']))
  f_html.write("<td>{}</td>".format(row['pct']))
  f_html.write("</tr>")

f_html.write("</table>")
f_html.write("</div>")
f_html.write("<div class='col-md-8'>")
f_html.write("</div>")
f_html.write("<div class='row'>")
f_html.write("<div class='col-md-12'>")
now = datetime.datetime.now()
f_html.write(now.strftime('%H:%M:%S on %A, %B the %dth, %Y'))
f_html.write("</div>")
f_html.write("</div>")
f_html.write("</body>")
f_html.write("</html>")
f_html.close()