from datetime import datetime
import scrapeutils
import dbutils

soup = scrapeutils.GetSoup("https://gels-avoirs.dgtresor.gouv.fr/ApiPublic/api/v1/publication/derniere-publication-fichier-xml","xml")
data = scrapeutils.ConvertDictXML(soup, "PublicationDetail")
# dbutils.generateCreateTable("FRFreezeRegistry", data)
conn = dbutils.connectDB("ITL-LTP-058\SQLEXPRESS", "SanctionList", "SA", "password1!")
const = {"DateGenerated":datetime.now().date(), "ImportedListName": "France Freeze Registry"}
data = dbutils.truncateValues(data, 4000)
dbutils.InsertDictArr(conn,"FRFreezeRegistry",data, const)