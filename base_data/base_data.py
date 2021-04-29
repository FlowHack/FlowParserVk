from sqlite3 import connect

from settings import DEFAULT_VALUE_FOR_BD, LOGGER, path_to_db

LOGGER = LOGGER('main_bd', 'base_data')


class MainDB:
    """
    Класс отвечающий за подключени базы данных, её настройку и создание
    """

    def __init__(self):
        self.connect_bd = connect(path_to_db)
        self.remote_control_bd = self.connect_bd.cursor()
        self.check_availability_db()

        self.columns = {
            'AppSettings': [
                'auto_update', 'first_start', 'start_free_version'
            ],
            'UserData': ['access_token'],
            'GetRequestsApi': [
                'pk', 'type_request', 'count_people', 'response',
                'time_request', 'last_parse'
            ]
        }
        self.settings = 'AppSettings'
        self.userdata = 'UserData'
        self.get_requests = 'GetRequestsApi'

    def check_availability_db(self) -> None:
        """
        Проверка наличия нужных таблиц в базе данных и создание их в случае их
        отсутствия
        :return:
        """
        should_be_table_in_db = {
            'UserData': self.create_user_db,
            'AppSettings': self.create_settings_db,
            'GetRequestsApi': self.create_get_people_db

        }
        table_in_bd = list(
            record[0] for record in self.remote_control_bd.execute(
                'SELECT name FROM sqlite_master WHERE type = "table"'
            ).fetchall()
        )
        for table, func in should_be_table_in_db.items():
            if table not in table_in_bd:
                func()

    def create_user_db(self) -> None:
        """
        Создание таблицы данных пользователя и её дефолтное заполнение
        :return:
        """
        self.remote_control_bd.execute(
            '''
            CREATE TABLE IF NOT EXISTS UserData(
            access_token TEXT NOT NULL
            )
            '''
        )
        self.connect_bd.commit()
        LOGGER.info('Создали базу данных юзера User_data')
        self.remote_control_bd.execute(
            f'INSERT INTO UserData VALUES ("{DEFAULT_VALUE_FOR_BD}")'
        )
        self.connect_bd.commit()
        LOGGER.info('Заполнили бд юзера дефолтными значениями')

    def create_settings_db(self) -> None:
        """
        Функция создания базы данных настроек и её дефолтное заполнение
        :return:
        """
        self.remote_control_bd.execute(
            '''
            CREATE TABLE IF NOT EXISTS AppSettings(
            auto_update INTEGER NOT NULL,
            first_start INTEGER NOT NULL,
            start_free_version INTEGER NOT NULL
            )
            '''
        )
        self.connect_bd.commit()
        LOGGER.info('Создали базу данных настроек')
        self.remote_control_bd.execute(
            'INSERT INTO AppSettings VALUES (1,1,0)'
        )
        self.connect_bd.commit()
        LOGGER.info('Заполнили бд настроек дефолтными значениями')

    def create_get_people_db(self):
        """
        Функция создания базы данных запросов к апи
        :return:
        """
        self.remote_control_bd.execute(
            '''
            CREATE TABLE IF NOT EXISTS GetRequestsApi(
            pk INTEGER PRIMARY KEY NOT NULL,
            type_request TEXT NOT NULL, 
            count_people INTEGER NOT NULL,
            response TEXT NOT NULL,
            time_request INTEGER NOT NULL,
            last_parse INTEGER NOT NULL
            )
            '''
        )
        self.connect_bd.commit()
        LOGGER.info('Создали базу данных записей get запросов')
