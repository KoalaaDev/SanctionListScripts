import scrapeutils
import dbutils
from datetime import datetime
import logging
logging.basicConfig(level=logging.DEBUG,format='%(filename)s %(levelname)-8s %(message)s')

soup = scrapeutils.GetSoup("https://scsanctions.un.org/resources/xml/en/consolidated.xml","xml")
data_individual = scrapeutils.ConvertDictXML(soup, "INDIVIDUAL")
data_entity = scrapeutils.ConvertDictXML(soup, "ENTITY")
conn = dbutils.connectDB("ITL-LTP-058\SQLEXPRESS", "SanctionList", "SA", "password1!")
date = soup.find("CONSOLIDATED_LIST")['dateGenerated']
datec = datetime.strptime(date.split('T')[0], "%Y-%m-%d").date()
const_individual = {"DateGenerated":datec, "ImportedListName": "UN Consolidated List", "Type": "Individual"}
const_entity = {"DateGenerated":datec, "ImportedListName": "UN Consolidated List", "Type": "Entity"}


dbutils.InsertDictArr(conn,"UNConsolidatedList",data_individual, const_individual)
dbutils.InsertDictArr(conn,"UNConsolidatedList",data_entity, const_entity, datec, False)