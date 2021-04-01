from math import ceil
from time import sleep
from tkinter.messagebox import showwarning

import requests

from settings import (HTTP_FOR_REQUESTS, LOGGER, PROGRESSBAR_MAX, VERSION_API,
                      WARNING_MSG)

from ..configure_connect_to_api import ConfigureVkApi


class GetRequestsToVkApi:
    def __init__(self):
        token = ConfigureVkApi().token
        if token is None:
            showwarning('Неверный токен', WARNING_MSG['VK_API']['bad_token'])
            LOGGER.warning('Получен неверный токен при GET запросе')

        self.default_params = {
            'v': VERSION_API,
            'access_token': token
        }

    def get_group_id(self, ids):
        if self.default_params['access_token'] is None:
            raise ValueError('неверный токен')

        params = {
            'group_ids': ids
        }
        params = {**self.default_params, **params}

        response = requests.get(
            HTTP_FOR_REQUESTS.format(method='groups.getById'),
            params=params
        ).json().get('response')

        return response

    def get_all_object(self, api_method, progressbar=None, **kwargs):
        if self.default_params['access_token'] is None:
            raise ValueError('неверный токен')

        params = {
            'count': 1000,
            'offset': 0
        }
        params = {**params, **kwargs, **self.default_params}

        request = requests.get(
            HTTP_FOR_REQUESTS.format(method=api_method),
            params=params
        ).json()
        count_return: int = request.get('response').get('count')


        if count_return <= params.get('count'):
            response_json = request.get('response').get('items')
        else:
            progressbar_max = PROGRESSBAR_MAX

            iterations = ceil(count_return / params.get('count'))
            step_progressbar = progressbar_max / iterations

            iteration = 0
            response_json = request.get('response').get('items')
            while iteration < iterations:
                if progressbar is not None:
                    progressbar['value'] += step_progressbar
                    progressbar.update()

                params['offset'] += 1000
                sleep(0.2)

                request = requests.get(
                    HTTP_FOR_REQUESTS.format(method=api_method),
                    params=params
                ).json()
                response_json += request.get('response').get('items')

                iteration += 1

        if progressbar is not None:
            progressbar['value'] = 0

        return response_json
