import unittest
from unittest.mock import MagicMock
from api.api import BybitAPI


class TestBybitAPI(unittest.TestCase):
    def setUp(self):
        config = {
            'start_time': 30,
            'test_method': 0,
            'spread_type': 0,
            'top_count': 10
        }
        self.logger = MagicMock()
        self.api = BybitAPI(config, self.logger, testnet=True)

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


if __name__ == '__main__':
    unittest.main()
