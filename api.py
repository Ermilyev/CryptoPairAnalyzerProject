import datetime as dt
from pybit.unified_trading import HTTP
import pandas as pd
from data_processor import DataProcessor


class BybitAPI:
    def __init__(self, config, logger, testnet=False):
        self.config = config
        self.logger = logger
        self.session = HTTP(testnet=testnet)
        self.end_time = int(dt.datetime.now().timestamp() * 1000)
        self.start_time = self.end_time - self.config['start_time'] * 24 * 60 * 60 * 1000

    def get_usdt_pairs(self):
        if self.config['test_method'] == 0:
            self.logger.info("Fetching USDT pairs from Bybit.")
            response = self.session.get_tickers(category="linear")
            if 'result' not in response or not response['result'].get('list'):
                self.logger.error(
                    "Failed to fetch tickers: " + str(response.get('ret_msg', 'No error message provided')))
                return []
            pairs = [ticker['symbol'] for ticker in response['result']['list'] if 'USDT' in ticker['symbol']]
            self.logger.info("Retrieved pairs: " + ', '.join(pairs))
            return pairs
        else:
            return self.get_usdt_pairs_test()

    @staticmethod
    def get_usdt_pairs_test():
        return ['BTCUSDT', 'ETHUSDT', 'MATICUSDT']

    def fetch_data(self, symbol, interval):
        self.logger.info(f"Fetching data for symbol: {symbol} with interval: {interval}")
        data = self.session.get_kline(symbol=symbol, interval=interval, start=self.start_time, end=self.end_time)
        if 'result' not in data or 'list' not in data['result']:
            self.logger.error(f"Failed to fetch data for {symbol}: {data.get('ret_msg', 'No error message provided')}")
            return pd.DataFrame()
        return DataProcessor.process_data(data['result'])
