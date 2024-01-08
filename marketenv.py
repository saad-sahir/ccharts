# MarketEnv class
import random
from datetime import datetime, timedelta
from utils import get_chart

class MarketEnv:
    def __init__(self, market, interval, current_index=0):
        self.market = market
        self.interval = interval
        self.current_index = current_index
        self.trade = []
        self.current_date = self._get_random_date(datetime(2022, 1, 1), datetime(2023, 12, 31))
        self.data = self._get_data(self.current_date)

    def _get_data(self, now):
        df = get_chart(self.market, self.interval, now=now)
        ## option to add indicator columns to dataframe
        # df['indicator'] = indicator()
        return df

    def _get_random_date(self, start_date, end_date):
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        random_date = start_date + timedelta(days=random_days)
        return random_date

    def simulate(self, strategy):
        data = self.data.loc[:self.current_index, strategy.columns]
        for _, row in data.iterrows():
            self.current_date = row['Date']
            strategy.evaluate_market(row)
            self.current_index += 1