# Trade Class
from utils import get_chart

class Trade:
    def __init__(self, market, entry_date, entry_price, position_size, trade_type, interval):
        self.market = market
        self.entry_date = entry_date
        self.entry_price = entry_price
        self.position_size = position_size
        self.trade_type = trade_type
        self.interval = interval

        self.exit_date = None
        self.status = True # True for open, False for closed
        self.profit = None

    def __repr__(self):
        return f"""
        Trade: 
        market={self.market}, 
        entry_date={self.entry_date}, 
        entry_price={self.entry_price}, 
        trade_type={self.trade_type}, 
        exit_date={self.exit_date}, 
        status={self.status}, 
        profit={self.profit})
        """

    def __str__(self):
        return f"""
        Trade: 
        market={self.market}, 
        entry_date={self.entry_date}, 
        entry_price={self.entry_price}, 
        trade_type={self.trade_type}, 
        exit_date={self.exit_date}, 
        status={self.status}, 
        profit={self.profit})
        """
        # position_size={self.position_size}, 
    
    def close_trade(self, exit_date, exit_price):
        if self.status:
            self.exit_date = exit_date
            self.exit_price = exit_price
            if self.trade_type == 'buy':
                self.profit = (self.exit_price - self.entry_price)* self.position_size
            elif self.trade_type =='sell':
                self.profit = (self.entry_price - self.exit_price)* self.position_size
            self.status = False