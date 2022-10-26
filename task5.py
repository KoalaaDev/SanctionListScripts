from datetime import datetime
import scrapeutils
import dbutils

soup = scrapeutils.GetSoup("https://ofsistorage.blob.core.windows.net/publishlive/2022format/ConList.xml","xml")
data = scrapeutils.ConvertDictXML(soup, "FinancialSanctionsTarget")
conn = dbutils.connectDB("ITL-LTP-058\SQLEXPRESS", "SanctionList", "SA", "password1!")
const = {"DateGenerated":datetime.now().date(), "ImportedListName": "Uk Asset Freeze List"}
dbutils.InsertDictArr(conn,"UKAssetFreezeList",data, const)
# conn = dbutils.connectDB("ITL-LTP-058\SQLEXPRESS", "SanctionList", "SA", "password1!")
# conn.cursor().execute(sql)
# dbutils.InsertDictArr(conn,"CASanctionsList",data, const)