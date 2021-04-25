from sqlite3 import connect

from settings import DEFAULT_VALUE_FOR_BD, LOGGER, path_to_db

LOGGER = LOGGER('main_bd', 'base_data')


class MainDB:
    def __init__(self):
        """
        Управление созданием базы
        """
        self.connect_bd = connect(path_to_db)
        self.remote_control_bd = self.connect_bd.cursor()
        self.check_availability_db()

    def check_availability_db(self):
        """
        Проверка наличия таблиц в базе
        :return: None
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

    def create_settings_db(self):
        """
        Создание таблицы настроек программы
        :return: None
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
        Создаёт таблицу спарсенных данных, тип которых указан в поле type
        :return: None
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
