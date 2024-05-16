# Crypto Analyzer

Crypto Analyzer is a Python-based project designed to analyze cryptocurrency pairs using advanced statistical methods. This tool fetches market data from cryptocurrency exchanges and applies statistical tests to identify promising trading pairs. The project is designed to help traders and analysts make informed decisions based on historical data analysis.

## Features

- **Fetches Market Data**: Retrieves cryptocurrency market data from exchanges like Bybit.
- **Statistical Analysis**: Applies Augmented Dickey-Fuller (ADF) test to evaluate the stationarity of price spreads between pairs.
- **Configurable Parameters**: Allows customization of analysis period, methods, and top results count.
- **Automated Reports**: Generates detailed reports of the top cryptocurrency pairs based on statistical significance.
- **Logging**: Provides comprehensive logging for tracking the analysis process and results.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/ermilyev/crypto_analyzer.git
    cd crypto_analyzer
    ```

2. Set Up the Environment:

    Create and activate a virtual environment:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up configuration in `config/config.json`:
    ```json
    {
        "start_time": 30,
        "test_method": 0,
        "spread_type": 0,
        "top_count": 10
    }
    ```

## Usage

Run the main script to start the analysis:
```sh
python main.py
 ```
## Examples

Here is an example of how to use the Crypto Analyzer to fetch and analyze cryptocurrency data:

```python
from config.config import read_configuration
from logger.logger import setup_logger
from analyzer.analyzer import CryptoPairAnalyzer

config = read_configuration()
logger = setup_logger()
analyzer = CryptoPairAnalyzer(config, logger, testnet=False)
analyzer.analyze_pairs()
```

![Build Status](https://github.com/ermilyev/crypto_analyzer/actions/workflows/ci.yml/badge.svg)
![Coverage](https://coveralls.io/repos/github/ermilyev/crypto_analyzer/badge.svg?branch=main)
![License](https://img.shields.io/github/license/ermilyev/crypto_analyzer.svg)
