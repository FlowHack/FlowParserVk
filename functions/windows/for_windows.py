import datetime
import gc
import json
import os
import shutil
import subprocess
import tempfile
import zipfile
from json.decoder import JSONDecodeError
from sys import exit as exit_ex
from tkinter.messagebox import (askyesno, askyesnocancel, showerror, showinfo,
                                showwarning)
from typing import List, Union

import requests
from _tkinter import TclError
from requests.exceptions import ConnectionError

from base_data import COUNT_MANY_INSERT, GetRequestsToDB, UpdateRequestsToDB
from my_vk_api import (EASY_PARSE_BY_GROUP_CODE, PARSE_BY_GROUP_CODE,
                       ConfigureVkApi, GetRequestsToVkApi)
from settings import (ALCOHOL, ASKS, ERROR_MSG, FOLLOWERS_MAX,
                      HTTP_FOR_REQUESTS, INFO_MSG, LAST_SEEN_MAX, LIFE_MAIN,
                      LIST_COUNTRIES, LOGGER, NAME_PARSING, PEOPLE_MAIN,
                      POLITICAL, PROGRESSBAR_MAX, REPO_BRANCH_UPDATER,
                      REPO_URL_UPDATER, REPO_URL_VERSION, REQUIRES_DATA,
                      SMOKING, STATUS_VK_PERSON, UPDATE_LINUX, UPDATE_WIN,
                      VERSION, VERSION_API, WARNING_MSG,
                      configure_progress_lbl, path, path_to_updater,
                      path_to_version, styles, time_now)

from .additional import AdditionalFunctionsForWindows

LOGGER = LOGGER('func_win', 'windows')


