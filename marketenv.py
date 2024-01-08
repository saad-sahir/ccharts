# MarketEnv class
import random
from datetime import datetime, timedelta
from utils import get_chart

class MarketEnv:
    def __init__(self, market, interval, current_index=0):
        self.market = market
        self.interval = interval
        self.current_index = current_index
        self.trades = []
        self.current_date = self._get_random_date(datetime(2022, 1, 1), datetime(2023, 12, 31))
        self.data = self._get_data(self.current_date)

    def _get_data(self, now):
        df = get_chart(self.market, self.interval, now=now)
        ## option to add indicator columns to dataframe
        df['EMA5'] = df['Close'].ewm(span=5, adjust=False).mean()
        df['EMA10'] = df['Close'].ewm(span=10, adjust=False).mean()
        df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
        return df

    def _get_random_date(self, start_date, end_date):
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        random_date = start_date + timedelta(days=random_days)
        return random_date

    def simulate(self, strategy):
        for i in range(len(self.data)):
            data = self.data.loc[:i, strategy.columns]
            for index, row in data.iterrows():
                # print(index)
                self.current_date = row['Date']
                strategy.evaluate_market(row)