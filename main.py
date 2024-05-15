from config import read_configuration
from logger import setup_logger
from analyzer import CryptoPairAnalyzer


def main():
    config = read_configuration()
    logger = setup_logger()
    analyzer = CryptoPairAnalyzer(config, logger, testnet=False)
    analyzer.analyze_pairs()


if __name__ == "__main__":
    main()
