from math import ceil
from time import sleep
from tkinter.messagebox import showwarning

import requests
import vk_api

from settings import (HTTP_FOR_REQUESTS, LOGGER, PROGRESSBAR_MAX, VERSION_API,
                      WARNING_MSG)

from ..configure_connect_to_api import ConfigureVkApi


class GetRequestsToVkApi:
    def __init__(self):
        config = ConfigureVkApi()
        token = config.token
        self.vk_tool = config.vk_tool

        if (token is None) or (self.vk_tool is None):
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

    def get_all_object(self, api_method, **kwargs):
        response = self.vk_tool.get_all(method=api_method, max_count=1000, values=kwargs)

        return response
