from sqlite3 import connect
from typing import List, Union
from .requests_to_bd.variables_create import *

from settings import LOGGER, path_to_db

LOGGER = LOGGER('main_db', 'base_data')


class MainDB:
    """
    Класс отвечающий за подключени базы данных, её настройку и создание
    """

    def __init__(self):
        self.settings = 'AppSettings'
        self.userdata = 'UserData'
        self.get_requests = 'GetRequestsApi'
        self.additional_get_requests = 'AdditionalGetRequestsApi'
        self.columns = {
            self.settings: [
                'auto_update', 'first_start', 'start_free_version'
            ],
            self.userdata: ['access_token'],
            self.get_requests: [
                'pk', 'type_request', 'count_people', 'response',
                'time_request', 'last_parse'
            ],
            self.additional_get_requests: ['pk_attachment', 'response']
        }

        self.connect_bd = connect(path_to_db)
        self.remote_control_bd = self.connect_bd.cursor()
        self.check_availability_db()

    def check_availability_db(self) -> None:
        """
        Проверка наличия нужных таблиц в базе данных и создание их в случае их
        отсутствия
        :return:
        """
        should_be_table_in_db = {
            self.userdata: lambda: self.create_db(
                tb_name=self.userdata, request=USER_DATA_DB,
                data=USER_DATA_DEFAULT
            ),
            self.settings: lambda: self.create_db(
                tb_name=self.settings, request=SETTINGS_DB,
                data=SETTINGS_DEFAULT

            ),
            self.get_requests: lambda: self.create_db(
                tb_name=self.get_requests, request=GET_REQUESTS_DB
            ),
            self.additional_get_requests: lambda: self.create_db(
                tb_name=self.additional_get_requests,
                request=ADDITIONAL_GET_REQUEST_DB
            )
        }
        table_in_bd = [
            record[0] for record in self.remote_control_bd.execute(
                'SELECT name FROM sqlite_master WHERE type = "table"'
            ).fetchall()
        ]

        for table, func in should_be_table_in_db.items():
            if table not in table_in_bd:
                func()

    def create_db(self, tb_name: str, request: str,
                  data: List[Union[str, int]] = None) -> None:
        """
        Функция создания таблиц и заполнения их дефолтными значениями
        :param tb_name: имя таблицы
        :param request: запрос к sqlite на создание таблицы
        :param data: список со значениями для заполнения default: None
        :return:
        """
        LOGGER.warning(f'Начинаю создание таблицы {tb_name}')
        self.remote_control_bd.execute(request.format(tb_name=tb_name))
        self.connect_bd.commit()
        LOGGER.warning('Удачно создана')

        if data is None:
            return

        LOGGER.warning(f'Начинаю default заполнение {tb_name}')
        data = ', '.join(data)
        self.remote_control_bd.execute(
            f'INSERT INTO {tb_name} VALUES ({data})'
        )
        self.connect_bd.commit()
        LOGGER.warning('Удачно заполнена')
