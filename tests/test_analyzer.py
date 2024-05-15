import unittest
from unittest.mock import MagicMock
import pandas as pd
from analyzer.analyzer import CryptoPairAnalyzer


class TestCryptoPairAnalyzer(unittest.TestCase):
    def setUp(self):
        config = {
            'start_time': 30,
            'test_method': 1,
            'spread_type': 0,
            'top_count': 10
        }
        self.logger = MagicMock()
        self.analyzer = CryptoPairAnalyzer(config, self.logger, testnet=True)

    def test_apply_adf_test(self):
        data = {
            'BTCUSDT': pd.DataFrame({
                'closePrice': [1, 2, 3, 4, 5]
            }, index=pd.date_range('2023-01-01', periods=5, freq='D')),
            'ETHUSDT': pd.DataFrame({
                'closePrice': [2, 3, 4, 5, 6]
            }, index=pd.date_range('2023-01-01', periods=5, freq='D'))
        }
        result = self.analyzer.apply_adf_test(data, '1d')
        self.assertIsInstance(result, list)

    def test_analyze_pairs(self):
        self.analyzer.api.get_usdt_pairs = MagicMock(return_value=['BTCUSDT', 'ETHUSDT'])
        self.analyzer.api.fetch_data = MagicMock(return_value=pd.DataFrame({
            'startTime': [1625097600000],
            'openPrice': [100],
            'highPrice': [110],
            'lowPrice': [90],
            'closePrice': [105],
            'volume': [1000],
            'turnover': [105000],
            'symbol': ['BTCUSDT']
        }).set_index(pd.to_datetime([1625097600000], unit='ms')))
        self.analyzer.analyze_pairs()
        self.logger.info.assert_called()


if __name__ == '__main__':
    unittest.main()
