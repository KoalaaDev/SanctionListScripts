import dbutils
import scrapeutils
from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO,format='%(filename)s %(levelname)-8s %(message)s')

soup = scrapeutils.GetSoup("https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32014R0833&from=EN")
date = soup.find("p", class_="hd-date").text
table = soup.find(id="L_2014229EN.01001101")
names = table.find_all("p",class_="normal")
namelist =[name.text for name in names if len(name.text)>2]
datec = datetime.strptime(date, "%d.%m.%Y ").date()


#putting the scraped data into the db
conn = dbutils.connectDB("ITL-LTP-058\SQLEXPRESS", "SanctionList", "SA", "password1!")
dbutils.InsertData(conn, "EUSanctionList", datec, namelist)
