from sqlite3 import connect

from settings import SettingsFunctions, get_logger

logger = get_logger('base_data')


class MainDB:
    def __init__(self):
        """
        Управление созданием базы
        """
        path_to_db = SettingsFunctions.path_to_db
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
            'GetRequestApi': self.create_get_people_db

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
            vk_login TEXT NOT NULL, 
            vk_password TEXT NOT NULL
            )
            '''
        )
        self.connect_bd.commit()
        logger.info('Создали базу данных юзера User_data')
        default_params = [('none_value', 'none_value')]
        self.remote_control_bd.executemany(
            'INSERT INTO UserData VALUES (?,?)',
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
            CREATE TABLE IF NOT EXISTS AppSettings(
            auto_update INT NOT NULL,
            first_start INT NOT NULL
            )
            '''
        )
        self.connect_bd.commit()
        logger.info('Создали базу данных настроек')
        default_params = [(1, 1)]
        self.remote_control_bd.executemany(
            'INSERT INTO AppSettings VALUES (?,?)',
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
            CREATE TABLE IF NOT EXISTS GetRequestApi(
            pk INT PRIMARY KEY,
            type_request TEXT NOT NULL, 
            count_people INT NOT NULL,
            response TEXT NOT NULL,
            params_request TEXT NOT NULL,
            datetime_request INT NOT NULL
            )
            '''
        )
        self.connect_bd.commit()
        logger.info('Создали базу данных записей get запросов')