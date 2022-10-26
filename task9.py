import dbutils
import scrapeutils
from datetime import datetime
import logging
logging.basicConfig(level=logging.DEBUG,format='%(filename)s %(levelname)-8s %(message)s')

soup = scrapeutils.GetSoup("https://www.treasury.gov/ofac/downloads/sdn.xml","xml")
data = scrapeutils.ConvertDictXML(soup, "sdnEntry")
conn = dbutils.connectDB("ITL-LTP-058\SQLEXPRESS", "SanctionList", "SA", "password1!")
date = soup.find("Publish_Date").text
datec = datetime.strptime(date, "%m/%d/%Y").date()
const = {"DateGenerated":datec, "ImportedListName": "US Treasury List"}
try:
    dbutils.InsertDictArr(conn,"USTreasuryList",data, const)
except Exception as e:
    logging.error(e)
    dbutils.generateCreateTable("USTreasuryList", data)