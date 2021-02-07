from logging import INFO, getLogger
from logging.handlers import RotatingFileHandler
from os import getcwd


class SettingsFunction:
    VERSION = '0.1.0'
    path = getcwd()
    path_to_dir_settings = f'{path}/settings'
    path_to_dir_ico = f'{path_to_dir_settings}/ico'
    path_to_dir_style = f'{path_to_dir_settings}/style/awthemes-10.2.0'
    path_to_db = f'{path_to_dir_settings}/settings.db'

    def __init__(self):
        """
        Получение путей до важных элементов программы
        """
        self.path = getcwd()
        self.path_to_settings = f'{self.path}/settings'
        self.path_to_dir_ico = f'{self.path_to_settings}/ico'
        self.path_to_db = f'{self.path_to_settings}/settings.db'

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

LICENSE_AGREEMENT = """Нажимая кнопку "Принять", вы соглашаетесь с собственной ответственностью за ваши действия в программе FlowParserVK, а также они обдуманны.
Нажимая кнопку "Принять",  вы соглашаетесь с тем, что запрещены догадки и бездоказательственные обвинения программы FlowParserVK, а также её автора за причинённые неполадки или заблокированные страницы.
Нажимая кнопку "Принять", вы соглашаетесь с тем, что автор не несёт ответственности за модифицированный или перепакованный исполняемый файл FlowParserVK, за любые случаи, которые затрагивают целостность исполняемого файла FlowParserVK, а также любой вред причинённый программой посредством редактирования содержимого её папки.

Только в случае полного понимания всего вышеописанного, нажмите правой кнопкой мыши на кнопку "Принять". Это сообщение показывается только один раз. В случае, если вы захотите его перечитать, то вы сможете найти его на сайте программы или в официальном боте программы в Telegram.
"""
