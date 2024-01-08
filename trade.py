# Trade Class
from utils import get_chart

class Trade:
    def __init__(self, market, entry_date, position_size, trade_type, interval):
        self.market = market
        self.entry_date = entry_date
        self.position_size = position_size
        self.trade_type = trade_type

        self.exit_date = None
        self.entry_price = self._get_price()
        self.status = True # True for open, False for closed
        self.profit = None

        self.interval = interval

    def _get_price(self):
        df = get_chart(
            self.market,
            self.interval,
            now=self.entry_date if self.exit_date is None else self.exit_date
        )
        return df.iloc[-1]['Close']
    
    def close_trade(self, current_date):
        if self.status:
            self.exit_date = current_date
            self.exit_price = self._get_price()
            if self.trade_type == 'buy':
                self.profit = (self.exit_price - self.entry_price)* self.position_size
            elif self.trade_type =='sell':
                self.profit = (self.entry_price - self.exit_price)* self.position_size
            self.status = False