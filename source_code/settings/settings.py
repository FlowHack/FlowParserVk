import logging
from logging import INFO, getLogger
from logging.handlers import RotatingFileHandler
from os import getcwd
import json


def get_logger(name: str) -> object:
    """
    Функция создания логгера
    :param name: имя файла логгера
    :return: объект логгера
    """
    logger = getLogger(name)
    logger.setLevel(INFO)

    logger_format = (
        '[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s'
    )
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(fmt=logger_format, datefmt=date_format)

    handler = RotatingFileHandler(
        fr'settings/log/{name}.log',
        maxBytes=50000000,
        backupCount=5,
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logger = get_logger('settings')


class SettingsFunction:
    VERSION = '0.1.0'
    VERSION_API = '5.130'
    APP_NAME = 'FlowParserVK'
    AUTHOR_PAGE = 'https://vk.com/flow_hack'
    PAGE_APP = ''
    TELEGRAM_BOT_APP = ''
    VK_BOT_APP = ''
    BANK_DETAILS = {
        'sberbank': '5469560018109591',
        'ymoney': '410017514569348',
        'qiwi_visa': '4890494702214891'
    }

    path = getcwd()
    path_to_dir_settings = f'{path}/settings'
    path_to_dir_dicts = f'{path_to_dir_settings}/dicts'
    path_to_dir_ico = f'{path_to_dir_settings}/ico'
    path_to_dir_style = f'{path_to_dir_settings}/style/awthemes-10.2.0'
    path_to_db = f'{path_to_dir_settings}/settings.db'

    MAIN_FONT = 'Times New Roman'
    H1_FONT = (MAIN_FONT, 20, 'bold italic')
    H5_FONT = (MAIN_FONT, 14, 'bold italic')
    H6_FONT = (MAIN_FONT, 12, 'bold italic')
    INPUT_FONT = (MAIN_FONT, 10, 'bold italic')
    COMBOBOX_FONT = (MAIN_FONT, 11, 'bold italic')
    SPINBOX_FONT = (MAIN_FONT, 11, 'bold')

    PROGRESSBAR_MAXIMUM = 1000

    try:
        with open(f'{path_to_dir_dicts}/countries.json', 'r') as file:
            file_str = json.load(file)
            LIST_COUNTRIES = json.loads(file_str)
    except FileNotFoundError as error:
        logger.warning('Не найден файл "countries.json", парсинг невозможен!')
        LIST_COUNTRIES = {
            'Россия': 1,
            'Украина': 2,
            'Беларусь': 3
        }

    @staticmethod
    def copy_in_clipboard(widget, value):
        """
        Функция управляющая наполнением буфера обмена
        :param widget: виджет от лица которого будет происходить копирование
        :param value: строковое значение, которое надо скопировать
        :return: ничего
        """
        widget.clipboard_clear()
        widget.clipboard_append(value)


LICENSE_AGREEMENT = f"""
Нажимая кнопку "Принять", вы соглашаетесь с собственной ответственностью за ваши действия в программе {SettingsFunction.APP_NAME}, а также они обдуманны.
Нажимая кнопку "Принять",  вы соглашаетесь с тем, что запрещены догадки и бездоказательственные обвинения программы {SettingsFunction.APP_NAME}, а также её автора за причинённые неполадки или заблокированные страницы.
Нажимая кнопку "Принять", вы соглашаетесь с тем, что автор не несёт ответственности за модифицированный или перепакованный исполняемый файл {SettingsFunction.APP_NAME}, за любые случаи, которые затрагивают целостность исполняемого файла {SettingsFunction.APP_NAME}, а также любой вред причинённый программой посредством редактирования содержимого её папки.

Только в случае полного понимания всего вышеописанного, нажмите правой кнопкой мыши на кнопку "Принять". Это сообщение показывается только один раз. В случае, если вы захотите его перечитать, то вы сможете найти его на сайте программы или в официальном боте программы в Telegram, VK.
"""

LABEL_DESCRIPTION = 'Эта программа создана для парсинга целевой аудитории из Vk. Основные инструменты для сбора ЦА находятся во вкладке "Действия"'
LABEL_HELP_DESCRIPTION = 'Помощь по программе можно получить на сайте программы (для перехода нажмите на иконку программы слева, либо на соответствующую кнопку). Либо в боте Vk, Telgram.\n\nВ случае ошибки, вы можете сообщить о ней в соответствующей вкладке программы, либо также в боте программы.\n\n\nПоддержать проект вы можете во вкладке "Донаты"'
STATUS_VK_PERSON = {
    '': 'Не выбрано',
    1: 'не женат (не замужем)',
    2: 'встречается',
    3: 'помолвлен(-а)',
    4: 'женат (замужем)',
    5: 'всё сложно',
    6: 'в активном поиске',
    7: 'влюблен(-а)',
    8: 'в гражданском браке'
}
