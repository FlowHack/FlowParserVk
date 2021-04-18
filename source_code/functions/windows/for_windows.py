import json
from time import time as time_now
from time import strptime, mktime
from tkinter.messagebox import askyesno, showinfo, showwarning

from base_data import UpdateRequestsToDB, GetRequestsToDB
from settings import (FOLLOWERS_MAX, FRIENDS_MAX, LAST_SEEN_MAX,
                      LIST_COUNTRIES, LOGGER, NAME_PARSING, STATUS_VK_PERSON,
                      POLITICAL, PEOPLE_MAIN, LIFE_MAIN, SMOKING, ALCOHOL,
                      PROGRESSBAR_MAX)

from ..vk_api import ParsingVk
from .additional import AdditionalFunctionsForWindows
from my_vk_api import GetRequestsToVkApi
from _tkinter import TclError


class FunctionsForWindows:
    def __init__(self):
        self.additional_functions = AdditionalFunctionsForWindows()

    @staticmethod
    def update_label_count_group(widgets):
        text, lbl = widgets['txt_groups'], widgets['lbl_count']
        text = text.get('1.0', 'end')

        try:
            count = AdditionalFunctionsForWindows.get_groups_from_text(text)[
                'count']
            lbl.configure(text='Количество: ' + str(count))
        except ValueError as error:
            if str(error) == 'неверный id':
                showwarning(
                    'Неверный id',
                    'Проверьте ваши id, среди них есть неверный!'
                )

    @staticmethod
    def parsing_groups(widgets):
        progressbar, text = widgets['progressbar'], widgets['txt_groups']
        lbl_progress = widgets['lbl_progress']
        easy_parse = int(widgets['var_easy_parse'].get())
        text = text.get('1.0', 'end')

        if easy_parse == 1:
            last_parse = 0
        else:
            last_parse = 1
        time = time_now()

        try:
            ids = AdditionalFunctionsForWindows.get_groups_from_text(text
                                                                     )['ids']
        except ValueError as error:
            if str(error) == 'неверный id':
                showwarning(
                    'Неверный id',
                    'Проверьте ваши id, среди них есть неверный!'
                )
                return

        values = ParsingVk.parse_by_groups(progressbar, lbl_progress, ids,
                                           last_parse)

        count, peoples = values['count'], values['result']

        if count == 0:
            showinfo(
                'Не найдено пользователей',
                'Пользователи не найдены!\n\nВозможно, что лимит запросов '
                'на сегодня исчерпан!'
            )
            return

        peoples = json.dumps(peoples, ensure_ascii=False)

        UpdateRequestsToDB().update_get_people_bd(
            type_request=NAME_PARSING['by_groups'], count_people=count, time=time,
            response=peoples,
            last_parse=int(last_parse)
        )

    @staticmethod
    def setting_region_city(widgets):
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
    def setting_only(widgets):
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

    def setting_before_parsing(self, widgets):
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

        lbl_progress.configure(text='', foreground='white')
        lbl_progress.update()

    def parsing_by_groups(self, widgets):
        pk = widgets['entry_pk'].get().strip()
        if bool(pk) is False:
            showwarning(
                'Не выбрана запись',
                'Для парсинга надо выбрать запись, по которой будет он '
                'произведён\n\nЗапись можно выбрать, нажав на кнопку '
                '"Выбрать"\n\nЕсли там нет записей, то выполните париснг по '
                'группам в первой подвкалдке вкладки "Парсинг", не ставя '
                'галочку у поля с отменой сбора дополнительных параметров. '
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

        followers_from = 0
        followers_to = 0
        data_from = 0
        data_to = 0
        relationship = 0
        last_seen_from = 0
        last_seen_to = 0
        political = 0
        people_main = 0
        life_main = 0
        smoking = 0
        alcohol = 0
        entry_status = ''
        entry_about = ''
        country = 0
        city = 0
        cities = []

        if (need_country == 0) and (need_city_region == 1):
            need = askyesno(
                'Не включена настройка',
                'Для парсинга по региону/городу необзодимо включить парсинг '
                'по стране '
                'и выбрать её\nПродолжить? (не будет учтён город/регион)'
            )
            if need is False:
                return

            need_city_region = 0

        if (need_city_region == 1) and (
                cmb_city_region == 'Нажмите "Настройка"'):
            need = askyesno(
                'Не сделана настройка',
                'Для парсинга по рeгиону/городу нужно выполнить настройку, '
                'нажав на соотвутствущую кнопку.\n\nПродолжить? (не будет '
                'учтён город/регион) '
            )
            if need is False:
                return

            need_city_region = 0

        if need_followers == 1:
            try:
                followers_from = widgets['var_followers_from'].get()
                followers_to = widgets['var_followers_to'].get()
            except TclError:
                showwarning(
                    'Неверное значение',
                    'Значения полей "Подписчиков" могут содержать только числа'
                )
                return
            if followers_from > followers_to:
                showwarning(
                    'Неверное значение',
                    'Значение поля "Подписчиков" "От" не может быть больше '
                    '"До" '
                )
                return
            if (followers_from > FOLLOWERS_MAX) or (
                    followers_to > FOLLOWERS_MAX):
                showwarning(
                    'Неверное значение',
                    'Значения полей "Друзей" не может быть больше '
                    f'{FOLLOWERS_MAX}'
                )
                return
        if need_data == 1:
            data_from = int(widgets['var_old_from'].get())
            data_to = int(widgets['var_old_to'].get())

            if data_from > data_to:
                showwarning(
                    'Неверное значение',
                    'Значение поля "Возраст" "От" не может быть больше "До"'
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
                showwarning(
                    'Неверное значение',
                    'Значения полей "Последний раз в сети" могут содержать '
                    'только числа '
                )
                return
            if last_seen_from > last_seen_to:
                showwarning(
                    'Неверное значение',
                    'Значение поля "Последний раз в сети" "От" не может быть '
                    'больше "До" '
                )
                return
            if (last_seen_from > LAST_SEEN_MAX) or (
                    last_seen_to > LAST_SEEN_MAX):
                showwarning(
                    'Неверное значение',
                    'Значения полей "Друзей" не может быть '
                    f'больше {FOLLOWERS_MAX}'
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
                showwarning(
                    'Неверное значение',
                    'Вы выбрали возможность парсинга по ключевому значению '
                    'статуса, '
                    'но оставили это поле пустым! '
                )
                return

        if need_entry_about == 1:
            entry_about = widgets['var_entry_about'].get().strip()

            if entry_about == '':
                showwarning(
                    'Неверное значение',
                    'Вы выбрали возможность парсинга по ключевому значению '
                    'Обо мне, '
                    'но оставили это поле пустым! '
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
        record = GetRequestsToDB().get_one_get_requests_table(
            pk=pk, columns='response'
        )

        record = json.loads(record[0])
        iteration = 0
        length = len(record)
        step = PROGRESSBAR_MAX // length
        progressbar['value'] = 0
        lbl_progress.configure(
            text=f'Прогресс {iteration}/{length}. Подождите, это может '
                 'занять несколько минут... '
        )
        progressbar.update()
        lbl_progress.update()

        result = []

        for item in record:
            iteration += 1
            lbl_progress.configure(
                text=f'Прогресс {iteration}/{length}. Подождите, это может '
                'занять несколько минут... '
            )
            progressbar['value'] += step
            progressbar.update()
            lbl_progress.update()

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
                    bdate = item['bdate']
                    if len(bdate.split('.')) != 3:
                        continue

                    format_bdate = '%d.%m.%Y'
                    now = time_now()
                    date_from = data_from
                    date_from = now - (int(date_from)*24*60*60)
                    date_to = data_to
                    date_to = now - (int(date_to)*24*60*60)

                    bdate = strptime(bdate, format_bdate)
                    bdate = mktime(bdate)

                    if date_from >= bdate >= date_to:
                        continue

                else:
                    continue

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

        count = len(result)
        time_parse = time_now()

        if count == 0:
            showinfo(
                'Не найдено пользователей',
                'Пользователи не найдены!\n\nВозможно, что лимит запросов '
                'на сегодня исчерпан!'
            )
            return

        peoples = json.dumps(result)
        UpdateRequestsToDB().update_get_people_bd(
            type_request=NAME_PARSING['by_criteria'], count_people=count,
            time=time_parse, response=peoples, last_parse=0
        )
