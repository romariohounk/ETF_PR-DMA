import json
import time
import urllib.request
from datetime import datetime

import pydash as py_

from directory_utilities import get_json_from_file, write_json_to_file


class Database(object):
    """
    Used to store all relevant data
    """

    instance = None

    def __new__(cls):
        if not Database.instance:
            Database.instance = Database.__Database()
        return Database.instance

    class __Database:
        def __init__(self):
            self.default_portfolio_data = {"initial_capital": 0, "returns": []}
            self.portfolio_data_file_string = "../database/portfolio-data.json"

        # Methodes pour ecrire dans portfolio-data.json
        def store_initial_portfolio(self, portfolio_value):
            """
            Used to initiate portfolio data file
            :TBD
            """
            portfolio_data = get_json_from_file(self.portfolio_data_file_string, self.default_portfolio_data)
            portfolio_data["initial_capital"] = portfolio_value

            write_json_to_file(self.portfolio_data_file_string, portfolio_data)

        def store_second_portfolio(self, portfolio_value, market_return):
            """
            Used to initiate portfolio data file
            :TBD
            """
            portfolio_data = get_json_from_file(self.portfolio_data_file_string, self.default_portfolio_data)

            return_object = {
                "date": datetime.now(),
                "portfolio_value": portfolio_value,
                "portfolio_return": ((portfolio_value / portfolio_data["initial_capital"]) - 1),
                "market_return": market_return
            }
            portfolio_data["returns"].append(return_object)

            write_json_to_file(self.portfolio_data_file_string, portfolio_data)

        def update_returns(self, portfolio_value, market_return):
            """
            Used to update returns
            :TBD
            """
            portfolio_data = get_json_from_file(self.portfolio_data_file_string, self.default_portfolio_data)
            if len(portfolio_data["returns"]) < 1:
                if portfolio_data["initial_capital"] == 0:
                    self.store_initial_portfolio(portfolio_value)
                    return
                else:
                    self.store_second_portfolio(portfolio_value, market_return)
                    return
            previous_portfolio_value = portfolio_data["returns"][-1]["portfolio_value"]

            return_object = {
                "date": datetime.now(),
                "portfolio_value": portfolio_value,
                "portfolio_return": ((portfolio_value / previous_portfolio_value) - 1),
                "market_return": market_return
            }
            portfolio_data["returns"].append(return_object)

            write_json_to_file(self.portfolio_data_file_string, portfolio_data)

