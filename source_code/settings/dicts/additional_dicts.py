from settings.settings import SettingsFunction, get_logger
import json

logger = get_logger('additional_dicts')

#  Словарь стран
try:
    with open(f'{SettingsFunction.path_to_dir_dicts}/countries.json',
              'r') as file:
        file_str = json.load(file)
        LIST_COUNTRIES = json.loads(file_str)
except FileNotFoundError as error:
    logger.warning(
        'Не найден файл "countries.json", загружены резервные данные!'
    )
    LIST_COUNTRIES = {
        'Россия': 1,
        'Украина': 2,
        'Беларусь': 3
    }

#  Словарь ошибок
try:
    with open(f'{SettingsFunction.path_to_dir_dicts}/error.json', 'r') as file:
        ERROR_MSG = json.load(file)
except FileNotFoundError as error:
    logger.error('Не найден файл "error.json"')

#  Словарь статусов
STATUS_VK_PERSON = {
        'Не выбрано': 0,
        'не женат (не замужем)': 1,
        'встречается': 2,
        'помолвлен(-а)': 3,
        'женат (замужем)': 4,
        'всё сложно': 5,
        'в активном поиске': 6,
        'влюблен(-а)': 7,
        'в гражданском браке': 8
    }
