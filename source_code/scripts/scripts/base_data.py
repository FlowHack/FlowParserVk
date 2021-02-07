from sqlite3 import connect

from settings.settings import SettingsFunction

logger = SettingsFunction.get_logger('base_data')


class MainBD:
    def __init__(self):
        """
        Управление созданием базы
        """
        path_to_db = SettingsFunction.path_to_db
        self.connect_bd = connect(path_to_db)
        self.remote_control_bd = self.connect_bd.cursor()
        self.check_availability_db()

    def check_availability_db(self):
        """
        Проверка наличия таблиц в базе
        :return: None
        """
        should_be_table_in_db = {
            'User_data': self.create_user_db,
            'Settings_app': self.create_settings_db,
            'Get_people': self.create_get_people_db

        }
        table_in_bd = list(
            record[0] for record in self.remote_control_bd.execute(
                'SELECT name FROM sqlite_master WHERE type = "table"'
            ).fetchall()
        )
        for table in should_be_table_in_db.items():
            if table[0] not in table_in_bd:
                create_db_function = table[1]
                create_db_function()

    def create_user_db(self):
        """
        Создание таблицы данных пользователя
        :return: None
        """
        self.remote_control_bd.execute(
            '''
            CREATE TABLE IF NOT EXISTS User_data(
            vk_login TEXT, 
            vk_password TEXT
            )
            '''
        )
        self.connect_bd.commit()
        logger.info('Создали базу данных юзера User_data')
        default_params = [('none_value', 'none_value')]
        self.remote_control_bd.executemany(
            'INSERT INTO User_data VALUES (?,?)',
            default_params
        )
        self.connect_bd.commit()
        logger.info('Заполнили бд юзера дефолтными значениями')

    def create_settings_db(self):
        """
        Создание таблицы настроек программы
        :return: None
        """
        self.remote_control_bd.execute(
            '''
            CREATE TABLE IF NOT EXISTS Settings_app(
            auto_update INT NOT NULL,
            first_start INT NOT NULL
            )
            '''
        )
        self.connect_bd.commit()
        logger.info('Создали базу данных настроек')
        default_params = [(1, 1)]
        self.remote_control_bd.executemany(
            'INSERT INTO Settings_app VALUES (?,?)',
            default_params
        )
        self.connect_bd.commit()
        logger.info('Заполнили бд настроек дефолтными значениями')

    def create_get_people_db(self):
        """
        Создаёт таблицу спарсенных данных, тип которых указан в поле type
        :return: None
        """
        self.remote_control_bd.execute(
            '''
            CREATE TABLE IF NOT EXISTS Get_people(
            type_request TEXT,
            date_request TEXT, 
            count_people INT,
            response TEXT,
            params_request TEXT
            )
            '''
        )
        self.connect_bd.commit()
        logger.info('Создали базу данных записей get запросов')


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
            'first_start': first_start,
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
        self.remote_control_bd.execute(
            '''
            CREATE TABLE IF NOT EXISTS Get_people(
            type_request TEXT,
            date_request TEXT,
            count_people INT,
            response TEXT,
            params_request TEXT
            )
            '''
        )
        self.remote_control_bd.execute('SELECT * FROM User_data')

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
                                  auto_update=None, first_start=None):
        """
        Функция обновления настроек программы. Можно подать один из двух
        парметров
        :param auto_update: значение авто обновления (1-да, 0-нет)
        :param first_start: значение первого запуска (1-да, 0-нет)
        :return: ничего
        """
        if (auto_update is None) or (first_start is None):
            settings_app_table_values = \
                RequestGetToBD().get_settings_table_value()
            if auto_update is None:
                auto_update: int = settings_app_table_values['auto_update']
            if first_start is None:
                first_start: int = settings_app_table_values['first_start']

        self.remote_control_bd.execute(
            f'''
            UPDATE Settings_app
            SET auto_update = {auto_update},
            first_start = {first_start}
            '''
        )
        self.connect_bd.commit()
        logger.warning('Обновлены данные таблицы Settings_app')
