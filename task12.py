import dbutils
import scrapeutils
from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO,format='%(filename)s %(levelname)-8s %(message)s')
import pandas

df = pandas.read_csv('20221024-FULL-1_1.csv', sep=';')
df['DateGenerated'] = datetime.now().date()
df['ImportedListName'] = 'EU Asset-Freeze List'
print(df)
from sqlalchemy.types import NVARCHAR
txt_cols = df.select_dtypes(include = ['object']).columns
conn = dbutils.connectAlchemy("ITL-LTP-058\SQLEXPRESS", "SanctionList", "SA", "password1!")
df.to_sql('EUAssetFreezeList', schema='dbo', con = conn, chunksize=200, method=None, index=False, if_exists='replace', dtype = {col_name: NVARCHAR for col_name in txt_cols})
