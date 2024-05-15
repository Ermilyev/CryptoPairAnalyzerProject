import pandas as pd


class DataProcessor:
    @staticmethod
    def process_data(result):
        df = pd.DataFrame(result['list'],
                          columns=['startTime', 'openPrice', 'highPrice', 'lowPrice', 'closePrice', 'volume',
                                   'turnover'])
        df['startTime'] = pd.to_datetime(df['startTime'].astype(int), unit='ms')
        df.set_index('startTime', inplace=True)
        df['symbol'] = result['symbol']
        df[['openPrice', 'highPrice', 'lowPrice', 'closePrice', 'volume', 'turnover']] = df[
            ['openPrice', 'highPrice', 'lowPrice', 'closePrice', 'volume', 'turnover']].apply(pd.to_numeric)
        return df

    @staticmethod
    def calculate_z_score(series):
        mean = series.mean()
        std = series.std()
        z_scores = (series - mean) / std
        return z_scores
