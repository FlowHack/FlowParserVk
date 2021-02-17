from settings.settings import get_logger

from .base_data import MainBD

logger = get_logger('request_to_bd')


class RequestGetToBD(MainBD):

    def get_settings_table_value(self):
        """
        Функция получения данных настроек программы из базы данных
        :return: словарь со значениями по имени их названия в базе
        """
        self.remote_control_bd.execute('SELECT * FROM Settings_app')
        settings_app = self.remote_control_bd.fetchone()

        auto_update: int = settings_app[0]
        first_start: int = settings_app[1]

        return {
            'auto_update': auto_update,
            'person_agreement': first_start,
        }

    def get_user_data_table_value(self):
        """
        Функция получения данных пользователя программы из базы данных
        :return: словарь со значениями по имени их названия в базе
        """
        self.remote_control_bd.execute('SELECT * FROM User_data')
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
        self.remote_control_bd.execute('SELECT * FROM Get_people')

        get_people_requests = self.remote_control_bd.fetchall()

        return get_people_requests


class RequestUpdateToBD(MainBD):

    def update_data_on_user_table(self,
                                  new_vk_login: str, new_vk_password: str):
        """
        Функция обновления данных пользователя
        :param new_vk_login: логин вконтакте
        :param new_vk_password: пароль вконтакте
        :return: ничего
        """
        self.remote_control_bd.execute(
            f'''
            UPDATE User_data
            SET vk_login = "{new_vk_login}",
            vk_password = "{new_vk_password}"
            '''
        )
        self.connect_bd.commit()
        logger.warning('Обновлены данные таблицы User_data')

    def update_settings_app_table(self,
                                  auto_update=None, person_agreement=None):
        """
        Функция обновления настроек программы. Можно подать один из двух
        парметров
        :param auto_update: значение авто обновления (1-да, 0-нет)
        :param person_agreement: значение первого запуска (1-да, 0-нет)
        :return: ничего
        """
        if (auto_update is None) or (person_agreement is None):
            settings_app_table_values = \
                RequestGetToBD().get_settings_table_value()
            if auto_update is None:
                auto_update: int = settings_app_table_values['auto_update']
            if person_agreement is None:
                person_agreement: int = \
                    settings_app_table_values['person_agreement']

        self.remote_control_bd.execute(
            f'''
            UPDATE Settings_app
            SET auto_update = {auto_update},
            person_agreement = {person_agreement}
            '''
        )
        self.connect_bd.commit()
        logger.warning('Обновлены данные таблицы Settings_app')
