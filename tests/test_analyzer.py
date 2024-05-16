import unittest
from unittest.mock import MagicMock
import pandas as pd
import numpy as np
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

    def test_apply_adf_test_empty_data(self):
        data = {
            'BTCUSDT': pd.DataFrame({'closePrice': []}, index=pd.to_datetime([])),
            'ETHUSDT': pd.DataFrame({'closePrice': []}, index=pd.to_datetime([]))
        }
        result = self.analyzer.apply_adf_test(data, '1d')
        self.assertEqual(result, [])

    def test_apply_adf_test_insufficient_data(self):
        data = {
            'BTCUSDT': pd.DataFrame({
                'closePrice': [1, 2]
            }, index=pd.date_range('2023-01-01', periods=2, freq='D')),
            'ETHUSDT': pd.DataFrame({
                'closePrice': [2, 3]
            }, index=pd.date_range('2023-01-01', periods=2, freq='D'))
        }
        result = self.analyzer.apply_adf_test(data, '1d')
        self.assertEqual(result, [])

    def test_apply_adf_test_with_error(self):
        data = {
            'BTCUSDT': pd.DataFrame({
                'closePrice': [1, 2, 3, 4, 5]
            }, index=pd.date_range('2023-01-01', periods=5, freq='D')),
            'ETHUSDT': pd.DataFrame({
                'closePrice': [2, 3, 4, 5, 6]
            }, index=pd.date_range('2023-01-01', periods=5, freq='D'))
        }
        self.analyzer.processor.calculate_z_score = MagicMock(side_effect=ValueError("Test Error"))
        result = self.analyzer.apply_adf_test(data, '1d')
        self.assertEqual(result, [])

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

    def test_analyze_pairs_no_pairs(self):
        self.analyzer.api.get_usdt_pairs = MagicMock(return_value=[])
        self.analyzer.analyze_pairs()
        self.logger.info.assert_called()

    def test_analyze_pairs_fetch_data_failure(self):
        self.analyzer.api.get_usdt_pairs = MagicMock(return_value=['BTCUSDT', 'ETHUSDT'])
        self.analyzer.api.fetch_data = MagicMock(return_value=pd.DataFrame({
            'startTime': [],
            'openPrice': [],
            'highPrice': [],
            'lowPrice': [],
            'closePrice': [],
            'volume': [],
            'turnover': [],
            'symbol': []
        }).set_index(pd.to_datetime([])))
        self.analyzer.analyze_pairs()
        self.logger.info.assert_called()


if __name__ == '__main__':
    unittest.main()
