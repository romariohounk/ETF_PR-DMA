import time

from slackclient import SlackClient

from directory_utilities import get_json_from_file, write_json_to_file, get_secrets

class Messenger(object):
    """
    Used for handling messaging functionality
    """

    def __init__(self):

        secrets = get_secrets()
        
        self.slack_channel = secrets["slack"]["channel"]
        self.slack_client = SlackClient(secrets["slack"]["token"])
        self.username = "Crypto Notification"
        self.slack_icon_emoji = ':chart_with_upwards_trend:'

        self.slack_no_stats = "*Portfolio data reset*\n"
        
        self.no_stats = "Portfolio data reset\n"

        self.slack_portfolio_report_str = "*Statistics as of : {}*\n>>>\n_*General information:*_\n_Initial capital : *{} euros*_\n_Ending capital : *{} euros*_\n_Net Profit : *{}*_\n_Net Profit %: *{}%*_\n_Market (CAC 40) return : *{}%*_\n_Average daily return : *{}%*_\n_Average daily volatility : *{}%*_\n\n_*Metrics based CAPM method :*_\n_Jensen's Alpha (outperforming the market) : *{}*_\n_Beta (exposure to the market) : *{}*_\n\n_*Risk-adjusted return based on volatility :*_\n_Sharpe ratio: *{}*_\n_Treynor ratio : *{}*_\n_Information ratio : *{}*_\n"

        self.portfolio_report_str = "Statistics as of : {}\n\nGeneral information :\nInitial capital : {}\nEnding capital : {}\nNet Profit : {}\nNet Profit % : {}%\nMarket (CAC40) return % : {}%\nAverage daily return : {}%\nAverage daily volatility : {}%\n\nMetrics based CAPM method :\nJensen's Alpha (outperforming the market) : {}\nBeta (exposure to the market) : {}\n\nRisk-adjusted return based on volatility :\nSharpe ratio : {}\nTreynor ratio : {}\nInformation ratio: {}\n"

        self.slack_capital_report_str = "*Capital report*\n>>>\n_AUM : *{} euros*_\n"


    def send_slack(self, message):
        """
        Send slack message to notify users
        """
        self.slack_client.api_call('chat.postMessage', channel=self.slack_channel, text=message, username=self.username, icon_emoji=self.slack_icon_emoji)
        print("Slack Notification sent")


    def send_capital_report_slack(self, portfolio_value):
        """
        Used to send a alive alert Slack message
        """
        slack_message = self.slack_capital_report_str.format(portfolio_value)
        self.send_slack(slack_message)

    def send_portfolio_reporting_slack(self, portfolio_stats):
        """
        Used to send a portfolio reporting Slack message
        """
        if portfolio_stats is None:
            slack_message = self.slack_no_stats
            self.send_slack(slack_message)
            return

        statistics_day, initial_capital, ending_capital, net_profit, net_profit_percentage, market_return_percentage, average_daily_return_percentage, average_daily_volatility_percentage, jensen_alpha, beta, sharpe_ratio, treynor_ratio, information_ratio = portfolio_stats

        slack_message = self.slack_portfolio_report_str.format(statistics_day, round(initial_capital, 4), round(ending_capital, 4), round(net_profit, 4), round(net_profit_percentage, 4), round(market_return_percentage, 4), round(average_daily_return_percentage, 4), round(average_daily_volatility_percentage, 4), round(jensen_alpha, 4),round(beta, 4), round(sharpe_ratio, 4), round(treynor_ratio, 4),round(information_ratio, 4))
        
        self.send_slack(slack_message)


    def print_portfolio_report(self, portfolio_stats):
        """
        Used to print portfolio report's info to the console
        """
        if portfolio_stats is None:
            print(self.no_stats)
            return
        statistics_day, initial_capital, ending_capital, net_profit, net_profit_percentage, market_return_percentage, average_daily_return_percentage, average_daily_volatility_percentage, jensen_alpha, beta, sharpe_ratio, treynor_ratio, information_ratio = portfolio_stats

        message = self.portfolio_report_str.format(statistics_day, round(initial_capital, 4), round(ending_capital, 4), round(net_profit, 4), round(net_profit_percentage, 4), round(market_return_percentage, 4), round(average_daily_return_percentage, 4), round(average_daily_volatility_percentage, 4), round(jensen_alpha, 4), round(beta, 4), round(sharpe_ratio, 4), round(treynor_ratio, 4), round(information_ratio, 4))
        
        print(message)

