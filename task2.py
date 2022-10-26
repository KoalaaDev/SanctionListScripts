import dbutils
import scrapeutils
from datetime import datetime
import locale
import logging
logging.basicConfig(level=logging.INFO,format='%(filename)s %(levelname)-8s %(message)s')
locale.setlocale(locale.LC_TIME,"nb_NO")

soup = scrapeutils.GetSoup("https://lovdata.no/dokument/SF/forskrift/2014-08-15-1076/*#KAPITTEL_19")
def scrape(id):
    """Scrapes the info based on the fact that the ids are ordered"""
    vedlegg = soup.find(id=f"KAPITTEL_{id}")
    date = vedlegg.find(class_="reference").text.split("nr.")[0]
    datec = datetime.strptime(date, "%d %B %Y ").date()
    vedlegg_list = [x.text for x in vedlegg.find_all(class_="morTableVerticalAlignTop morTableAlignLeft")]
    return vedlegg_list, datec

vedlegg1, dategen1 = scrape(19)
vedlegg2, dategen2 = scrape(20)
vedlegg3, dategen3 = scrape(21)
vedlegg3_wdates = [(vedlegg3[i],vedlegg3[i+1]) for i in range(0,len(vedlegg3),2)]
vedlegg3_names = [x[0] for x in vedlegg3_wdates]

#database input
conn = dbutils.connectDB("ITL-LTP-058\SQLEXPRESS", "SanctionList", "SA", "password1!")
dbutils.InsertData(conn, "NorwaySanctionList", dategen1, vedlegg1+vedlegg2+vedlegg3_names)