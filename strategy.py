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
            if condition['enter'](row):
                trade = Trade(
                    self.market,
                    self.data.iloc[self.current_index],
                    1,
                    condition['type'],
                    self.interval
                )
                self.marketenv.current_index += 1
                self.marketenv.trade.append(trade)
                return True