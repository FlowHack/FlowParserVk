import requests

from FlowParserVk import ConfigureVkApi
from settings import HTTP_FOR_REQUESTS, LOGGER, VERSION_API

LOGGER = LOGGER('vk_get_request', 'vk_api')


class GetRequestsToVkApi:
    def __init__(self):
        config = ConfigureVkApi()
        token = config.token
        self.vk_tool = config.vk_tool

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
        if self.vk_tool is None:
            raise ValueError('неверный токен')

        response = self.vk_tool.get_all(
            method=api_method, max_count=1000, values=kwargs
        )

        return response
