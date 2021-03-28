from time import time as time_now

from connection_to_vk import ConnectionToVk, GetRequestsToVkApi
from settings import SettingsFunctions, get_logger

from .additional import AdditionalFunctionsVkApi
from settings import PROGRESSBAR_MAX

logger = get_logger('additional_functions_for_windows')


class FunctionsForRequestToAPI(AdditionalFunctionsVkApi, GetRequestsToVkApi):
    def __init__(self):
        super().__init__()
        self.settings_app = SettingsFunctions()

    def get_all_cities(self, country_id, progressbar=None):
        api = ConnectionToVk().api
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

    def get_all_regions(self, country_id, progressbar=None):
        api = ConnectionToVk().api
        if api is None:
            return None

        response = {}
        action_arguments = {
            'country_id': country_id
        }
        api_method = self.api.database.getRegions

        json = self.get_all_object(
            api_method=api_method,
            progressbar=progressbar,
            **action_arguments
        )

        for item in json:
            response[item['title']] = item['id']

        return response

    def get_all_cities_in_region(self, country_id, region_id):
        api = ConnectionToVk().api
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

    def sort_group_id(self, ids):
        group_id = self.get_group_id(ids)
        group_id = group_id[0].get('id')

        return group_id

    def main_parsing_city(self, main_values, additional_values):
        pass

    def main_parsing_region(self, main_values, additional_values, progressbar):
        api = ConnectionToVk().api
        if api is None:
            return None

        cities = additional_values['cities']
        step_progressbar = PROGRESSBAR_MAX / len(cities)
        api_method = api.users.search
        response = []

        for city in cities:
            progressbar['value'] += step_progressbar
            progressbar.update()
            main_values['city'] = city

            json = self.get_all_object(
                api_method=api_method,
                **main_values
            )
            print(json)

            response.append(json)

        print(response)
