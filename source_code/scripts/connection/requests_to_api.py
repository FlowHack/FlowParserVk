from math import ceil

from scripts.connection.authorization import Authorize
from settings.settings import SettingsFunction, get_logger
from settings import value_constraints

from vk_api.exceptions import ApiError

logger = get_logger('requests_to_api')


class RequestsAPI:
    def __init__(self):
        self.v_api = SettingsFunction.VERSION_API

    def parsing_search_on_group(self, progressbar=None, **kwargs):
        pass

    def cities_on_region(self, country_id, region_id):
        api = self.authorize_for_get_api()
        if api is None:
            return None

        response = []
        action_arguments = {
            'country_id': country_id,
            'region_id': region_id,
            'need_all': 1
        }
        api_method = api.database.getCities

        json = self.get_all_object(
            api_method=api_method,
            **action_arguments
        )

        for item in json:
            response.append(item['id'])

        return response

    def get_id_group(self, ids):
        api = self.authorize_for_get_api()
        if api is None:
            return None

        try:
            response = api.groups.getById(
                v=self.v_api, group_ids=ids
            )
        except ApiError as error:
            if str(error) == '[100] One of the parameters specified was missing or invalid: group_ids is undefined':
                return None

        group_id = response[0].get('id')

        return group_id

    @staticmethod
    def authorize_for_get_api():
        authorize = Authorize()

        vk_session = authorize.vk_session

        if vk_session is not None:
            api = vk_session.get_api()
        else:
            return None

        return api

    def get_cities(self, country_id, progressbar=None):
        api = self.authorize_for_get_api()
        if api is None:
            return None

        response = {}
        action_arguments = {
            'need_all': 1,
            'country_id': country_id
        }
        api_method = api.database.getCities

        json = self.get_all_object(
            api_method=api_method,
            progressbar=progressbar,
            **action_arguments
        )

        for item in json:
            response[item['title']] = item['id']

        return response

    def get_regions(self, country_id, progressbar=None):
        api = self.authorize_for_get_api()
        if api is None:
            return None

        response = {}
        action_arguments = {
            'country_id': country_id
        }
        api_method = api.database.getRegions

        json = self.get_all_object(
            api_method=api_method,
            progressbar=progressbar,
            **action_arguments
        )

        for item in json:
            response[item['title']] = item['id']

        return response

    def get_all_object(self,
                       api_method, progressbar=None, **kwargs):

        action_arguments = {
            'v': self.v_api,
            'count': 1000,
            'offset': 0
        }
        action_arguments.update(kwargs)

        response = api_method(**action_arguments)
        count_return: int = response.get('count')

        if count_return <= action_arguments.get('count'):
            response_json = response.get('items')
        else:
            progressbar_max = value_constraints.PROGRESSBAR_MAX

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
