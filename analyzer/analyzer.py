import itertools
import numpy as np
from statsmodels.tsa.stattools import adfuller
from tabulate import tabulate
from api.api import BybitAPI
from processor.data_processor import DataProcessor


class CryptoPairAnalyzer:
    def __init__(self, config, logger, testnet=False):
        self.config = config
        self.logger = logger
        self.api = BybitAPI(config, logger, testnet)
        self.processor = DataProcessor()
        self.top_count = self.config['top_count']
        self.logger.info("Initialized CryptoPairAnalyzer with testnet=" + str(testnet))

    def apply_adf_test(self, data, timeframe):
        self.logger.info(f"Applying ADF test on timeframe: {timeframe}")
        results = []
        for pair1, pair2 in itertools.combinations(data.keys(), 2):
            self.logger.info(f"Calculating spread for pair {pair1} and {pair2}")
            resampled_pair1 = data[pair1].resample(timeframe).last()['closePrice']
            resampled_pair2 = data[pair2].resample(timeframe).last()['closePrice']
            if self.config['spread_type'] == 1:
                spread = np.log(resampled_pair1) - np.log(resampled_pair2)
            else:
                spread = resampled_pair1 / resampled_pair2
            spread = spread.dropna()
            if spread.empty or len(spread) < 20:
                self.logger.warning(
                    f"No data available or sample size too small for ADF test between {pair1} and {pair2}")
                continue
            try:
                result = adfuller(spread, autolag='AIC')
                adf_statistic, p_value = result[0], result[1]
                if -7 <= adf_statistic <= -4 and p_value <= 0.05:
                    results.append(
                        (pair1, pair2, adf_statistic, p_value, self.processor.calculate_z_score(spread).iloc[-1]))
            except ValueError as e:
                self.logger.warning(f"Error in ADF test for pairs {pair1} and {pair2}: {str(e)}")
                continue
        results_sorted = sorted(results, key=lambda x: (x[3], x[2]))
        return results_sorted[:self.top_count]

    def analyze_pairs(self):
        self.logger.info("Starting analysis of pairs.")
        symbols = self.api.get_usdt_pairs()
        data_4h = {symbol: self.processor.process_data(self.api.fetch_data(symbol, '240')) for symbol in symbols}
        self.logger.info("Applying ADF test for 4H data.")
        adf_results_4h = self.apply_adf_test(data_4h, '4h')
        top_pairs_4h = [pair[:2] for pair in sorted(adf_results_4h, key=lambda x: x[3])[:self.top_count]]
        data_1h = {symbol: self.processor.process_data(self.api.fetch_data(symbol, '60')) for symbol, _ in top_pairs_4h}
        self.logger.info("Applying ADF test for 1H data on top 500 pairs.")
        adf_results_1h = self.apply_adf_test(data_1h, '1h')

        print("Sorted 4H ADF Results:\n" + tabulate(adf_results_4h[:500],
                                                    headers=['Pair 1', 'Pair 2', 'ADF Statistic', 'P-Value',
                                                             'Current Z-Score'],
                                                    tablefmt='grid'))
        print("Sorted 1H ADF Results:\n" + tabulate(adf_results_1h,
                                                    headers=['Pair 1', 'Pair 2', 'ADF Statistic', 'P-Value',
                                                             'Current Z-Score'],
                                                    tablefmt='grid'))

        if adf_results_4h:
            top_4h = ", ".join([f"{res[0]}/{res[1]}" for res in adf_results_4h])
            print(f"Top 4H Pairs: {top_4h}")
        if adf_results_1h:
            top_1h = ", ".join([f"{res[0]}/{res[1]}" for res in adf_results_1h])
            print(f"Top 1H Pairs: {top_1h}")
