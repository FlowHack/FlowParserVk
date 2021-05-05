import json
from time import sleep
from typing import Dict, List, Union

from base_data import GetRequestsToDB, MainDB
from settings import LOGGER, REQUIRES_DATA

LOGGER = LOGGER('db_update', 'base_data')
COUNT_MANY_INSERT = 50000


class UpdateRequestsToDB(MainDB):
    """
    Класс отвечающий за UPDATE запросы к базе данных
    """

    def __init__(self):
        super().__init__()

    def update_table(self, tb_name: str,
                     update_row: Dict[str, Union[str, int]],
                     where: str = None) -> None:
        """
        функция выполняющая обноление данных таблицы
        :param tb_name: имя таблицы
        :param update_row: словарь {колонка: значение}
        :param where: параметры выборки запии default: не используется
        :return:
        """
        update_row_values = self.__get_update_row__(
            tb_name, update_row, where=where
        )

        request = 'UPDATE {tb_name} SET {set}'
        if where is not None:
            request += f' WHERE {where}'

        SET = []

        for key, value in update_row_values.items():
            if type(value) == int:
                SET += [f'{key}={value}']
            else:
                SET += [f'{key}="{value}"']

        SET = ', '.join(SET)
        request = request.format(tb_name=tb_name, set=SET)

        LOGGER.info(f'Обновляю данные {request}')
        self.remote_control_bd.execute(request)
        self.connect_bd.commit()

        LOGGER.warning(f'Обновлены данные таблицы {tb_name}')

    def insert_in_table(self, tb_name: str,
                        data: List[Union[str, int]]) -> None:
        """
        Функция вставляющая запись в таблицу
        :param tb_name: имя таблицы
        :param data: список со значениями
        :return:
        """
        LOGGER.warning(f'Начинаю добавлять даные в таблицу {tb_name}')

        columns = self.columns[tb_name]

        if tb_name == self.get_requests:
            del (columns[columns.index('pk')])

        question_marks = ', '.join(['?'] * len(columns))
        columns = ', '.join(columns)

        request = f'''
        INSERT INTO {tb_name} ({columns}) 
        VALUES ({question_marks})
        '''

        self.remote_control_bd.execute(request, data)
        self.connect_bd.commit()

        LOGGER.warning(f'Добавлены данные в таблицу {tb_name}')

    def insert_many_values_into_get_requests(self, type_request: str,
                                             count: int, response: List[dict],
                                             time: float,
                                             last_parse: int) -> None:
        """
        Функция вставки данных в таблицу GET запросов к Vk в том случае.
        Создана потому что Windows плохо работает если нужно большое
        количество данных вставить в БД
        :param type_request: тип парсинга
        :param count: количество людей
        :param response: результат выполнения парсинга
        :param time: время парсинга
        :param last_parse: возможен ли дальнейший парсинг по данным
        :return:
        """
        if count <= COUNT_MANY_INSERT:
            # Если норм количество людей в записи
            peoples = json.dumps(response, ensure_ascii=False)
            self.insert_in_table(
                tb_name=self.get_requests,
                data=[type_request, count, peoples, time, last_parse]
            )
        else:
            # Если слишком много людей в записи
            get_request_db = GetRequestsToDB()
            self.insert_in_table(  # Вставка заглушки в основную тб
                tb_name=self.get_requests,
                data=[
                    type_request, count, REQUIRES_DATA, time, last_parse
                ]
            )
            pk = get_request_db.get_records(
                tb_name=self.get_requests,
                select=['pk'],
                one_record=True, order='pk DESC'
            )
            attachment_pk = int(pk['pk'])
            slice_from = 0
            slice_to = COUNT_MANY_INSERT + 1

            while True:
                sleep(0.2)
                peoples = response[slice_from:slice_to]
                peoples = json.dumps(peoples, ensure_ascii=False)[1:-1]
                self.insert_in_table(
                    tb_name=self.additional_get_requests,
                    data=[attachment_pk, peoples]
                )

                if slice_to == count + 1:
                    break
                slice_from = slice_to
                if slice_to + COUNT_MANY_INSERT + 1 > count + 1:
                    slice_to = count + 1
                else:
                    slice_to += COUNT_MANY_INSERT + 1

    def __get_update_row__(self, tb_name: str, update_row: dict,
                           where: str) -> dict:
        rows = self.columns[tb_name]

        if len(rows) == len(update_row):
            return update_row

        get_requests_db = GetRequestsToDB()
        values = get_requests_db.get_records(
            tb_name=tb_name, where=where, one_record=True
        )

        for item in rows:
            if item not in update_row:
                update_row[item] = values[item]

        return update_row
