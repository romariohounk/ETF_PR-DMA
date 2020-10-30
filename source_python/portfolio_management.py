import pandas as pd
from datetime import datetime
import urllib.request
import json
from numpy import array

from directory_utilities import get_json_from_file
from portfolio_metrics import PortfolioMetrics


class PortfolioManagement(object):
    """
    Used for managing portfolio
    """

    def __init__(self):

        # Average annual inflation in US divided by number of trading days since returns are computed daily
        risk_free_rate = 0.0167 / 365

        self.PortfolioMetrics = PortfolioMetrics(risk_free_rate)
        self.portfolio_file_directory = "../database/portfolio-data.json"
        self.portfolio_template = {
            "initial_capital": 0,
            "returns": [
            ]
        }

    def get_portfolio_return_to_date(self):
        """
        Used to get cumulative percentage returns for the entire portfolio up to this point.
        TBD
        """
        portfolio_content = get_json_from_file(self.portfolio_file_directory, self.portfolio_template)

        if portfolio_content == self.portfolio_template:
            print("No relevant portfolio data to get")
            return
        if len(portfolio_content["returns"]) < 1:
            print("No return data to get")
            return

        returns = portfolio_content["returns"]
        cumulative_return = 1
        for r in returns:
            cumulative_return *= (1 + (r["return"]))
        return_to_date = cumulative_return - 1
        return return_to_date

    def get_market_return_to_date(self):
        """
        Used to get cumulative percentage returns for the entire portfolio up to this point.
        TBD
        """
        portfolio_content = get_json_from_file(self.portfolio_file_directory, self.portfolio_template)

        if portfolio_content == self.portfolio_template:
            print("No relevant portfolio data to get")
            return
        if len(portfolio_content["returns"]) < 1:
            print("No return data to get")
            return

        returns = portfolio_content["returns"]
        cumulative_return = 1
        for r in returns:
            cumulative_return *= (1 + (r["market_return"]))
        return_to_date = cumulative_return - 1
        return return_to_date

    def get_last_day_return(self):
        """
        Used to get last day return.
        TBD
        """
        portfolio_content = get_json_from_file(self.portfolio_file_directory, self.portfolio_template)

        if portfolio_content == self.portfolio_template:
            print("No relevant portfolio data to get")
            return
        if len(portfolio_content["returns"]) < 1:
            print("No return data to get")
            return

        last_day_return = portfolio_content["returns"][-1]["return"]
        return last_day_return

    def get_initial_capital(self):
        """
        Used to get amount of cash with which investing has started.
        TBD
        """
        portfolio_content = get_json_from_file(self.portfolio_file_directory, self.portfolio_template)

        if portfolio_content == self.portfolio_template:
            print("No relevant portfolio data to get")
            return
        if len(portfolio_content["returns"]) < 1:
            print("No initial cash value to get")
            return

        initial_capital = portfolio_content["initial_capital"]
        return initial_capital

    def get_portfolio_metrics(self):
        """
        Used to get portfolio metrics reports.
        TBD
        """
        portfolio_content = get_json_from_file(self.portfolio_file_directory, self.portfolio_template)

        if portfolio_content == self.portfolio_template:
            print("No relevant portfolio data to get")
            return
        if len(portfolio_content["returns"]) < 1:
            print("No return data to get")
            return

        # Compute first part of data to get
        statistics_date = datetime.strptime(portfolio_content["returns"][-1]["date"], '%Y-%m-%d %H:%M:%S.%f')
        statistics_day = statistics_date.strftime('%d-%m-%Y')
        initial_capital = portfolio_content["initial_capital"]
        ending_capital = portfolio_content["returns"][-1]["usd_value"]
        net_profit = ending_capital - initial_capital
        net_profit_percentage = ((ending_capital / initial_capital) - 1) * 100
        market_return_percentage = self.get_market_return_to_date() * 100

        returns_data = portfolio_content["returns"]
        p_returns = []
        m_returns = []
        for r in returns_data:
            p_returns.append(r["return"])
            m_returns.append(r["market_return"])

        # Compute second part of data to get
        portfolio_returns = array(p_returns)
        market_returns = array(m_returns)

        average_daily_return, average_daily_volatility, max_drawdown, var_0_05, jensen_alpha, beta, sharpe_ratio,\
            treynor_ratio, information_ratio = self.PortfolioMetrics.get_risk_metrics(
            portfolio_returns, market_returns)
        average_daily_return_percentage = average_daily_return * 100
        average_daily_volatility_percentage = average_daily_volatility * 100
        return statistics_day, initial_capital, ending_capital, net_profit, net_profit_percentage, market_return_percentage, average_daily_return_percentage, average_daily_volatility_percentage, jensen_alpha, beta, sharpe_ratio, treynor_ratio, information_ratio

