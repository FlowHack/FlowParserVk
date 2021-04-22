import json
import os

from settings.additional.variables import path_to_dir_dicts

from ..settings import LOGGER

LOGGER = LOGGER('add_dicts', 'main')

#  Словарь стран
try:
    with open(os.path.join(path_to_dir_dicts, 'countries.json'),
              'r', encoding='utf-8') as file:
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
    with open(os.path.join(path_to_dir_dicts, 'error.json'), 'r',
              encoding='utf-8') as file:
        ERROR_MSG = json.load(file)
        LOGGER.info('Загружен словарь ошибок')
except FileNotFoundError as error:
    LOGGER.error('Не найден файл "error.json"')
try:
    with open(os.path.join(path_to_dir_dicts, 'warning.json'), 'r',
              encoding='utf-8') as file:
        WARNING_MSG = json.load(file)
        LOGGER.info('Загружен словарь предупреждений')
except FileNotFoundError as error:
    LOGGER.error('Не найден файл "warning.json"')
try:
    with open(os.path.join(path_to_dir_dicts, 'info.json'), 'r',
              encoding='utf-8') as file:
        INFO_MSG = json.load(file)
        LOGGER.info('Загружен словарь информационных сообщений')
except FileNotFoundError as error:
    LOGGER.error('Не найден файл "info.json"')

#  Словарь статусов
STATUS_VK_PERSON = {
    'не женат (не замужем)': 1,
    'встречается': 2,
    'помолвлен(-а)': 3,
    'женат (замужем)': 4,
    'всё сложно': 5,
    'в активном поиске': 6,
    'влюблен(-а)': 7,
    'в гражданском браке': 8
}

POLITICAL = {
    'коммунистические': 1,
    'социалистические': 2,
    'умеренные': 3,
    'либеральные': 4,
    'консервативные': 5,
    'монархические': 6,
    'ультраконсервативные': 7,
    'индифферентные': 8,
    'либертарианские': 9,
}

PEOPLE_MAIN = {
    'ум и креативность': 1,
    'доброта и честность': 2,
    'красота и здоровье': 3,
    'власть и богатство': 4,
    'смелость и упорство': 5,
    'юмор и жизнелюбие': 6,
}

LIFE_MAIN = {
    'семья и дети': 1,
    'карьера и деньги': 2,
    'развлечения и отдых': 3,
    'наука и исследования': 4,
    'совершенствование мира': 5,
    'саморазвитие': 6,
    'красота и искусство': 7,
    'слава и влияние': 8,
}

SMOKING = {
    'резко негативное': 1,
    'негативное': 2,
    'компромиссное': 3,
    'нейтральное': 4,
    'положительное': 5,
}

ALCOHOL = {
    'резко негативное': 1,
    'негативное': 2,
    'компромиссное': 3,
    'нейтральное': 4,
    'положительное': 5,
}
