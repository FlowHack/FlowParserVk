from logging import INFO, getLogger
from logging.handlers import RotatingFileHandler
from os import getcwd


class SettingsFunction:
    VERSION = '0.1.0'
    APP_NAME = 'FlowParserVK'
    PAGE_APP = ''
    TELEGRAM_BOT_APP = ''
    VK_BOT_APP = ''

    path = getcwd()
    path_to_dir_settings = f'{path}/settings'
    path_to_dir_ico = f'{path_to_dir_settings}/ico'
    path_to_dir_style = f'{path_to_dir_settings}/style/awthemes-10.2.0'
    path_to_db = f'{path_to_dir_settings}/settings.db'

    MAIN_FONT = 'Times New Roman'
    H1_FONT = (MAIN_FONT, 20, 'bold italic')
    H5_FONT = (MAIN_FONT, 14, 'bold italic')
    H6_FONT = (MAIN_FONT, 12, 'bold italic')
    INPUT_FONT = (MAIN_FONT, 10, 'bold italic')

    @staticmethod
    def get_logger(name: str) -> object:
        """
        Функция создания логгера
        :param name: имя файла логгера
        :return: объект логгера
        """
        logger = getLogger('__name__')
        logger.setLevel(INFO)
        handler = RotatingFileHandler(
            fr'settings/log/{name}.log',
            maxBytes=50000000,
            backupCount=5,
        )
        logger.addHandler(handler)

        return logger


LICENSE_AGREEMENT = f"""
Нажимая кнопку "Принять", вы соглашаетесь с собственной ответственностью за ваши действия в программе {SettingsFunction.APP_NAME}, а также они обдуманны.
Нажимая кнопку "Принять",  вы соглашаетесь с тем, что запрещены догадки и бездоказательственные обвинения программы {SettingsFunction.APP_NAME}, а также её автора за причинённые неполадки или заблокированные страницы.
Нажимая кнопку "Принять", вы соглашаетесь с тем, что автор не несёт ответственности за модифицированный или перепакованный исполняемый файл {SettingsFunction.APP_NAME}, за любые случаи, которые затрагивают целостность исполняемого файла {SettingsFunction.APP_NAME}, а также любой вред причинённый программой посредством редактирования содержимого её папки.

Только в случае полного понимания всего вышеописанного, нажмите правой кнопкой мыши на кнопку "Принять". Это сообщение показывается только один раз. В случае, если вы захотите его перечитать, то вы сможете найти его на сайте программы или в официальном боте программы в Telegram, VK.
"""

LABEL_DESCRIPTION = 'Эта программа создана для парсинга целевой аудитории из Vk. Основные инструменты для сбора ЦА находятся во вкладке "Действия"'
LABEL_HELP_DESCRIPTION = 'Помощь по программе можно получить на сайте программы (для перехода нажмите на иконку программы слева). Либо в боте Vk, Telgram.\n\nВ случае ошибки, вы можете сообщить о ней в соответствующей вкладке программы, либо также в боте программы.'
