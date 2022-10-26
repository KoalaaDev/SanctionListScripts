import pyodbc
import logging
from datetime import datetime
from itertools import chain
from sqlalchemy import create_engine
import urllib

def connectDB(server_name: str, database_name: str, userID: str, password: str):
    """Connects to the Database"""
    connStr = "DRIVER={ODBC Driver 18 for SQL Server};"+f"SERVER={server_name};" \
        + f"DATABASE={database_name};UID={userID};PWD={password};Encrypt=no;"
    conn = pyodbc.connect(connStr)
    return conn
def connectAlchemy(server_name: str, database_name: str, userID: str, password: str):
    """Connects to the Database"""
    
    connStr = "DRIVER={ODBC Driver 18 for SQL Server};"+f"SERVER={server_name};" \
        + f"DATABASE={database_name};UID={userID};PWD={password};Encrypt=no;"
    quoted = urllib.parse.quote_plus(connStr)
    engine = create_engine('mssql+pyodbc:///?odbc_connect={}?charset=utf8'.format(quoted), encoding="utf8")
    return engine

def InsertData(conn, table: str, datec: datetime, namelist: str, const_values=[], CheckDuplicate = True):
    """Inserts Data to a table provided the name list, date generated"""
    cursor = conn.cursor()
    cursor.execute(f"SELECT DateGenerated FROM {table}")
    checkEmpty = cursor.fetchone()
    cursor.execute(f"SELECT DateGenerated FROM {table} WHERE DateGenerated != ?", datec)
    rows = cursor.fetchone()
    datenow = datetime.now().date()
    placeholders = '?, ?, ?,'
    placeholders += ', '.join(['?'] * len(const_values))
    if not checkEmpty:
        logging.info("Table empty, Filling data")
        for name in namelist:
            logging.debug(f"Adding {name}...")
            cursor.execute(f"INSERT INTO {table} VALUES ({placeholders})", datec, name, datenow, *const_values)
            cursor.commit()
    elif rows or not CheckDuplicate:
        logging.info("Found changes to date generated, Filling data")
        for name in namelist:
            logging.debug(f"Adding {name}...")
            cursor.execute(f"INSERT INTO {table} VALUES ({placeholders})", datec, name, datenow, *const_values)
            cursor.commit()
    else:
        logging.info("No changes found")

def InsertDictArr(conn, table: str, data_arr, const_dict={}, datec=datetime.now().date(), CheckDuplicate = True):
    """Inserts an array of dictionaries into a table"""
    cursor = conn.cursor()
    cursor.execute(f"SELECT DateGenerated FROM {table}")
    checkEmpty = cursor.fetchone()
    cursor.execute(f"SELECT DateGenerated FROM {table} WHERE DateGenerated != ?", datec)
    rows = cursor.fetchone()
    

    if not checkEmpty:
        logging.info("Table empty, Filling data")
        for mydict in data_arr:
            placeholders = ', '.join(['?'] * (len(mydict)+len(const_dict)))
            columns = ', '.join(list(mydict.keys())+list(const_dict.keys()))
            sql = "INSERT INTO %s ( %s) VALUES ( %s)" % (table, columns, placeholders)
            logging.debug(sql)
            cursor.execute(sql, *mydict.values(), *const_dict.values())
            cursor.commit()
    elif rows or not CheckDuplicate:
        logging.info("Found changes to date generated, Filling data")
        for mydict in data_arr:
            placeholders = ', '.join(['?'] * (len(mydict)+len(const_dict)))
            columns = ', '.join(list(mydict.keys())+list(const_dict.keys()))
            sql = "INSERT INTO %s ( %s) VALUES ( %s)" % (table, columns, placeholders)
            logging.debug(sql)
            cursor.execute(sql, *mydict.values(), *const_dict.values())
            cursor.commit()
    else:
        logging.info("No changes found")

def generateCreateTable(table: str, arr):
    """Generates a create table statement based on the array of dictionaries"""
    if not arr:
        logging.error("Array is empty")
        return
    # longest_val = roundup(max(len(max(i.values(), key=len)) for i in arr))#prevents that annoying DB error :(
    # if longest_val > 4000:
    #     logging.warn("Longest value is greater than 4000, truncating to 4000")
    #     truncateValues(arr, 4000)
    #     longest_val = 4000
    sql = "CREATE TABLE " + f"{table}("
    sql = sql + f" [nvarchar](500) NULL,".join(list(set(chain.from_iterable(sub.keys() for sub in arr)))) + "[nvarchar](500) NULL, \
[DateGenerated] [Date] NULL, [ImportedListName] [nvarchar](500) NULL)"
    text_file = open("Output.txt", "w")
    print(sql, file=text_file)

def truncateValues(arr, length):
    """Truncates the values of the array to the length provided"""
    for i in arr:
        for key, value in i.items():
            if len(value) > length:
                i[key] = value[:length]
    return arr

def roundup(x):
    """Rounds up to the nearest 100"""
    return int(math.ceil(x / 100.0)) * 100
