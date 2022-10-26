import dbutils
import scrapeutils
from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO,format='%(filename)s %(levelname)-8s %(message)s')
arr = []
for x in range(4,7):
    if x == 4:
        soup = scrapeutils.GetSoup(f"https://laws.justice.gc.ca/eng/regulations/sor-2014-58/page-{x}.html")
        namelist = scrapeutils.ConvertArrayHTML(soup, "listItemText4", "div")
        date = soup.find("time", property="dateModified").text
        conn = dbutils.connectDB("ITL-LTP-058\SQLEXPRESS", "SanctionList", "SA", "password1!")
        datec = datetime.strptime(date, "%Y-%m-%d").date()
        dbutils.InsertData(conn, "CASpecialMeasuresList", datec, namelist, ["Canada Special Measures List", 'Individual'])
    else:
        soup = scrapeutils.GetSoup(f"https://laws.justice.gc.ca/eng/regulations/sor-2014-58/page-{x}.html")
        namelist = scrapeutils.ConvertArrayHTML(soup, "listItemText2", "div")
        arr = arr + namelist
dbutils.InsertData(conn, "CASpecialMeasuresList", datec, namelist, ["Canada Special Measures List", 'Entities'], False)

