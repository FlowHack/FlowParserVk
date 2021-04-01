from time import time as time_now
from tkinter.messagebox import showinfo, showwarning
from webbrowser import open_new_tab as web_open_new_tab
from math import ceil

import requests

from base_data import GetRequestsToDB, UpdateRequestsToDB
from settings import (DEFAULT_VALUE_FOR_BD, HTTP_FOR_REQUESTS, HTTP_GET_TOKEN,
                      ID_GROUP_VK, INFO_MSG, LOGGER, TIME_FREE_VERSION,
                      VERSION_API, WARNING_MSG)
from windows import AdditionalWindows


class ConfigureVkApi:
    def __init__(self, ignore_existing_token=False):
        user_data_table_value = GetRequestsToDB().get_user_data_table_value()
        token = user_data_table_value['access_token']
        self.additional_windows = AdditionalWindows

        if ignore_existing_token is False:
            if token is None:
                token = self.get_token()
        else:
            token = self.get_token()

        if token is not None:
            is_donat = self.check_is_donat(token)
            if is_donat is False:
                token = None

        self.token = token

    def get_token(self):
        showinfo('Получение токена!', INFO_MSG['VK_API']['get_token'])
        web_open_new_tab(HTTP_GET_TOKEN)

        token = self.additional_windows().get_token()
        token = self.preparation_final_token(token)

        UpdateRequestsToDB().update_data_on_user_table(token)

        if token == DEFAULT_VALUE_FOR_BD:
            LOGGER.warning(
                'При выполнении функции get_token был получен невалидный токен'
            )
            return None

        return token

    @staticmethod
    def check_is_donat(token):
        return True
        params = {
            'v': VERSION_API,
            'access_token': token,
            'owner_id': ID_GROUP_VK
        }
        request = requests.get(
            HTTP_FOR_REQUESTS.format(method='donut.isDon'),
            params=params
        ).json()

        response = request.get('response')
        if response is None:
            print(request.get('error'))

        if int(response) == 1:
            return True
        else:
            __start = GetRequestsToDB().get_settings_table_value()['start_free_version']

            if __start is None:
                warning = WARNING_MSG['VK_API']['is_not_donat_free']
                showwarning(
                    'Пробная версия!',
                    warning.format(min=TIME_FREE_VERSION // 60)
                )
                start_free_version = time_now()
                UpdateRequestsToDB().update_settings_app_table(
                    start_free_version=int(start_free_version)
                )
                return True
            else:
                time_use_free_version = ceil(time_now()) - int(__start)

                if time_use_free_version >= TIME_FREE_VERSION:
                    warning = WARNING_MSG['VK_API']['is_not_donat']
                    showwarning(
                        'Пробная версия!',
                        warning
                    )
                    return False
                else:
                    time_left = TIME_FREE_VERSION - time_use_free_version

                    warning = WARNING_MSG['VK_API']['is_not_donat_free']
                    showwarning(
                        'Пробная версия!',
                        warning.format(min=time_left // 60)
                    )
                    return True

    @staticmethod
    def preparation_final_token(token):
        token = token.split('access_token=')

        if len(token) == 2:
            token = token[1].split('&')[0]
            return token

        if len(token) == 1:
            token = token[0]
            return token

        showwarning(
            'Не смог распознать токен', WARNING_MSG['VK_API']['non_inspected_token']
        )
        LOGGER.warning(
            'При выполнении preparation_final_token, не смог распознать токен'
        )

        return DEFAULT_VALUE_FOR_BD
