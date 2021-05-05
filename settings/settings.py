import os
from logging import INFO, Formatter, getLogger
from logging.handlers import RotatingFileHandler

from settings.additional.variables import APP_NAME, path, path_to_dir_settings


def __get_logger__(name: str, file: str) -> object:
    """
    Функция создания логгера
    :param name: имя файла логгера
    :return: объект логгера
    """
    if 'log' not in os.listdir(path_to_dir_settings):
        os.mkdir(os.path.join(path_to_dir_settings, 'log'))

    file_logger = getLogger(name)
    file_logger.setLevel(INFO)

    logger_format = (
        '[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s'
    )
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = Formatter(fmt=logger_format, datefmt=date_format)

    handler = RotatingFileHandler(
        fr'settings/log/{file}.log',
        maxBytes=5252880,
        backupCount=5,
    )

    handler.setFormatter(formatter)
    file_logger.addHandler(handler)

    return file_logger


LOGGER = __get_logger__

path_agreement = os.path.join(path, 'PERSON_AGREEMENT.txt')
with open(path_agreement, 'r', encoding='utf-8') as person_agreement:
    LICENSE_AGREEMENT = person_agreement.read().strip().format(
        APP_NAME=APP_NAME
    )

LABEL_DESCRIPTION = 'Эта программа создана для парсинга целевой аудитории из Vk. Основные инструменты для сбора ЦА находятся во вкладке "Действия"'
LABEL_HELP_DESCRIPTION = 'Помощь по программе можно получить в боте программы (для перехода нажмите на соответствующую кнопку).\n\nВ случае ошибки, вы можете сообщить о ней вcё там же, либо в сообществе в Vk.'
