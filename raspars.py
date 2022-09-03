# To run this, download the BeautifulSoup zip file
# http://www.py4e.com/code3/bs4.zip
# and unzip it in the same directory as this file

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re
import pandas as pd
import urllib.request
import sqlite3
import csv
import os.path
import codecs

def get_data():
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url_base = 'https://rosstat.gov.ru'
    url = 'https://rosstat.gov.ru/'
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    # Retrieve all of the anchor tags
    tags = soup('a')

    x = list()

    for tag in tags:  # .find_all('div', contents=None):

        http = str(tag.get('href', None))

        a = re.findall('statistic', http)

        if len(a) >= 1:

            if http not in x:
                x.append(http)
    ###########


    url = x[0]
    print(url)
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    # Retrieve all of the anchor tags
    tags = soup('a')

    x.clear()

    for tag in tags:  # .find_all('div', contents=None):
        http = str(tag.get('href', None))
        cont = str(('Contents:', tag))

        of = re.findall('Официальная статистика', cont)
        if len(of) >= 1:
            x.append(http)
    ##################


    url = x[0]
    print(url)
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    # Retrieve all of the anchor tags
    tags = soup('a')

    x.clear()

    for tag in tags:  # .find_all('div', contents=None):
        http = str(tag.get('href', None))
        cont = str(('Contents:', tag))

        of = re.findall('Цены', cont)
        if len(of) >= 1:
            x.append(http)
    #######################

    url = x[0]
    print(url)
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    # Retrieve all of the anchor tags
    tags = soup('a')

    x.clear()

    for tag in tags:  # .find_all('div', contents=None):
        file = (tag.get('href', None))
        excell = re.findall('.xls', str(tag))

        if len(excell) >= 1:
            x.append(file)

    df = pd.DataFrame(x)
    
    ######

    direct = str(url_base + x[1])

    print(direct)


    exc = pd.read_excel(direct)

    exc.to_csv('data.csv')
    #https://rosstat.gov.ru/storage/mediabank/IND-KIPC(1).xlsx


    # python3 raspars.py
    # https://rosstat.gov.ru/


def read_data():
    file_name = "data.csv"
    file = codecs.open(file_name, encoding = "utf-8", errors= "ignore")
    contents = csv.reader(file)
    return contents


def create_table():
    connection = sqlite3.connect('Prices.db')
    cursor = connection.cursor()
    create_table = '''CREATE TABLE IF NOT EXISTS Prices(
                        Zero int,
                        Product_code text,
                        Product_name text,
                        Index_2010 REAL,
                        Index_2011 REAL,
                        Index_2012 REAL,
                        Index_2013 REAL,
                        Index_2014 REAL,
                        Index_2015 REAL,
                        Index_2016 REAL,
                        Index_2017 REAL,
                        Index_2018 REAL,
                        Index_2019 REAL,
                        Index_2020 REAL,
                        Index_2021 REAL);
                    '''
    cursor.execute(create_table)
    connection.commit()
    connection.close()


def insert_data():
    connection = sqlite3.connect('Prices.db')
    cursor = connection.cursor()
    insert_records = "INSERT INTO Prices (Zero, Product_code, Product_name, Index_2010, Index_2011, Index_2012, Index_2013, Index_2014, Index_2015, Index_2016, Index_2017, Index_2018, Index_2019, Index_2020, Index_2021) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    contents = read_data()
    cursor.executemany(insert_records, contents)
    connection.commit()
    connection.close()


def main():
    get_data()
    create_table()
    insert_data()
    print("INFO: Prices database created!")
    print("Run extract.py to build reports")


if __name__ == "__main__":
  main()


#https://rosstat.gov.ru/storage/mediabank/IND-KIPC(1).xlsx


# python3 raspars.py
# https://rosstat.gov.ru/
