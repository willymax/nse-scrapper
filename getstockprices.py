import requests
from bs4 import BeautifulSoup
import pandas
import datetime
import os

weekno = datetime.datetime.today().weekday()

is_weekday = False
if weekno < 5:
    is_weekday = True
else:  # 5 Sat, 6 Sun
    is_weekday = False


def getData(stock_symbol):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'}
    url = f'https://live.mystocks.co.ke/stock={stock_symbol}'
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, 'html.parser')
    # Open,High,Low,Close,Adj Close,Volume
    stock = {
        'Date': [datetime.date.today()],
        'Open': [soup.find('b', {'id': 'rtPrev'}).text],
        'High': [soup.find('b', {'id': 'rtHi'}).text],
        'Low': [soup.find('b', {'id': 'rtLo'}).text],
        'Close': [soup.find('b', {'id': 'rtPrice2'}).text],
        'Volume': [soup.find('b', {'id': 'rtVol'}).text],
    }
    return stock


if is_weekday:
    with open('symbols.csv') as f:
        lines = f.read().splitlines()
        for symbol in lines:
            print(symbol)
            data = pandas.DataFrame.from_dict(getData(symbol))
            if os.path.isfile("datasets/{}.csv".format(symbol)):
                data.to_csv("datasets/{}.csv".format(symbol), mode='a', header=False, index=False)
            else:
                data.to_csv("datasets/{}.csv".format(symbol), mode='a', header=True, index=False)
            data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
