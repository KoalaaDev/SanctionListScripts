from typing import List
from bs4 import BeautifulSoup
import requests
import logging
import pandas

def GetSoup(URL: str, type="html.parser", is_downloaded=False):
    """Returns back soup object of the URL"""
    if is_downloaded:
        path = URL.split("/")[-1]
        with open(path, encoding="utf8") as f:
            soup = BeautifulSoup(f, features=type)
    else:
        file = requests.get(URL).content
        soup = BeautifulSoup(file, features=type)
    return soup

def GetPDF(URL: str, name="EU Sanction list"):
    """Downloads the pdf"""
    req = requests.get(URL)
    pdf = open(f"{name}"+".pdf", 'wb')
    pdf.write(req.content)
    pdf.close()
    logging.info("Downloaded PDF")

def ConvertDictXML(soup, seperator: str) -> List:
    """Converts a XML file to a list of dictionaries by a seperation tag"""
    records = soup.find_all(seperator)
    data = [{child.name: child.text for child in record.findChildren()} for record in records]
    return data

def ConvertArrayHTML(soup, seperator: str, html_tag = '') -> List:
    """Converts a HTML file to a list by a seperation tag"""
    records = soup.find_all(html_tag, class_=seperator)
    data = [record.text for record in records]
    return data

def DownloadXLS(URL: str, name="file"):
    """Downloads the xls"""
    req = requests.get(URL)
    xls = open(f"{name}"+".xls", 'wb')
    xls.write(req.content)
    xls.close()
    logging.info("Downloaded XLS")
def GetDataFrame(URL: str, type='csv'):
    """Returns back a dataframe object of the URL"""
    if type == 'csv':
        df = pandas.read_csv(URL, index_col=0)
    else:
        filename = URL.split("/")[-1]
        DownloadXLS(URL, name=filename)
        df = pandas.read_excel(filename, index_col=0)
    return df
