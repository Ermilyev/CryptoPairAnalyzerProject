import json
import os
import logging


def read_configuration():
    file_path = os.path.join(os.path.dirname(__file__), 'config.json')
    config = {
        'start_time': 30,  # Количество дней в периоде (значение по умолчанию)
        'test_method': 0,  # 0 - Обычный метод, 1 - Тестовый метод (значение по умолчанию)
        'spread_type': 0,  # 0 - Деление, 1 - Вычитание логорифмов (значение по умолчанию)
        'top_count': 10  # Максимальное количество результатов для вывода (значение по умолчанию)
    }
    try:
        with open(file_path, 'r') as file:
            config_from_file = json.load(file)
            config.update(config_from_file)
    except FileNotFoundError:
        logging.error(f'Configuration file not found: {file_path}')
    except json.JSONDecodeError:
        logging.error(f'Error decoding JSON from the configuration file: {file_path}')
    except Exception as e:
        logging.error(f'Unexpected error while reading the configuration file: {e}')
    return config
