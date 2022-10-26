import dbutils
import scrapeutils
from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO,format='%(filename)s %(levelname)-8s %(message)s')
import pandas

df = pandas.read_excel('https://www.mfat.govt.nz/assets/Countries-and-Regions/Europe/Ukraine/Russia-Sanctions-Register.xlsx',skiprows=10)
df['DateGenerated'] = datetime.now().date()
df['ImportedListName'] = 'Russia Sanctions Register (New Zealand)'
df = df.dropna(axis=1, how='all', inplace=False)
print(df)
conn = dbutils.connectAlchemy("ITL-LTP-058\SQLEXPRESS", "SanctionList", "SA", "password1!")
df.to_sql('NZConsolidatedList', schema='dbo', con = conn, chunksize=200, method=None, index=False, if_exists='replace')