class FunctionsForWindows:
    """
    Класс отвечающий за основные функции для окон
    """

    def __init__(self):
        self.additional_functions = AdditionalFunctionsForWindows()

    def check_update(self, os_name: str, call: bool = False) -> None:
        """
        Проверка наличия обновлений
        :param os_name: имя OS
        :param call: булево принудительно ли отправлен запрос на проверку
        обновлений default: False
        :return:
        """
        version = os.path.join(path_to_version, 'version.txt')

        try:
            LOGGER.info('Клонируем version')
            response = requests.get(REPO_URL_VERSION)

            with tempfile.TemporaryFile() as file:
                file.write(response.content)
                with zipfile.ZipFile(file) as fzip:
                    fzip.extractall(path)

        except ConnectionError as error:
            LOGGER.error(
                f'Произошла ошибка при клонировании проекта {error}'
            )
            if call is True:
                showerror(
                    'Невозможно выполнить обновление',
                    ERROR_MSG['Update_app']['Bad_connect'].format(VERSION)
                )

            return

        with open(version, 'r', encoding='utf-8') as file:
            file = file.readline().strip().split('&')

        shutil.rmtree(path_to_version, ignore_errors=True, onerror=None)

        version = file[0].strip()
        v_int = [int(item) for item in version.split('.')]
        version_old = [item for item in VERSION.split('.')]
        v_old_int = [int(item) for item in version_old]
        info = file[1]

        condition_1 = v_int[0] > v_old_int[0]
        condition_2 = v_int[0] >= v_old_int[0] and v_int[1] > v_old_int[1]
        condition_3 = \
            v_int[0] >= v_old_int[0] and v_int[1] >= v_old_int[1] and \
            v_int[2] > v_old_int[2]
        need_update = (False, True)[condition_1 or condition_2 or condition_3]

        if (call is True) and (need_update is False):
            showinfo(
                'Обновление не требуется',
                INFO_MSG['Update_app']['Not_need_update'].format(version)
            )

        if need_update is True:
            answer = askyesnocancel(
                'Требуется обновление',
                ASKS['Update_app']['Need_update'].format(
                    version=version, info=info
                )
            )

            if answer is False:
                return
            if answer is None:
                LOGGER.info('Отмена автообновлений')
                update_request_db = UpdateRequestsToDB()
                update_request_db.update_table(
                    tb_name=update_request_db.settings,
                    update_row={'auto_update': 0}
                )
                return
            if answer is True:
                try:
                    self.update_app(os_name)
                except ConnectionError as error:
                    LOGGER.error(
                        f'Невозможно обновиться {os_name} -> {error}'
                    )
                    showerror(
                        'Невозможно выполнить обновление',
                        ERROR_MSG['Update_app']['Bad_connect'].format(VERSION)
                    )

    @staticmethod
    def update_app(os_name: str) -> None:
        """
        Скачивание программы обновления и запуск обновлений
        :param os_name: имя OS
        :return:
        """
        LOGGER.info(f'Клонируем проект {os_name}')

        response = requests.get(REPO_URL_UPDATER)

        with tempfile.TemporaryFile() as file:
            file.write(response.content)
            with zipfile.ZipFile(file) as fzip:
                fzip.extractall(path)

        if os_name == 'Windows':
            command = os.path.join(path_to_updater, UPDATE_WIN)
            subprocess.Popen(command, cwd=path_to_updater)
            exit_ex()

        if os_name == 'Linux':
            os.system(f'chmod -R 775 {path_to_updater}')

            showwarning(
                'Обновление',
                WARNING_MSG['Update_app']['Linux'].format(
                    branch=REPO_BRANCH_UPDATER, file=UPDATE_LINUX
                )
            )
            exit_ex()

    @staticmethod
    def update_label_count_group(widgets: dict) -> None:
        """
        Функция обновления Label количества ссылок на группы
        :param widgets: словарь {ключ: виджет}
        :return:
        """
        text, lbl = widgets['txt_groups'], widgets['lbl_count']
        text = text.get('1.0', 'end')
        additional_functions = AdditionalFunctionsForWindows

        try:
            count = additional_functions.get_groups_from_text(text)['count']
            lbl.configure(text='Количество: ' + str(count))
        except ValueError as error:
            showwarning(
                'Неверный id',
                f'Проверьте ваши id, среди них есть неверный!\n\n{error}'
            )

    def parsing_groups(self, widgets: dict) -> None:
        """
        Функция парсинга по группам
        :param widgets: словарь {ключ: виджет}
        :return:
        """
        progressbar, text = widgets['progressbar'], widgets['txt_groups']
        lbl_progress = widgets['lbl_progress']
        easy_parse = int(widgets['var_easy_parse'].get())
        text = text.get('1.0', 'end')

        try:
            additional_functions = AdditionalFunctionsForWindows
            values = additional_functions.get_groups_from_text(text)
            ids = values['ids']
            length_ids = values['count']
        except ValueError as error:
            showwarning(
                'Неверный id',
                f'Проверьте ваши id, среди них есть неверный!\n\n{error}'
            )
            return

        last_parse = (1, 0)[easy_parse == 1]

        try:
            count, pk = self.__parsing_by_groups__(
                lbl=lbl_progress, progressbar=progressbar,
                length_ids=length_ids,
                ids=ids,
                last_parse=last_parse
            )
        except ConnectionError as error:
            showerror(
                'Нет подключения',
                ERROR_MSG['Parsing']['Bad_connection'].format(str(error))
            )
            return

        if count == 0:
            showinfo(
                'Не найдено пользователей',
                INFO_MSG['Parsing']['none_people_by_groups']
            )

        if count > 0:
            update_request_db = UpdateRequestsToDB()
            update_request_db.update_table(
                tb_name=update_request_db.get_requests,
                update_row={'count_people': count},
                where=f'pk={pk}'
            )

        configure_progress_lbl(progressbar, lbl_progress, 0)
        gc.collect()

    def __parsing_by_groups__(self, lbl: object, length_ids: int,
                              ids: list, progressbar: object,
                              last_parse: int) -> Union[None, List[int]]:
        """
        Функция с алгоритмом парсинга по группам
        :param lbl: Label прогресса
        :param length_ids: len для list ids
        :param ids: list с id групп
        :param progressbar: Progressbar
        :param last_parse: Возможен ли дальнейший парсинг
        :return: список [количество, pk]
        """
        url = HTTP_FOR_REQUESTS.format(method='execute')
        code, request_count = ([PARSE_BY_GROUP_CODE, 11000],
                               [EASY_PARSE_BY_GROUP_CODE, 25000]
                               )[last_parse != 1]
        type_request, pk, count = NAME_PARSING['by_groups'], None, 0
        self.result, vk_params = [], {'group_id': ''}

        for i in range(length_ids):
            token = ConfigureVkApi().token
            if token is None:
                showerror(
                    'Неверный токен',
                    ERROR_MSG['Parsing']['Bad_token']
                )
                return

            lbl_text = f'Прогресс: {i}/{length_ids}. Не прекращайте ' \
                       f'работу, это займёт пару минут...'
            configure_progress_lbl(progressbar, lbl, pg_value := 0, lbl_text)

            offset, i_response, json_error = 0, 0, 0
            vk_params['group_id'] = ids[i]

            while True:
                try:
                    params = {
                        'v': VERSION_API,
                        'access_token': token,
                        'code': code.format(offset=offset, vk_params=vk_params)
                    }

                    response = requests.get(url, params=params)
                    response = response.json()

                    if response.get('execute_errors') or response.get('error'):
                        if i == length_ids - 1:
                            break
                        else:
                            continue

                    response = response['response']
                    count_id = int(response['count_id'])
                    offset = int(response['offset'])
                    vk_result = response['result']
                    count += len(vk_result)
                    self.result += vk_result
                    json_error = 0
                    del vk_result, response

                    lbl_text = f'Прогресс: {i}/{length_ids}. Запрос: ' \
                               f'{i_response}/{count_id // request_count}. ' \
                               'Не прекращайте работу, это займёт пару ' \
                               'минут... '
                    step = PROGRESSBAR_MAX / (count_id / request_count)
                    pg_value += step
                    configure_progress_lbl(
                        progressbar, lbl, pg_value, lbl_text
                    )

                    if offset >= count_id:
                        if count > 0:
                            pk = self.__update_db__(
                                pk, self.result, last_parse, type_request
                            )
                        del self.result
                        self.result = []
                        gc.collect()
                        break
                    if len(self.result) >= COUNT_MANY_INSERT:
                        pk = self.__update_db__(
                            pk, self.result, last_parse, type_request
                        )
                        del self.result
                        self.result = []
                        gc.collect()

                    offset += 1000
                    i_response += 1
                    gc.collect()

                except JSONDecodeError as error:
                    LOGGER.error(f'Ошибка при парсинге по группам {error}')
                    if json_error == 3:
                        if i == length_ids - 1:
                            break
                        else:
                            continue
                    else:
                        json_error += 1

        if len(self.result) > 0:
            pk = self.__update_db__(pk, self.result, last_parse, type_request)

        del offset, last_parse, type_request, self.result
        gc.collect()
        return [count, pk]

    @staticmethod
    def __update_db__(attachment_pk: int, res_peoples: list, last_parse: int,
                      type_request: str) -> Union[None, int]:
        """
        Функция добавления записи в базу
        :param attachment_pk: к какому pk прикреплять
        :param res_peoples: что нужно записать
        :param last_parse: возможен ли дальнейший парсинг
        :param type_request: тип запроса
        :return: attachment_pk
        """
        if len(res_peoples) == 0:
            return
        get_request_db = GetRequestsToDB()
        update_request_db = UpdateRequestsToDB()

        if attachment_pk is None:
            update_request_db.insert_in_table(
                tb_name=update_request_db.get_requests,
                data=[
                    type_request, 0, REQUIRES_DATA, time_now(),
                    last_parse
                ]
            )
            attachment_pk = get_request_db.get_records(
                tb_name=get_request_db.get_requests,
                select=['pk'],
                one_record=True, order='pk DESC'
            )
            get_request_db.connect_bd.close()
            attachment_pk = int(attachment_pk['pk'])

        peoples = json.dumps(res_peoples, ensure_ascii=False)[1:-1]
        update_request_db.insert_in_table(
            tb_name=update_request_db.additional_get_requests,
            data=[attachment_pk, peoples]
        )

        del peoples
        del res_peoples
        gc.collect()
        return attachment_pk

    @staticmethod
    def setting_region_city(widgets: dict) -> None:
        """
        Функция для радиобаттона регион/город
        :param widgets: словарь {ключ: виджет}
        :return:
        """
        var, cmb = widgets['var_city_region'], widgets['cmb_city_region']

        if var.get() == 0:
            var.set(1)
            cmb['value'] = []
            cmb.set('Нажмите "Настройка"')
        elif var.get() == 1:
            var.set(0)
            cmb['value'] = []
            cmb.set('Нажмите "Настройка"')

    @staticmethod
    def setting_only(widgets: dict) -> None:
        """
        Функция настройки радиобаттона онлайн ли пользователь
        :param widgets: словарь {ключ: виджет}
        :return:
        """
        var, chk = widgets['var_only'], widgets['chk_need_last_seen']
        lbl, lbl_to = widgets['lbl_last_seen'], widgets['lbl_last_seen_to']
        spn_from, spn_to = widgets['spn_last_seen_from'], widgets[
            'spn_last_seen_to']
        day = widgets['lbl_last_seen_day']

        if var.get() == 0:
            var.set(1)
            chk.grid_remove()
            lbl.grid_remove()
            lbl_to.grid_remove()
            spn_from.grid_remove()
            spn_to.grid_remove()
            day.grid_remove()
        elif var.get() == 1:
            var.set(0)
            chk.grid()
            lbl.grid()
            lbl_to.grid()
            spn_from.grid()
            spn_to.grid()
            day.grid()

    def setting_before_parsing(self, widgets: dict) -> None:
        """
        Функция загрузки регионов/городов перед парсингом
        :param widgets: словарь {ключ: виджет}
        :return:
        """
        var_need_country = widgets['var_need_country']
        if var_need_country.get() == 0:
            showwarning(
                'Не выбрана страна',
                'Для настройки нужно включить пасинг по стране и выбрать её.'
            )
            return

        var_need_city_region = widgets['var_need_city_region']
        if var_need_city_region.get() == 0:
            showwarning(
                'Не включен парсинг по региону/городу',
                'Вы не включили парсинг по региону/стране'
            )
            return

        country = widgets['var_country'].get()
        country_id = LIST_COUNTRIES[country]

        var_city_region = widgets['var_city_region']
        cmb_city_region = widgets['cmb_city_region']

        lbl_progress = widgets['lbl_progress']
        lbl_progress.configure(
            text='Подождите, идёт загрузка данных...', foreground='red'
        )
        lbl_progress.update()

        try:
            if var_city_region.get() == 0:
                cities = self.additional_functions.get_cities(country_id)
                __var_city_region__ = list(cities.keys())
                cmb_city_region['value'] = __var_city_region__
                cmb_city_region.set(__var_city_region__[0])
            else:
                regions = self.additional_functions.get_regions(country_id)
                __var_city_region__ = list(regions.keys())
                cmb_city_region['value'] = __var_city_region__
                cmb_city_region.set(__var_city_region__[0])
        except ConnectionError:
            showerror(
                'Нет подключения',
                'Подключение к интернету не установлено, настройка невозможна'
                '\n\n{error}'
            )

        configure_progress_lbl(lbl=lbl_progress)

    def parsing_by_groups(self, widgets: dict) -> None:
        """
        Парсинг по критериям
        :param widgets: словарь {ключ: виджет}
        :return:
        """
        pk = widgets['entry_pk'].get().strip()
        if bool(pk) is False:
            showerror(
                'Не выбрана запись',
                ERROR_MSG['Parsing']['Dont_choose_pk']
            )
            return
        pk = int(pk)

        need_country = widgets['var_need_country'].get()
        need_city_region = widgets['var_need_city_region'].get()
        var_city_region = widgets['var_city_region'].get()
        cmb_city_region = widgets['cmb_city_region'].get()
        need_followers = widgets['var_need_count_followers'].get()
        need_data = widgets['var_need_old'].get()
        need_relationship = widgets['var_need_relationship'].get()
        need_political = widgets['var_need_political'].get()
        need_life_main = widgets['var_need_life_main'].get()
        need_people_main = widgets['var_need_people_main'].get()
        need_smoking = widgets['var_need_smoking'].get()
        need_alcohol = widgets['var_need_alcohol'].get()
        need_entry_status = widgets['var_need_entry_status'].get()
        need_entry_about = widgets['var_need_entry_about'].get()
        need_last_seen = widgets['var_need_last_seen'].get()
        sex = widgets['var_sex'].get()
        send_message = widgets['var_can_send_message'].get()
        online = widgets['var_only'].get()
        photos = widgets['var_has_photo'].get()
        deactivated = widgets['var_deactivate'].get()

        lbl_progress = widgets['lbl_progress']
        progressbar = widgets['progressbar']

        followers_from, followers_to, data_from, data_to = 0, 0, 0, 0
        relationship, last_seen_from, last_seen_to, political = 0, 0, 0, 0
        people_main, life_main, smoking, alcohol, entry_status = 0, 0, 0, 0, ''
        entry_about, country, city, cities = '', 0, 0, []

        if (need_country == 0) and (need_city_region == 1):
            need = askyesno(
                'Не включена настройка',
                ASKS['Parsing']['Dont_enable_country']
            )
            if need is False:
                return

            need_city_region = 0

        if need_city_region == 1 and cmb_city_region == 'Нажмите "Настройка"':
            need = askyesno(
                'Не сделана настройка',
                ASKS['Parsing']['Dont_settings']
            )
            if need is False:
                return

            need_city_region = 0

        if need_followers == 1:
            try:
                followers_from = widgets['var_followers_from'].get()
                followers_to = widgets['var_followers_to'].get()
            except TclError:
                showerror(
                    'Неверное значение',
                    ERROR_MSG['Parsing']['Validate_follower']['Not_int']
                )
                return
            if followers_from > followers_to:
                showerror(
                    'Неверное значение',
                    ERROR_MSG['Validate_follower']['Not_int']['From_more_to']
                )
                return
            if (followers_from > FOLLOWERS_MAX) or (
                    followers_to > FOLLOWERS_MAX):
                showerror(
                    'Неверное значение',
                    ERROR_MSG['Validate_follower']
                    ['Not_int']['Max_value'].format(FOLLOWERS_MAX)
                )
                return
        if need_data == 1:
            data_from = int(widgets['var_old_from'].get())
            data_to = int(widgets['var_old_to'].get())

            if data_from > data_to:
                showerror(
                    'Неверное значение',
                    ERROR_MSG['Parsing']['Validate_old']['From_more_to']
                )
                return

        if need_relationship == 1:
            relationship = widgets['var_relationship'].get()
            relationship = STATUS_VK_PERSON[relationship]

        if (online == 0) and (need_last_seen == 1):
            try:
                last_seen_from = widgets['var_last_seen_from'].get()
                last_seen_to = widgets['var_last_seen_to'].get()
            except TclError:
                showerror(
                    'Неверное значение',
                    ERROR_MSG['Parsing']['Validate_last_seen']['Not_int']
                )
                return
            if last_seen_from > last_seen_to:
                showerror(
                    'Неверное значение',
                    ERROR_MSG['Parsing']['Validate_last_seen']['From_more_to']
                )
                return
            if (last_seen_from > LAST_SEEN_MAX) or (
                    last_seen_to > LAST_SEEN_MAX):
                showerror(
                    'Неверное значение',
                    ERROR_MSG['Parsing']['Validate_last_seen']['Max_value']
                )
                return

        if need_political == 1:
            political = widgets['var_political'].get()
            political = POLITICAL[political]

        if need_people_main == 1:
            people_main = widgets['var_people_main'].get()
            people_main = PEOPLE_MAIN[people_main]

        if need_life_main == 1:
            life_main = widgets['var_life_main'].get()
            life_main = LIFE_MAIN[life_main]

        if need_smoking == 1:
            smoking = widgets['var_smoking'].get()
            smoking = SMOKING[smoking]

        if need_alcohol == 1:
            alcohol = widgets['var_alcohol'].get()
            alcohol = ALCOHOL[alcohol]

        if need_entry_status == 1:
            entry_status = widgets['var_entry_status'].get().strip()
            if entry_status == '':
                showerror(
                    'Неверное значение',
                    ERROR_MSG['Parsing']['Validate_status']['Empty']
                )
                return

        if need_entry_about == 1:
            entry_about = widgets['var_entry_about'].get().strip()

            if entry_about == '':
                showerror(
                    'Неверное значение',
                    ERROR_MSG['Parsing']['Validate_about']['Empty']
                )
                return

        if need_country == 1:
            country = widgets['var_country'].get()
            country = LIST_COUNTRIES[country]

        if need_city_region == 1:
            city_region = widgets['var_city_region'].get()

            if city_region == 0:
                city = widgets['cmb_city_region'].get()
                city = self.additional_functions.cities['cities'][city]
            else:
                region = widgets['cmb_city_region'].get()
                region = self.additional_functions.regions['regions'][region]

                params = {
                    'country_id': country,
                    'region_id': region,
                    'need_all': 1
                }
                cities_res = GetRequestsToVkApi().get_all_object(
                    'database.getCities', **params
                )
                cities = []
                for item in cities_res['items']:
                    cities.append(item['id'])

        lbl_progress.configure(text='Подождите...')
        lbl_progress.update()
        get_requests_db = GetRequestsToDB()

        records = get_requests_db.get_records(
            tb_name=get_requests_db.get_requests,
            select=['response', 'count_people'], where=f'pk={pk}',
            one_record=True
        )
        count_peoples = records['count_people']
        step = PROGRESSBAR_MAX / count_peoples
        pg_value = 0
        records = records['response']
        iteration = 0
        result = []

        lbl_text = f'Прогресс {iteration}/{count_peoples}. Подождите, ' \
                   'это может занять несколько минут... '
        configure_progress_lbl(
            progressbar, lbl_progress, pg_value, lbl_text
        )

        if records != REQUIRES_DATA:
            pks = [json.loads(f'[{records}]')]
        else:
            pks = get_requests_db.get_records(
                tb_name=get_requests_db.additional_get_requests,
                select=['pk'], where=f'pk_attachment={pk}', dictionary=False
            )
            pks = [item[0] for item in pks]
        del records
        gc.collect()
        for pk in pks:
            if type(pk) == str or type(pk) == int:
                record = get_requests_db.get_records(
                    tb_name=get_requests_db.additional_get_requests,
                    select=['response'], where=f'pk={pk}', one_record=True
                )['response']
                record = json.loads(f'[{record}]')
            else:
                record = pk

            for item in record:
                iteration += 1
                lbl_text = f'Прогресс {iteration}/{count_peoples}. ' \
                           'Подождите, это может занять несколько минут... '
                pg_value += step
                configure_progress_lbl(
                    progressbar, lbl_progress, pg_value, lbl_text
                )

                if deactivated == 1:
                    if item.get('deactivated'):
                        continue
                else:
                    if item.get('deactivated'):
                        result.append(item['id'])
                        continue

                if need_country == 1:
                    if item.get('country'):
                        if item['country']['id'] != country:
                            continue
                    else:
                        continue

                if need_city_region == 1:
                    if var_city_region == 0:
                        if item.get('city'):
                            if item['city']['id'] != city:
                                continue
                        else:
                            continue
                    else:
                        if item.get('city'):
                            if item['city']['id'] not in cities:
                                continue
                        else:
                            continue

                if need_followers == 1:
                    if item.get('followers_count'):
                        count = item['followers_count']
                        if followers_from > count > followers_to:
                            continue
                    else:
                        continue

                if need_data == 1:
                    if item.get('bdate'):
                        bdate = item['bdate'].split('.')
                        if len(bdate) != 3:
                            pass
                        else:
                            year_now = int(datetime.datetime.now().year)
                            date_from = year_now - data_from
                            date_to = year_now - data_to
                            bdate = int(bdate[2])

                            if date_from <= bdate or bdate <= date_to:
                                del year_now, date_from, date_to, bdate
                                continue

                            del year_now, date_from, date_to, bdate

                if need_relationship == 1:
                    if item.get('relation'):
                        if item['relation'] != relationship:
                            continue
                    else:
                        continue

                if sex != 0:
                    if item.get('sex'):
                        if item['sex'] != sex:
                            continue
                    else:
                        continue

                if send_message == 1:
                    if item.get('can_write_private_message'):
                        if item['can_write_private_message'] != 1:
                            continue
                    else:
                        continue

                if online == 1:
                    if item.get('online'):
                        if item['online'] != 1:
                            continue
                    else:
                        continue

                if (online == 0) and (need_last_seen == 1):
                    if item.get('online'):
                        time = time_now()
                        time_from = time - (last_seen_from * 24 * 60 * 60)
                        time_to = time - (last_seen_to * 24 * 60 * 60)
                        if (item['online'] < time_from) or (
                                item['online'] > time_to):
                            continue
                    else:
                        continue

                if photos == 1:
                    if item.get('has_photo'):
                        if item['has_photo'] != 1:
                            continue
                    else:
                        continue

                if (need_political == 1) or (need_life_main == 1) or (
                        need_people_main == 1) \
                        or (need_smoking == 1) or (need_alcohol == 1):
                    if item.get('personal'):
                        personal = item['personal']

                        if need_political == 1:
                            if personal.get('political'):
                                if personal['political'] != political:
                                    continue
                            else:
                                continue

                        if need_life_main == 1:
                            if personal.get('life_main'):
                                if personal['life_main'] != life_main:
                                    continue
                            else:
                                continue

                        if need_people_main == 1:
                            if personal.get('people_main'):
                                if personal['people_main'] != people_main:
                                    continue
                            else:
                                continue

                        if need_smoking == 1:
                            if personal.get('smoking'):
                                if personal['smoking'] != smoking:
                                    continue
                            else:
                                continue

                        if need_alcohol == 1:
                            if personal.get('alcohol'):
                                if personal['alcohol'] != alcohol:
                                    continue
                            else:
                                continue
                    else:
                        continue

                if need_entry_about == 1:
                    if item.get('about'):
                        if entry_about not in item['about']:
                            continue
                    else:
                        continue

                if need_entry_status == 1:
                    if item.get('status'):
                        if entry_status not in item['status']:
                            continue
                    else:
                        continue

                result.append(item['id'])
            del pk, record
            gc.collect()

        lbl_progress.configure(
            text='Запись данных', foreground=styles.NOTABLE_LABEL_FONT
        )
        lbl_progress.update()

        count = len(result)

        if count == 0:
            configure_progress_lbl(lbl=lbl_progress)

            showinfo(
                'Не найдено пользователей',
                INFO_MSG['Parsing']['none_value_by_criteria']
            )
            return

        configure_progress_lbl(
            progressbar, lbl_progress, 0, 'Запись результатов',
            styles.NOTABLE_LABEL_FONT
        )

        type_request = NAME_PARSING['by_criteria']
        UpdateRequestsToDB().insert_many_values_into_get_requests(
            type_request=type_request,
            count=count, response=result, time=time_now(), last_parse=0
        )
        configure_progress_lbl(
            lbl=lbl_progress
        )

        del result, pks, lbl_text
        gc.collect()
