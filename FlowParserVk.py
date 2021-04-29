import os
import time
from math import ceil
from shutil import rmtree
from sys import exit as exit_ex
from sys import platform
from time import time as time_now
from tkinter import Label, Tk
from tkinter.messagebox import showerror, showinfo, showwarning
from typing import Union
from webbrowser import open_new_tab as web_open_new_tab

import requests
import vk_api
from _tkinter import TclError
from PIL import Image, ImageTk

from base_data import GetRequestsToDB, MainDB, UpdateRequestsToDB
from settings import (DEFAULT_VALUE_FOR_BD, HTTP_FOR_REQUESTS, HTTP_GET_TOKEN,
                      ID_GROUP_VK, INFO_MSG, LOGGER, REPO_BRANCH_MASTER,
                      REPO_BRANCH_UPDATER, REPO_BRANCH_VERSION,
                      TIME_FREE_VERSION, VERSION_API, WARNING_MSG, path,
                      path_to_dir_ico)
from windows import AdditionalWindows

if platform in ['linux']:
    OS = 'Linux'
elif platform in ['win32', 'cygwin']:
    OS = 'Windows'
else:
    showerror(
        'Платформа не поддерживается',
        f'Неподдерживаемая платформа: {platform}\n\nОбратитесь за помощью '
        'к боту VK'
    )

    exit_ex()


class BrainForApp:
    """
    Класс отвечающий за настройку и запуск приложения
    """

    def __init__(self, window_preview):
        """
        Создаёт превью и проверяет нужные настройки для программы, а также
        запускает её
        :param window_preview: объект окна превью
        """
        self.logger = LOGGER('main', 'main')
        png_preview_open, png_preview = self.preview_image_open()
        self.preview_image_set(png_preview_open, png_preview, window_preview)
        window_preview.update()

        time.sleep(2)
        MainDB()

        get_requests_db = GetRequestsToDB()
        settings = get_requests_db.get_records(
            tb_name=get_requests_db.settings, one_record=True,
            select=['first_start', 'auto_update']
        )

        first_start = settings['first_start']
        auto_update = settings['auto_update']

        if first_start == 1:
            self.logger.info('Первый запуск')
            window_preview.destroy()
            done = AdditionalWindows().person_and_agreement_data()

            if done is True:
                update_requests_db = UpdateRequestsToDB()
                update_requests_db.update_table(
                    tb_name=update_requests_db.settings,
                    update_row={'first_start': 0}
                )

        try:
            window_preview.destroy()
        except TclError as err:
            if str(err) == 'can\'t invoke "destroy" command: application ' \
                           'has been destroyed':
                pass

        self.logger.info('Запуск приложения')

        list_path = os.listdir(path)

        if REPO_BRANCH_UPDATER in list_path:
            rmtree(REPO_BRANCH_UPDATER, ignore_errors=True, onerror=None)

        if REPO_BRANCH_VERSION in list_path:
            rmtree(REPO_BRANCH_VERSION, ignore_errors=True, onerror=None)

        if REPO_BRANCH_MASTER in list_path:
            rmtree(REPO_BRANCH_MASTER, ignore_errors=True, onerror=None)

        from windows import App
        App(auto_update, OS)
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
    """
    Класс отвечающий за нстройку инструментов для запросов к API Vk
    """

    def __init__(self, ignore_existing_token: bool = False):
        self.logger = LOGGER('config_vk_api', 'vk_api')
        get_requests_db = GetRequestsToDB()
        user_data_table_value = get_requests_db.get_records(
            tb_name=get_requests_db.userdata, one_record=True,
            select=['access_token']
        )
        token = user_data_table_value['access_token']
        self.__additional_windows = AdditionalWindows

        if ignore_existing_token is False:
            if (token is None) or (token == DEFAULT_VALUE_FOR_BD):
                token = self.get_token()
        else:
            token = self.get_token()

        if (token is not None) or (token != DEFAULT_VALUE_FOR_BD):
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

    def get_token(self) -> Union[str, None]:
        """
        Функция получения токнеа пользователя
        :return:
        """
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
        update_requests_db = UpdateRequestsToDB()
        update_requests_db.update_table(
            tb_name=update_requests_db.userdata,
            update_row={'access_token': token}
        )

        return token

    @staticmethod
    def check_is_donat(token: str) -> bool:
        """
        Функция проверки оплаты подписки на программу пользователем
        :param token: токен пользователя
        :return:
        """
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
            get_requests_db = GetRequestsToDB()
            __start = GetRequestsToDB().get_records(
                select=['start_free_version'], one_record=True,
                tb_name=get_requests_db.settings
            )['start_free_version']

            if __start is None:
                warning = WARNING_MSG['VK_API']['is_not_donat_free']
                showwarning(
                    'Пробная версия!',
                    warning.format(min=TIME_FREE_VERSION // 60)
                )
                start_free_version = time_now()
                update_request_db = UpdateRequestsToDB()
                update_request_db.update_table(
                    tb_name=update_request_db.settings,
                    update_row={'start_free_version': int(start_free_version)}
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

    def preparation_final_token(self, token: str) -> str:
        """
        Функция обработки ссылки и получения из неё токена
        :param token: ссылка с токеном
        :return:
        """
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

    try:
        app_brain = BrainForApp(master)
    except SystemExit:
        pass
    except BaseException as error:
        showerror(
            'Ошибка',
            f'Произошла непредвиденная ошибка\n\n{error}'
        )
