"""
Note - for some of the metrics the absolute value is returns. This is because if the risk (loss) is higher we want to
discount the expected excess return from the portfolio by a higher amount. Therefore risk should be positive.
"""

import math
import numpy


class PortfolioMetrics(object):
    """
    Used for computing portfolio risks metrics
    """

    def __init__(self, risk_free_rate):
        self.risk_free_rate = risk_free_rate

    def vol(self, returns):
        # Return the standard deviation of returns
        return numpy.std(returns)

    def beta(self, returns, market):
        # Create a matrix of [returns, market]
        m = numpy.matrix([returns, market])
        # Return the covariance of m divided by the standard deviation of the market returns
        std = numpy.std(market)
        if std == 0:
            return 0
        return numpy.cov(m)[0][1] / std

    def lpm(self, returns, threshold, order):
        # This method returns a lower partial moment of the returns
        # Create an array he same length as returns containing the minimum return threshold
        threshold_array = numpy.empty(len(returns))
        threshold_array.fill(threshold)
        # Calculate the difference between the threshold and the returns
        diff = threshold_array - returns
        # Set the minimum of each to 0
        diff = diff.clip(min=0)
        # Return the sum of the different to the power of order
        return numpy.sum(diff ** order) / len(returns)

    def hpm(self, returns, threshold, order):
        # This method returns a higher partial moment of the returns
        # Create an array he same length as returns containing the minimum return threshold
        threshold_array = numpy.empty(len(returns))
        threshold_array.fill(threshold)
        # Calculate the difference between the returns and the threshold
        diff = returns - threshold_array
        # Set the minimum of each to 0
        diff = diff.clip(min=0)
        # Return the sum of the different to the power of order
        return numpy.sum(diff ** order) / len(returns)

    def var(self, returns, alpha):
        # This method calculates the historical simulation var of the returns
        sorted_returns = numpy.sort(returns)
        # Calculate the index associated with alpha
        index = int(alpha * len(sorted_returns))
        # VaR should be positive
        return abs(sorted_returns[index])

    def cvar(self, returns, alpha):
        # This method calculates the condition VaR of the returns
        sorted_returns = numpy.sort(returns)
        # Calculate the index associated with alpha
        index = int(alpha * len(sorted_returns))
        # Calculate the total VaR beyond alpha
        sum_var = sorted_returns[0]
        for i in range(1, index):
            sum_var += sorted_returns[i]
        # Return the average VaR
        # CVaR should be positive
        return abs(sum_var / index)

    # NOT ACCURATE
    # TBD More accurate prices
    def prices(self, returns, base):
        # Converts returns into prices
        s = [base]
        for i in range(len(returns)):
            s.append(base * (1 + returns[i]))
        return numpy.array(s)

    def dd(self, returns, tau):
        # Returns the draw-down given time period tau
        values = self.prices(returns, 100)
        pos = len(values) - 1
        pre = pos - tau
        drawdown = float('+inf')
        # Find the maximum drawdown given tau
        while pre >= 0:
            dd_i = (values[pos] / values[pre]) - 1
            if dd_i < drawdown:
                drawdown = dd_i
            pos, pre = pos - 1, pre - 1
        # Drawdown should be positive
        return abs(drawdown)

    def max_dd(self, returns):
        # Returns the maximum draw-down for any tau in (0, T) where T is the length of the return series
        max_drawdown = float('-inf')
        for i in range(0, len(returns)):
            drawdown_i = self.dd(returns, i)
            if drawdown_i > max_drawdown:
                max_drawdown = drawdown_i
        # Max draw-down should be positive
        return abs(max_drawdown)

    def average_dd(self, returns, periods):
        # Returns the average maximum drawdown over n periods
        drawdowns = []
        for i in range(0, len(returns)):
            drawdown_i = self.dd(returns, i)
            drawdowns.append(drawdown_i)
        drawdowns = sorted(drawdowns)
        total_dd = abs(drawdowns[0])
        for i in range(1, periods):
            total_dd += abs(drawdowns[i])
        return total_dd / periods

    def average_dd_squared(self, returns, periods):
        # Returns the average maximum drawdown squared over n periods
        drawdowns = []
        for i in range(0, len(returns)):
            drawdown_i = math.pow(self.dd(returns, i), 2.0)
            drawdowns.append(drawdown_i)
        drawdowns = sorted(drawdowns)
        total_dd = abs(drawdowns[0])
        for i in range(1, periods):
            total_dd += abs(drawdowns[i])
        return total_dd / periods

    def treynor_ratio(self, er, returns, market, rf):
        beta = self.beta(returns, market)
        if beta == 0:
            return 0
        return (er - rf) / beta

    def sharpe_ratio(self, er, returns, rf):
        vol = self.vol(returns)
        if vol == 0:
            return 0
        return (er - rf) / vol

    def alpha_jensen(self, er, em, returns, market, rf):
        return er - (rf + float(self.beta(returns, market)) * (em - rf))

    def information_ratio(self, returns, benchmark):
        diff = returns - benchmark
        vol = self.vol(diff)
        if vol == 0:
            return 0
        return numpy.mean(diff) / vol

    def modigliani_ratio(self, er, returns, benchmark, rf):
        np_rf = numpy.empty(len(returns))
        np_rf.fill(rf)
        rdiff = returns - np_rf
        bdiff = benchmark - np_rf
        vol_bd = self.vol(bdiff)
        if vol_bd == 0:
            return 0
        return (er - rf) * (self.vol(rdiff) / self.vol(bdiff)) + rf

    def excess_var(self, er, returns, rf, alpha):
        var = self.var(returns, alpha)
        if var == 0:
            return 0
        return (er - rf) / var

    def conditional_sharpe_ratio(self, er, returns, rf, alpha):
        cvar = self.cvar(returns, alpha)
        if cvar == 0:
            return 0
        return (er - rf) / cvar

    #TODO Continue to handle possible exception raised when trying to divide by 0
    def omega_ratio(self, er, returns, rf, target=0):
        return (er - rf) / self.lpm(returns, target, 1)

    def sortino_ratio(self, er, returns, rf, target=0):
        return (er - rf) / math.sqrt(self.lpm(returns, target, 2))

    def kappa_three_ratio(self, er, returns, rf, target=0):
        return (er - rf) / math.pow(self.lpm(returns, target, 3), float(1 / 3))

    def gain_loss_ratio(self, returns, target=0):
        return self.hpm(returns, target, 1) / self.lpm(returns, target, 1)

    def upside_potential_ratio(self, returns, target=0):
        return self.hpm(returns, target, 1) / math.sqrt(self.lpm(returns, target, 2))

    def calmar_ratio(self, er, returns, rf):
        return (er - rf) / self.max_dd(returns)

    def sterling_ration(self, er, returns, rf, periods):
        return (er - rf) / self.average_dd(returns, periods)

    def burke_ratio(self, er, returns, rf, periods):
        return (er - rf) / math.sqrt(self.average_dd_squared(returns, periods))

    # Messenger
    def get_risk_metrics(self, portfolio_returns, market_returns):
        # This is just a testing method
        r = portfolio_returns
        m = market_returns
        er = numpy.mean(r)
        em = numpy.mean(m)
        f = self.risk_free_rate

        #General information
        average_daily_return = er
        average_daily_volatility = self.vol(r)
        max_drawdown = self.max_dd(r)
        var_0_05 = self.var(r, 0.05)

        #Metrics based CAPM method
        jensen_alpha = self.alpha_jensen(er, em, r, m, f)
        beta = self.beta(r, m)

        #Risk-adjusted return based on volatility
        sharpe_ratio = self.sharpe_ratio(er, r, f)
        treynor_ratio = self.treynor_ratio(er, r, m, f)
        information_ratio = self.information_ratio(r, m)

        return average_daily_return, average_daily_volatility, max_drawdown, var_0_05, jensen_alpha, beta, sharpe_ratio, treynor_ratio, information_ratio
