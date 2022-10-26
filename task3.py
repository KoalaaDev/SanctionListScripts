from datetime import datetime
import scrapeutils
import dbutils

soup = scrapeutils.GetSoup("https://www.international.gc.ca/world-monde/assets/office_docs/international_relations-relations_internationales/sanctions/sema-lmes.xml","xml")
data = scrapeutils.ConvertDictXML(soup, "record")
conn = dbutils.connectDB("ITL-LTP-058\SQLEXPRESS", "SanctionList", "SA", "password1!")
const = {"DateGenerated":datetime.now().date(), "ImportedListName": "Canada Sanction List"}
dbutils.InsertDictArr(conn,"CASanctionsList",data, const)