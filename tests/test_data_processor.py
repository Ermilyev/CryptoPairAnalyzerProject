import unittest
import pandas as pd
from processor.data_processor import DataProcessor


class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = DataProcessor()

    def test_process_data(self):
        result = {
            'list': [
                {'startTime': 1625097600000, 'openPrice': '100', 'highPrice': '110', 'lowPrice': '90',
                 'closePrice': '105', 'volume': '1000', 'turnover': '105000'}
            ],
            'symbol': 'BTCUSDT'
        }
        df = self.processor.process_data(result)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 1)
        self.assertEqual(df['symbol'].iloc[0], 'BTCUSDT')  # Использование .iloc

    def test_calculate_z_score(self):
        series = pd.Series([1, 2, 3, 4, 5])
        z_scores = self.processor.calculate_z_score(series)
        self.assertAlmostEqual(z_scores.mean(), 0)
        self.assertAlmostEqual(z_scores.std(), 1)


if __name__ == '__main__':
    unittest.main()
