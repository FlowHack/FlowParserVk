from settings import get_logger

from ..base_data import MainDB

logger = get_logger('get_requests_to_bd')


class GetRequestsToDB(MainDB):

    def get_settings_table_value(self):
        """
        Функция получения данных настроек программы из базы данных
        :return: словарь со значениями по имени их названия в базе
        """
        self.remote_control_bd.execute('SELECT * FROM AppSettings')
        settings_app = self.remote_control_bd.fetchone()

        auto_update: int = settings_app[0]
        first_start: int = settings_app[1]

        return {
            'auto_update': auto_update,
            'first_start': first_start,
        }

    def get_user_data_table_value(self):
        """
        Функция получения данных пользователя программы из базы данных
        :return: словарь со значениями по имени их названия в базе
        """
        self.remote_control_bd.execute('SELECT * FROM UserData')
        data_user = self.remote_control_bd.fetchone()

        vk_login: str = data_user[0]
        vk_password: str = data_user[1]

        return {
            'vk_login': vk_login,
            'vk_password': vk_password
        }

    def get_get_requests_people_table_value(self):
        """
        Функция получения результатов get запросов пользователей в вк
        :return: список запросов
        """
        self.remote_control_bd.execute('SELECT * FROM GetRequestApi')

        get_people_requests = self.remote_control_bd.fetchall()

        return get_people_requests
