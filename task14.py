import dbutils
import scrapeutils
from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO,format='%(filename)s %(levelname)-8s %(message)s')
import pandas

df = pandas.read_csv('UK_Sanctions_List.csv', sep=',')
df['DateGenerated'] = datetime.now().date()
df['ImportedListName'] = 'Russia (Sanctions) (EU Exit) Regulations'
print(df)
from sqlalchemy.types import NVARCHAR
txt_cols = df.select_dtypes(include = ['object']).columns
conn = dbutils.connectAlchemy("ITL-LTP-058\SQLEXPRESS", "SanctionList", "SA", "password1!")
df.to_sql('UKSanctionsList', schema='dbo', con = conn, chunksize=200, method=None, index=False, if_exists='replace', dtype = {col_name: NVARCHAR for col_name in txt_cols})
