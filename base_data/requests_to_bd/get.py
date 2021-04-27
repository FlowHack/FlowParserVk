from settings import LOGGER

from ..base_data import MainDB


class GetRequestsToDB(MainDB):

    def get_settings_table_value(self, hide_result=True):
        """
        Функция получения данных настроек программы из базы данных
        :return: словарь со значениями по имени их названия в базе
        """
        self.remote_control_bd.execute('SELECT * FROM AppSettings')
        settings_app = self.remote_control_bd.fetchone()

        auto_update: int = settings_app[0]
        first_start: int = settings_app[1]
        start_free_version = settings_app[2]

        if hide_result is True:
            start_free_version = (settings_app[2], None)[settings_app[2] == 0]

        return {
            'auto_update': auto_update,
            'first_start': first_start,
            'start_free_version': start_free_version
        }

    def get_user_data_table_value(self, hide_result=True):
        """
        Функция получения данных пользователя программы из базы данных
        :return: словарь со значениями по имени их названия в базе
        """
        self.remote_control_bd.execute('SELECT * FROM UserData')
        data_user = self.remote_control_bd.fetchone()

        access_token = data_user[0]
        if hide_result is True:
            access_token = (access_token, None)[access_token == 'none_value']

        return {
            'access_token': access_token
        }

    def get_get_requests_people_table_value(self, hide_result=True):
        """
        Функция получения результатов get запросов пользователей в вк
        :return: список запросов
        """
        self.remote_control_bd.execute('SELECT * FROM GetRequestsApi ORDER BY pk DESC')

        get_people_requests = self.remote_control_bd.fetchall()

        return get_people_requests

    def get_get_requests_people_for_parse(self, name):
        self.remote_control_bd.execute(
            f'''
            SELECT *
            FROM GetRequestsApi
            WHERE (type_request = "{name}") and (last_parse = 1)
            ORDER BY pk DESC
            '''
        )

        get_people_requests = self.remote_control_bd.fetchall()

        return get_people_requests

    def get_one_get_requests_table(self, pk, columns='*'):
        self.remote_control_bd.execute(
            f'SELECT {columns} FROM GetRequestsApi WHERE pk={pk}'
        )

        data = self.remote_control_bd.fetchone()

        if len(data) == 6:
            pk, method, count, result, data, last_parse = \
                data[0], data[1], data[2], data[3], data[4], int(data[5])

            return {
                'pk': pk,
                'method': method,
                'count': count,
                'result': result,
                'data': data,
                'last_parse': last_parse
            }
        else:
            return data