import unittest
from unittest.mock import MagicMock
from api.api import BybitAPI


class TestBybitAPI(unittest.TestCase):
    def setUp(self):
        self.config = {
            'start_time': 30,
            'test_method': 0,
            'spread_type': 0,
            'top_count': 10
        }
        self.logger = MagicMock()
        self.api = BybitAPI(self.config, self.logger, testnet=True)

    def test_get_usdt_pairs(self):
        self.api.session.get_tickers = MagicMock(return_value={
            'result': {
                'list': [
                    {'symbol': 'BTCUSDT'},
                    {'symbol': 'ETHUSDT'},
                    {'symbol': 'MATICUSDT'}
                ]
            }
        })
        pairs = self.api.get_usdt_pairs()
        self.assertEqual(pairs, ['BTCUSDT', 'ETHUSDT', 'MATICUSDT'])

    def test_get_usdt_pairs_no_result(self):
        self.api.session.get_tickers = MagicMock(return_value={'result': {}})
        pairs = self.api.get_usdt_pairs()
        self.assertEqual(pairs, [])

    def test_get_usdt_pairs_error(self):
        self.api.session.get_tickers = MagicMock(return_value={})
        pairs = self.api.get_usdt_pairs()
        self.assertEqual(pairs, [])

    def test_get_usdt_pairs_test_method(self):
        self.api.config['test_method'] = 1
        pairs = self.api.get_usdt_pairs()
        self.assertEqual(pairs, ['BTCUSDT', 'ETHUSDT', 'MATICUSDT'])

    def test_fetch_data(self):
        self.api.session.get_kline = MagicMock(return_value={
            'result': {
                'list': [
                    {'startTime': 1625097600000, 'openPrice': '100', 'highPrice': '110', 'lowPrice': '90',
                     'closePrice': '105', 'volume': '1000', 'turnover': '105000'}
                ],
                'symbol': 'BTCUSDT'
            }
        })
        data = self.api.fetch_data('BTCUSDT', '240')
        self.assertFalse(data.empty)

    def test_fetch_data_no_result(self):
        self.api.session.get_kline = MagicMock(return_value={'result': {}})
        data = self.api.fetch_data('BTCUSDT', '240')
        self.assertTrue(data.empty)

    def test_fetch_data_error(self):
        self.api.session.get_kline = MagicMock(return_value={})
        data = self.api.fetch_data('BTCUSDT', '240')
        self.assertTrue(data.empty)

    def test_fetch_data_invalid_interval(self):
        with self.assertRaises(ValueError):
            self.api.fetch_data('BTCUSDT', 'invalid_interval')


if __name__ == '__main__':
    unittest.main()
