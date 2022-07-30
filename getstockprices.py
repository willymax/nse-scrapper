import requests
from bs4 import BeautifulSoup
import pandas
import datetime
import os
import urllib

from dotenv import load_dotenv

load_dotenv()

weekno = datetime.datetime.today().weekday()

is_weekday = False
if weekno < 5:
    is_weekday = True
else:  # 5 Sat, 6 Sun
    is_weekday = False


def get_database():
    from pymongo import MongoClient
    import pymongo

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = os.environ.get('MONGO_DB_URL')
    MONGO_USER = os.environ.get('MONGO_USER')
    MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
    mongo_uri = "mongodb://" + MONGO_USER + ":" + \
        urllib.quote("" + MONGO_PASSWORD + "") + "@127.0.0.1:27001/"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['stock_prices']


def getData(stock_symbol):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'}
    url = f'https://live.mystocks.co.ke/stock={stock_symbol}'
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, 'html.parser')
    # Open,High,Low,Close,Adj Close,Volume
    stock = {
        'Date': datetime.date.today(),
        'Open': soup.find('b', {'id': 'rtPrev'}).text,
        'High': soup.find('b', {'id': 'rtHi'}).text,
        'Low': soup.find('b', {'id': 'rtLo'}).text,
        'Close': soup.find('b', {'id': 'rtPrice2'}).text,
        'Volume': soup.find('b', {'id': 'rtVol'}).text,
    }
    return stock


if is_weekday == False:
    # Get the database
    dbname = get_database()
    collection_name = dbname["stock_prices"]
    theData = []
    with open('symbols.csv') as f:
        lines = f.read().splitlines()
        for symbol in lines:
            print(symbol)
            # data = pandas.DataFrame.from_dict(getData(symbol))
            theData.append(getData(symbol))
            # if os.path.isfile("datasets/{}.csv".format(symbol)):
            #     data.to_csv("datasets/{}.csv".format(symbol), mode='a', header=False, index=False)
            # else:
            #     data.to_csv("datasets/{}.csv".format(symbol), mode='a', header=True, index=False)
            # data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        collection_name.insert_many(theData)
        print('Done')
