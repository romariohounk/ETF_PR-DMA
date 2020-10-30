import os
import csv
import time
import json
import pandas as pd
from talib import abstract
from bs4 import BeautifulSoup
from slackclient import SlackClient
from configparser import SafeConfigParser
from urllib.request import Request, urlopen
pd.set_option('mode.chained_assignment', None) #https://www.dataquest.io/blog/settingwithcopywarning/
from directory_utilities import get_json_from_file, write_json_to_file, get_secrets

def get_OHLC_data(quote_page, csv_file):
    req = Request(quote_page, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'})
    #"""
    #print(csv_file)
    #"""
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')

    last_box = soup.find('span', attrs={'class':'quotation-last bd-streaming-select-value-last'})
    open_box = soup.find('span', attrs={'class':'bd-streaming-select-value-open'})
    high_box = soup.find('td', attrs={'class':'text-right bd-streaming-select-anim-high'})
    low_box = soup.find('td', attrs={'class':'text-right bd-streaming-select-anim-low'})
    close_box = soup.find('td', attrs={'class':'text-right bd-streaming-select-anim-close'})
    volume_box = soup.find('td', attrs={'class':'text-right bd-streaming-select-anim-cumulative-volume'})

    current_milli_time = int(round(time.time() * 1000))
    last_price = float(last_box.text.strip().replace(u'\xa0', u''))
    open_price = float(open_box.text.strip().replace(u'\xa0', u''))
    high_price = float(high_box.text.strip().replace(u'\xa0', u''))
    low_price = float(low_box.text.strip().replace(u'\xa0', u''))
    close_price = float(close_box.text.strip().replace(u'\xa0', u''))
    volume = float(volume_box.text.strip().replace(u'\xa0', u''))

    to_insert = [[current_milli_time, open_price, high_price, low_price, close_price, volume]]

    with open(os.path.expanduser(csv_file), "a") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(to_insert)

# Main

secrets = get_secrets()
etfs = secrets["ETFs"]

for etf in etfs:
    last_price = get_OHLC_data(etf["quote_page"], etf["csv_file"])

