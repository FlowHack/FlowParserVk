from time import sleep

import requests

from my_vk_api import (EASY_PARSE_BY_GROUP_CODE, PARSE_BY_GROUP_CODE,
                       ConfigureVkApi)
from settings import HTTP_FOR_REQUESTS, PROGRESSBAR_MAX, VERSION_API


class ParsingVk:
    @staticmethod
    def parse_by_groups(progressbar, lbl_progress, ids: list, last_parse: int):
        ids = list(ids)
        length = len(ids)
        vk_params = {'group_id': ''}
        url = HTTP_FOR_REQUESTS.format(method='execute')
        result = []

        if last_parse == 1:
            code = PARSE_BY_GROUP_CODE
        else:
            code = EASY_PARSE_BY_GROUP_CODE

        for i in range(length):
            token = ConfigureVkApi().token
            if token is None:
                return None

            lbl_progress.configure(text=f'Прогресс: {i}/{length}. Не прекращайте '
                                        f'работу, это займёт пару минут...')
            lbl_progress.update()

            offset = 0
            i_response = 0
            group_id = ids[i]
            vk_params['group_id'] = group_id

            while True:
                if last_parse is True:
                    pass
                params = {
                    'v': VERSION_API,
                    'access_token': token,
                    'code': code.format(
                        offset=offset, vk_params=vk_params
                    )
                }

                response = requests.get(url, params=params).json()

                response = response['response']
                offset = int(response['offset'])
                count_id = int(response['count_id'])
                vk_result = response['result']
                result += vk_result
                i_response += 1

                lbl_progress.configure(
                    text=
                    f'Прогресс: {i+1}/{length}. '
                    f'Запрос: {i_response-1}/{count_id//11000}. '
                    f'Не прекращайте работу, это займёт пару минут...'
                )
                lbl_progress.update()
                step = PROGRESSBAR_MAX/(count_id/11000)
                progressbar['value'] += step
                progressbar.update()
                if offset >= count_id:
                    break

                offset += 1000
                sleep(0.3)

            progressbar['value'] = 0
            progressbar.update()

        lbl_progress.configure(text='')
        count = len(result)

        return {'result': result, 'count': count}
