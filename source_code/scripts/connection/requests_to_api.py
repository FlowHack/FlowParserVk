from math import ceil

from scripts.connection.authorization import Authorize
from settings.settings import SettingsFunction, get_logger

logger = get_logger('requests_to_api')


class RequestsAPI(Authorize):
    def __init__(self):
        authorize = Authorize()
        self.vk_session = authorize.vk_session
        self.api = self.vk_session.get_api()
        self.v_api = SettingsFunction.VERSION_API

    def get_response(self, api_method, progressbar, **kwargs):
        count = 1000
        offset = 0
        action_arguments = {
            'v': self.v_api,
            'count': count,
            'offset': offset
        }
        action_arguments.update(**kwargs)
        if api_method == 'database.getCities':
            action = self.api.database.getCities
            action_arguments['need_all'] = 1
        elif api_method == 'database.getRegions':
            action = self.api.database.getRegions
        elif api_method == 'users.search':
            action = self.api.users.search
        else:
            action = None

        result_dict = {}
        result_list = []
        request = action(**action_arguments)
        print(request)
        count_return: int = request.get('count')
        if count_return > count:
            need_iteration = ceil(count_return / count)
            step_progressbar = \
                SettingsFunction.PROGRESSBAR_MAXIMUM / need_iteration
            iteration = 0
            result_json = request.get('items')
            while iteration < need_iteration:
                progressbar['value'] += step_progressbar
                progressbar.update()
                action_arguments['offset'] += 1000
                request = action(**action_arguments)
                result_json += request.get('items')
                iteration += 1
        else:
            result_json = request.get('items')

        progressbar['value'] = 0
        print(result_json)
        if api_method == 'users.search':
            for item in result_json:
                result_list.append(item['id'])

            return result_list

        else:
            for item in result_json:
                result_dict[item['title']] = item['id']

            return result_dict
