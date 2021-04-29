from typing import List, Union

from settings import LOGGER

from ..base_data import MainDB

LOGGER = LOGGER('db_get', 'base_data')


class GetRequestsToDB(MainDB):
    """
    Класс отвечающий за GET запросы к базе данных
    """

    def __init__(self):
        super().__init__()

    def get_records(self, tb_name: str, select: List[str] = None,
                    one_record: bool = False,
                    where: str = None, order: str = None,
                    limit: Union[str, int] = None,
                    dictionary: bool = True) -> Union[List[dict], dict]:
        """
        Функция получения записей из базы данных
        :param tb_name: название таблицы
        :param select: имена колонн, которые нужно взять default: все
        :param one_record: булево одну ли брать запись default: False
        :param where: параметр выборки default: не используется
        :param order: параметр сортировки default: не используется
        :param limit: параметр ограничения кол-ва строк default: не используется
        :param dictionary: параметр определения вида выходных даных,
        если False, то вернётся читый результат SQL, если True, то словарь
        {столбец: значение} default True
        :return:
        """
        LOGGER.warning(
            f'Начинаю брать данные из {tb_name}'
        )
        response = []
        select = self.__get_select__(tb_name, select)

        LOGGER.info('Собираю запрос')
        request = f'SELECT {", ".join(select)} FROM {tb_name}'
        if where is not None:
            request += f' WHERE {where}'
        if order is not None:
            request += f' ORDER BY {order}'
        if limit is not None:
            request += f' LIMIT {limit}'

        LOGGER.info(f'Получаю данные {request}')
        self.remote_control_bd.execute(request)
        records = (
            [self.remote_control_bd.fetchone()],
            self.remote_control_bd.fetchall()
        )[one_record is False]

        LOGGER.info('Обрабатываю')
        if dictionary is False:
            response = records
        else:
            for i in range(len(records)):
                record = records[i]
                response.append({})
                for k in range(len(select)):
                    name = select[k]
                    response[i][name] = record[k]

        LOGGER.warning(f'Успешно получены данные из {tb_name}')
        return response[0] if len(response) == 1 else response

    def __get_select__(self, tb_name, select):
        return (select, self.columns[tb_name])[select is None]
