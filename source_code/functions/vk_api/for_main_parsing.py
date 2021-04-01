from time import sleep
from time import time as time_now

from settings import LOGGER, PROGRESSBAR_MAX
from vk_api import ConfigureVkApi, GetRequestsToVkApi
from base_data import UpdateRequestsToDB

from .additional import AdditionalFunctionsVkApi


class FunctionsForMainParsing:
    @staticmethod
    def check_values_for_main_parsing(additional_values, json):
        count_people = 0
        result = []

        followers_from = additional_values['followers_from']
        followers_to = additional_values['followers_to']

        if additional_values.get('last_seen'):
            last_seen_need = int(additional_values.get('last_seen'))

        for item in json:
            if item.get('followers_count') is None:
                continue

            followers_count = int(item.get('followers_count'))
            if (followers_count > followers_to) or (followers_count < followers_from):
                continue

            if additional_values.get('last_seen'):
                last_seen = int(item.get('last_seen')['time'])

                if last_seen < last_seen_need:
                    continue

            if additional_values.get('can_send_message'):
                if int(item.get('can_write_private_message')) != 1:
                    continue

            result.append(str(item.get('id')))
            count_people += 1

        return result, count_people

    def main_parsing_city(self, main_values, additional_values, progressbar):
        get_requests_to_vk_api = GetRequestsToVkApi()
        api_method = 'users.search'

        try:
            json = get_requests_to_vk_api.get_all_object(
                api_method=api_method,
                progressbar=progressbar,
                **main_values
            )
        except ValueError as error:
            if str(error) == 'неверный токен':
                return None
            else:
                return None
        response, count_people = self.check_values_for_main_parsing(
            additional_values,
            json
        )

        progressbar['value'] = 0

        return {
            'count_people': count_people,
            'response': response,
        }

    def main_parsing_region(self, main_values, additional_values, progressbar):
        cities = additional_values['cities']
        step_progressbar = PROGRESSBAR_MAX / len(cities)
        get_requests_to_vk_api = GetRequestsToVkApi()
        api_method = 'users.search'
        count_people = 0
        response = []

        for city in cities:
            progressbar['value'] += step_progressbar
            progressbar.update()
            main_values['city'] = city
            sleep(0.2)

            try:
                json = get_requests_to_vk_api.get_all_object(
                    api_method=api_method,
                    **main_values
                )
            except ValueError as error:
                if str(error) == 'неверный токен':
                    return None
                else:
                    return None

            checker = self.check_values_for_main_parsing(additional_values, json)
            response += checker[0]
            count_people += checker[1]

        progressbar['value'] = 0

        return {
            'count_people': count_people,
            'response': response,
        }
