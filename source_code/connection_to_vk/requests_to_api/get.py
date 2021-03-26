from math import ceil

from connection_to_vk import ConnectionToVk
from settings import PROGRESSBAR_MAX, SettingsFunctions, get_logger

logger = get_logger('get_requests_to_vk_api')


class GetRequestsToVkApi:
    def __init__(self):
        self.version_api = SettingsFunctions.VERSION_API

        self.api = ConnectionToVk().api

    def get_group_id(self, ids):
        response = self.api.groups.getById(
            v=self.version_api, group_ids=ids
        )

        return response

    def get_all_object(self,
                       api_method, progressbar=None, **kwargs):

        action_arguments = {
            'v': self.version_api,
            'count': 1000,
            'offset': 0
        }
        action_arguments.update(kwargs)

        response = api_method(**action_arguments)
        count_return: int = response.get('count')

        if count_return <= action_arguments.get('count'):
            response_json = response.get('items')
        else:
            progressbar_max = PROGRESSBAR_MAX

            iterations = ceil(count_return / action_arguments.get('count'))
            step_progressbar = progressbar_max / iterations

            iteration = 0
            response_json = response.get('items')
            while iteration < iterations:
                if progressbar is not None:
                    progressbar['value'] += step_progressbar
                    progressbar.update()

                action_arguments['offset'] += 1000
                request = api_method(**action_arguments)
                response_json += request.get('items')

                iteration += 1

        if progressbar is not None:
            progressbar['value'] = 0

        return response_json
