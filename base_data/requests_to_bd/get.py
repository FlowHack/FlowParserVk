from typing import Dict, List, Union

from settings import LOGGER, REQUIRES_DATA

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
                if record is None:
                    continue

                response.append({})
                for k in range(len(select)):
                    name = select[k]
                    response[i][name] = record[k]

        LOGGER.warning(f'Успешно получены данные из {tb_name}')
        return response[0] if len(response) == 1 else response

    def get_records_get_requests(self, pk: int,
                                 method: bool = False,
                                 last_parse: bool = False,
                                 ) -> Union[str, Dict[str, str]]:
        """
        Получение результатов парсинга
        :param pk: pk запроса
        :param method: нужно ли вернуть тип запроса default: False
        :param last_parse: нужно ли вернуть last_parse default: False
        :return: str результат
        """
        select = ['response']
        select += ['type_request'] if method is True else []
        select += ['last_parse'] if last_parse is True else []

        record = self.get_records(
            select=select, tb_name=self.get_requests,
            where=f'pk={pk}', one_record=True
        )

        _method_ = record['type_request'] if method is True else method
        _last_parse_ = \
            record['last_parse'] if last_parse is True else last_parse

        if record['response'] == REQUIRES_DATA:
            record = '['

            _record_ = [self.get_records(
                select=['response'], where=f'pk_attachment={pk}',
                tb_name=self.additional_get_requests, one_record=True
            )]
            value = self.get_records(
                select=['response'], where=f'pk_attachment={pk}',
                tb_name=self.additional_get_requests
            )
            if type(value) == dict:
                _record_ += [value]
            else:
                _record_ += value

            record += ', '.join([item['response'] for item in _record_])
            record += ']'
        else:
            record = record['response']

        if (method is False) and (last_parse is False):
            result = record
        else:
            result = {'response': record}
            if method is True:
                result['method'] = _method_
            if last_parse is True:
                result['last_parse'] = int(_last_parse_)

        return result

    def __get_select__(self, tb_name, select):
        return (select, self.columns[tb_name])[select is None]
