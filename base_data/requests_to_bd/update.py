from typing import Dict, List, Union

from base_data import GetRequestsToDB, MainDB
from settings import LOGGER

LOGGER = LOGGER('db_update', 'base_data')


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
