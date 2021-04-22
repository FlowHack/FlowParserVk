import os
import time
from shutil import rmtree
from tkinter import Label, Tk
from tkinter.messagebox import showerror, showinfo, showwarning
from webbrowser import open_new_tab as web_open_new_tab

import requests
import vk_api
from _tkinter import TclError
from PIL import Image, ImageTk

from base_data import GetRequestsToDB, MainDB, UpdateRequestsToDB
from settings import (DEFAULT_VALUE_FOR_BD, HTTP_FOR_REQUESTS, HTTP_GET_TOKEN,
                      ID_GROUP_VK, INFO_MSG, LOGGER, TIME_FREE_VERSION,
                      VERSION_API, WARNING_MSG, path, path_to_dir_ico)
from windows import AdditionalWindows


class BrainForApp:

    def __init__(self, window_preview):
        """
        Создаёт превью и проверяет нужные настройки для программы
        :param window_preview: объект окна превью
        """
        self.logger = LOGGER('main', 'main')
        png_preview_open, png_preview = self.preview_image_open()
        self.preview_image_set(png_preview_open, png_preview, window_preview)
        window_preview.update()

        time.sleep(2)
        MainDB()

        settings = GetRequestsToDB().get_settings_table_value()
        first_start = settings['first_start']
        auto_update = settings['auto_update']

        if first_start == 1:
            self.logger.info('Первый запуск')
            window_preview.destroy()
            done = AdditionalWindows().person_and_agreement_data()

            if done is True:
                UpdateRequestsToDB().update_settings_app_table(
                    person_agreement=0
                )

        try:
            window_preview.destroy()
        except TclError as err:
            if str(err) == 'can\'t invoke "destroy" command: application ' \
                             'has been destroyed':
                pass

        self.logger.info('Запуск приложения')

        list_path = os.listdir(path)

        if 'updater' in list_path:
            rmtree('updater', ignore_errors=True, onerror=None)

        if 'tmp' in list_path:
            rmtree('tmp', ignore_errors=True, onerror=None)

        from windows import App
        App(auto_update)
        self.logger.info('Закрытие приложения')

    def preview_image_open(self):
        """
        Возвращает первью картинку
        """
        while True:
            try:
                png_preview_open = Image.open(
                    os.path.join(path_to_dir_ico, 'preview.png')
                )
                png_preview = ImageTk.PhotoImage(png_preview_open)
                return png_preview_open, png_preview
            except FileNotFoundError as err:
                self.logger.error(str(err))

    @staticmethod
    def preview_image_set(png_preview_open, png_preview, window_preview):
        """
        Устанавливает размеры окна, ставит его по середине, устанавливает
        картинку как фон
        """
        x_img, y_img = png_preview_open.size
        x = (window_preview.winfo_screenwidth() - x_img) // 2
        y = (window_preview.winfo_screenheight() - y_img) // 2
        window_preview.geometry("%ix%i+%i+%i" % (x_img, y_img, x, y))
        Label(window_preview, image=png_preview).pack(side='top')


class ConfigureVkApi:
    def __init__(self, ignore_existing_token=False):
        self.logger = LOGGER('config_vk_api', 'vk_api')
        user_data_table_value = GetRequestsToDB().get_user_data_table_value()
        token = user_data_table_value['access_token']
        self.__additional_windows = AdditionalWindows

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

        if self.token is not None:
            vk_session = vk_api.VkApi(token=self.token)
            self.vk_tool = vk_api.tools.VkTools(vk_session)

            if ignore_existing_token is True:
                showinfo(
                    'Авторизовались',
                    'Вы удачно авторизовались!'
                )
            self.logger.info('Получен vk_tool и сам токен')
        else:
            self.logger.error('vk_tool не удалось получить')
            self.vk_tool = None

    def get_token(self):
        showinfo('Получение токена!', INFO_MSG['VK_API']['get_token'])
        web_open_new_tab(HTTP_GET_TOKEN)

        token = self.__additional_windows().get_token()
        token = self.preparation_final_token(token)

        if token == DEFAULT_VALUE_FOR_BD:
            LOGGER.warning(
                'При выполнении функции get_token был получен невалидный токен'
            )
            return None

        params = {
            'v': VERSION_API,
            'access_token': token
        }

        try:
            request = requests.get(
                HTTP_FOR_REQUESTS.format(method='users.get'),
                params=params
            ).json()
        except ConnectionError:
            showerror(
                'Нет подключения',
                'Не возиожно авторизоваться, нетп подключения к интернету'
            )
            return None

        if request.get('error'):
            showerror(
                'Авторизация не удалась',
                'Неверный токен авторизации, произошла ошибка, '
                'повторите попытку'
            )
            return None

        UpdateRequestsToDB().update_data_on_user_table(token)

        return token

    @staticmethod
    def check_is_donat(token):
        return True
        params = {
            'v': VERSION_API,
            'access_token': token,
            'owner_id': ID_GROUP_VK
        }

        try:
            request = requests.get(
                HTTP_FOR_REQUESTS.format(method='donut.isDon'),
                params=params
            ).json()
        except ConnectionError:
            showerror(
                'Нет подключения',
                'Невозможно авторизоваться, нет подключения к интернету'
            )
            return False

        if request.get('error'):
            showerror(
                'Ошибка',
                f'Произошла непредвиденная ошибка {request["error"]}'
            )

        response = request.get('response')

        if int(response) == 1:
            return True
        else:
            __start = GetRequestsToDB().get_settings_table_value()[
                'start_free_version'
            ]

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

    def preparation_final_token(self, token):
        token = token.split('access_token=')

        if len(token) == 2:
            token = token[1].split('&')[0]
            return token

        showwarning(
            'Не смог распознать токен',
            WARNING_MSG['VK_API']['non_inspected_token']
        )
        self.logger.warning(
            'При выполнении preparation_final_token, не смог распознать токен'
        )

        return DEFAULT_VALUE_FOR_BD


if __name__ == '__main__':
    master = Tk()
    master.overrideredirect(True)

    app_brain = BrainForApp(master)
