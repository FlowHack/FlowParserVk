from base_data import GetRequestsToDB, MainDB
from settings import get_logger

logger = get_logger('update_requests_to_bd')


class UpdateRequestsToDB(MainDB):

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
            UPDATE UserData
            SET vk_login = "{new_vk_login}",
            vk_password = "{new_vk_password}"
            '''
        )
        self.connect_bd.commit()
        logger.warning('Обновлены данные таблицы UserData')

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
                GetRequestsToDB().get_settings_table_value()
            if auto_update is None:
                auto_update: int = settings_app_table_values['auto_update']
            if person_agreement is None:
                person_agreement: int = \
                    settings_app_table_values['first_start']

        self.remote_control_bd.execute(
            f'''
            UPDATE AppSettings
            SET auto_update = {auto_update},
            first_start = {person_agreement}
            '''
        )
        self.connect_bd.commit()
        logger.warning('Обновлены данные таблицы AppSettings')
