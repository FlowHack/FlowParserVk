import json

from settings.additional.variables import path_to_dir_dicts

from ..settings import LOGGER

#  Словарь стран
try:
    with open(f'{path_to_dir_dicts}/countries.json',
              'r') as file:
        file_str = json.load(file)
        LIST_COUNTRIES = json.loads(file_str)
        LOGGER.info('Загружен словарь LIST_COUNTRIES')
except FileNotFoundError as error:
    LIST_COUNTRIES = {
        'Россия': 1,
        'Украина': 2,
        'Беларусь': 3
    }
    LOGGER.warning(
        'Не найден файл "countries.json", загружены резервные данные!'
    )

#  Словарь ошибок
try:
    with open(f'{path_to_dir_dicts}/error.json', 'r') as file:
        ERROR_MSG = json.load(file)
        LOGGER.info('Загружен словарь ошибок')
except FileNotFoundError as error:
    LOGGER.error('Не найден файл "error.json"')
try:
    with open(f'{path_to_dir_dicts}/warning.json', 'r') as file:
        WARNING_MSG = json.load(file)
        LOGGER.info('Загружен словарь предупреждений')
except FileNotFoundError as error:
    LOGGER.error('Не найден файл "warning.json"')
try:
    with open(f'{path_to_dir_dicts}/info.json', 'r') as file:
        INFO_MSG = json.load(file)
        LOGGER.info('Загружен словарь информационных сообщений')
except FileNotFoundError as error:
    LOGGER.error('Не найден файл "info.json"')

#  Словарь статусов
STATUS_VK_PERSON = {
        'Не выбранно': 0,
        'не женат (не замужем)': 1,
        'встречается': 2,
        'помолвлен(-а)': 3,
        'женат (замужем)': 4,
        'всё сложно': 5,
        'в активном поиске': 6,
        'влюблен(-а)': 7,
        'в гражданском браке': 8
    }
