from typing import Dict, List, Union

import requests
from time import sleep

from my_vk_api import (EASY_PARSE_BY_GROUP_CODE, PARSE_BY_GROUP_CODE,
                       ConfigureVkApi)
from settings import HTTP_FOR_REQUESTS, PROGRESSBAR_MAX, VERSION_API


class ParsingVk:
    """
    Функция отвечающая за парсинг данных
    """

    @staticmethod
    def parse_by_groups(progressbar: object, lbl_progress: object,
                        ids: List[Union[str, int]],
                        last_parse: int) -> Union[
        None, Dict[str, Union[List[dict], int]]
    ]:
        """
        Функция парсящая пользователей по группам
        :param progressbar: виджет програссбар
        :param lbl_progress: виджет Label для вывода прогресса
        :param ids: список id групп
        :param last_parse: возможен ли будет дальнейший парсинг по этой выборке
        :return: Dict{'result': результат, 'count': количество пользоваиелей}
        """
        ids = list(ids)
        length = len(ids)
        vk_params = {'group_id': ''}
        url = HTTP_FOR_REQUESTS.format(method='execute')
        result = []

        if last_parse == 1:
            code = PARSE_BY_GROUP_CODE
            request_count = 11000
        else:
            code = EASY_PARSE_BY_GROUP_CODE
            request_count = 24000

        for i in range(length):
            token = ConfigureVkApi().token
            if token is None:
                return None

            lbl_progress.configure(
                text=f'Прогресс: {i}/{length}. Не прекращайте '
                     f'работу, это займёт пару минут...')
            lbl_progress.update()

            offset = 0
            i_response = 0
            group_id = ids[i]
            vk_params['group_id'] = group_id

            while True:
                params = {
                    'v': VERSION_API,
                    'access_token': token,
                    'code': code.format(
                        offset=offset, vk_params=vk_params
                    )
                }

                sleep(0.3)
                response = requests.get(url, params=params).json()

                if response.get('execute_errors') or response.get('error'):
                    if i == length - 1:
                        break
                    else:
                        continue

                response = response['response']
                offset = int(response['offset'])
                count_id = int(response['count_id'])
                vk_result = response['result']
                result += vk_result
                i_response += 1

                lbl_progress.configure(
                    text=
                    f'Прогресс: {i + 1}/{length}. '
                    f'Запрос: {i_response - 1}/{count_id // request_count}. '
                    f'Не прекращайте работу, это займёт пару минут...'
                )
                lbl_progress.update()
                step = PROGRESSBAR_MAX / (count_id / request_count)
                progressbar['value'] += step
                progressbar.update()
                if offset >= count_id:
                    break

                offset += 1000

            progressbar['value'] = 0
            progressbar.update()

        lbl_progress.configure(text='')
        count = len(result)

        return {'result': result, 'count': count}
