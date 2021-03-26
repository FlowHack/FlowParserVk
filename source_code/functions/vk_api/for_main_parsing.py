from time import time as time_now

from connection_to_vk import ConnectionToVk, GetRequestsToVkApi
from settings import SettingsFunctions, get_logger

from .additional import AdditionalFunctionsVkApi

logger = get_logger('additional_functions_for_windows')


class FunctionsForAPI(AdditionalFunctionsVkApi, GetRequestsToVkApi):
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
        group_id = self.sort_group_ids(ids)

        group_id = self.get_group_id(group_id)
        group_id = group_id[0].get('id')

        return group_id

    def main_parsing_city(self, widgets, cities):
        pass

    def main_parsing_region(self, widgets, regions):
        main_values, additional_values = self.get_values_for_main_parsing(
            widgets=widgets,
            city_or_region='region',
            regions=regions
        )
        print(main_values)
        print(additional_values)

        if 'last_only' in additional_values.keys():
            last_only = additional_values['last_only']
            last_only = time_now() - (int(last_only) * 24 * 60 * 60)
            additional_values['last_only'] = last_only
