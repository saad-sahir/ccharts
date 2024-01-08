# Strategy class
from trade import Trade
            
class Strategy:
    def __init__(self, conditions, columns, marketenv):
        self.marketenv = marketenv
        self.market = marketenv.market
        self.interval = marketenv.interval
        self.data = marketenv.data
        self.columns = columns # columns of interest (open, close, volume, indicators, etc...)
        self.conditions = conditions # list of conditions as lambda functions

    def evaluate_market(self, row):

        ## If strategy condition(s) is met return true else false
        ## row = a row in an ohlc df with conditions

        for condition in self.conditions:
            for trade in self.marketenv.trades:
                if trade.status and condition['exit'](row):
                    trade.close_trade(row['Date'], row['Close'])

            if condition['enter'](row):
                entry_price = row['Close']
                trade = Trade(
                    self.market,
                    row['Date'],
                    entry_price,
                    1,
                    condition['type'],
                    self.interval
                )
                self.marketenv.trades.append(trade)
                return True