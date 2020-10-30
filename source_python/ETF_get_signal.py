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
from portfolio_management import PortfolioManagement
from database import Database
from messenger import Messenger
from directory_chains_utilities import get_json_from_file, write_json_to_file, get_secrets, make_slack_etf_chain, make_slack_etf_chain_total

CURRENCY = "euros"

def get_market_return(quote_page):
    req = Request(quote_page, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'})

    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')

    last_box = soup.find('span', attrs={'class':'variation'})
    
    market_return = round((float(last_box.text.strip().replace(u'\xa0', u'').split()[0]) / 100), 5)

    return market_return

def get_cash_report(cash_position):
    """"TBD"""
    currency = CURRENCY
    slack_str = "*" + "Boursorama Cash Position" + "*\n>>>\n"
    slack_str = slack_str + make_slack_etf_chain_total(cash_position, currency)
    """
    sendSlackNotification('etf', slack_str, "ETF Notification", ':chart_with_upwards_trend:')
    """
    return slack_str, round(cash_position, 2)


def get_total_value_report(total_value):
    """"TBD"""
    # Total value report
    currency = CURRENCY
    slack_str = "*" + "Total value report" + "*\n>>>\n"
    slack_str = slack_str + make_slack_etf_chain_total(total_value, currency)
    """
    sendSlackNotification('etf', slack_str, "ETF Notification", ':chart_with_upwards_trend:')
    """
    return total_value


def get_last_price(quote_page):
    req = Request(quote_page, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'})

    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')

    last_box = soup.find('span', attrs={'class':'quotation-last bd-streaming-select-value-last'})

    last_price = float(last_box.text.strip().replace(u'\xa0', u''))

    return last_price

def get_signal_from_TA(etf_id, csv_file, last_price, number):
    data = pd.read_csv(csv_file, parse_dates=True, sep=',', header=0, encoding='ascii')
    data['time'] = pd.to_datetime(data['time'],unit='ms')
    data.set_index('time', inplace=True, drop=True)

    close_values = data['close']
    adx_values = abstract.ADX(data, 14)
    rsi_values = abstract.RSI(data, 50)
    stochs_values = abstract.STOCH(data, 50, 3, 0, 3, 0).iloc[:, 0]
    cci_values = abstract.CCI(data, 50)

    data['adx_values'] = adx_values
    data['rsi_values'] = rsi_values
    data['stochs_values'] = stochs_values
    data['cci_values'] = cci_values

    signal = ["No data"]

    for i in range(1, len(adx_values)):
        if rsi_values[i] <= 40 and stochs_values[i] <= 20 and cci_values[i]<=-100:
            signal.append("BUY")
        elif rsi_values[i] >= 60 and stochs_values[i] >= 80 and cci_values[i]>=100:
            signal.append("SELL")
        else:
            signal.append("HOLD")

    slack_str = "*" + etf_id + make_slack_etf_chain(last_price, number, close_values[-1], adx_values[-1], rsi_values[-1], stochs_values[-1], cci_values[-1], signal[-1])
    
    currency = CURRENCY
    slack_str = slack_str + make_slack_etf_chain_total(last_price * number, currency)
    """
    sendSlackNotification('etf', slack_str, "ETF Notification", ':chart_with_upwards_trend:')
    print ("Slack Notification sent for " + etf_id)
    """
    return slack_str, round(last_price * number, 2)

# Main

PortfolioManagement = PortfolioManagement()
Database = Database()
Messenger = Messenger()

total_value = 0

secrets = get_secrets()
etfs = secrets["ETFs"]
cash_position = secrets["cash"]["cash_position"]
market_return_link = secrets["market"]["market_return_link"]

for etf in etfs:
    last_price = get_last_price(etf["quote_page"])
    etf_report, etf_value = get_signal_from_TA(etf["id"], etf["csv_file"], last_price, etf["number"])
    Messenger.send_slack(etf_report)
    total_value = total_value + etf_value

cash_report, cash_value = get_cash_report(cash_position)
Messenger.send_slack(cash_report)

total_value = total_value + cash_value
Messenger.send_capital_report_slack(round(total_value, 2))

market_return = get_market_return(market_return_link)

Database.update_returns(total_value, market_return)
portfolio_metrics = PortfolioManagement.get_portfolio_metrics()
Messenger.print_portfolio_report(portfolio_metrics)
Messenger.send_portfolio_reporting_slack(portfolio_metrics)

