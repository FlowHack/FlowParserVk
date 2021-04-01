from time import time as time_now
from tkinter.messagebox import showwarning
from math import ceil

from _tkinter import TclError

from settings import (ERROR_MSG, FOLLOWERS_MAX, FRIENDS_MAX, LIST_COUNTRIES,
                      STATUS_VK_PERSON)

from ..vk_api import FunctionsForMainParsing, MainFunctionsForParsing


class AdditionalFunctionsForWindows:
    @staticmethod
    def sort_group_ids(ids):
        if ids[:15] == 'https://vk.com/':
            group_id = ids[15:]

            return group_id

        if ids[:17] == 'https://vk.com/id':
            group_id = ids[17:]

            return group_id

        if ids[:2] == 'id':
            group_id = ids[2:]

            return group_id

        if ids[:3] == '@id':
            group_id = ids[3:]

            return group_id

        try:
            group_id = int(ids)

            return group_id
        except ValueError:
            pass

        return ids

    def data_preparation_for_main_parsing(self, widgets, city_or_region, cities=None,
                                          regions=None):
        main_values_for_parsing = {'fields': 'followers_count'}
        additional_values = {}

        country = widgets['cmb_country'].get()
        country = LIST_COUNTRIES[country]
        main_values_for_parsing['country'] = country

        city_region = widgets['cmb_city_or_region'].get()
        if city_or_region == 'city':
            city_region = cities[city_region]
            main_values_for_parsing['city'] = city_region
        else:
            cities = []

            city_region = regions[city_region]
            city_region = MainFunctionsForParsing.get_objects(
                country_id=country, region_id=city_region,
                do=3
            )
            for item in city_region:
                cities.append(item['id'])

            additional_values['cities'] = cities

        try:
            follower_from = int(widgets['var_follower_from'].get())
            follower_to = int(widgets['var_follower_to'].get())

            if (follower_to > FOLLOWERS_MAX) or \
                    (follower_from > FOLLOWERS_MAX) or \
                    (follower_from > follower_to):
                raise TclError('Неверное значение в поле "Подписчики"')

            additional_values['followers_from'] = follower_from
            additional_values['followers_to'] = follower_to

        except TclError as error:
            from windows import DialogWindows
            if str(error) == 'Неверное значение в поле "Друзья"':
                error = ERROR_MSG['Preparation_of_data']
                error = error['invalid_friends_value']
                showwarning('Неверное значение', error.format(FRIENDS_MAX))
            if str(error) == 'Неверное значение в поле "Подписчики"':
                error = ERROR_MSG['Preparation_of_data']
                error = error['invalid_followers_value']
                showwarning('Неверное значение', error.format(FOLLOWERS_MAX))
            error = ERROR_MSG['Preparation_of_data']
            error = error['invalid_value_friends_or_followers']
            showwarning('Неверное значение', error)

        status = widgets['cmb_status'].get()
        status = STATUS_VK_PERSON[status]
        if status != 0:
            main_values_for_parsing['status'] = status

        old_from = int(widgets['var_old_from'].get())
        old_to = int(widgets['var_old_to'].get())
        main_values_for_parsing['age_from'] = old_from
        main_values_for_parsing['age_to'] = old_to

        sex = widgets['var_sex'].get()
        main_values_for_parsing['sex'] = sex

        only = widgets['var_only'].get()
        if only == 0:
            last_only = widgets['spin_old_only'].get()
            if last_only == '':
                last_only = 0
            else:
                last_only = ceil(time_now() - (int(last_only) * 24 * 60 * 60))

            main_values_for_parsing['online'] = only
            main_values_for_parsing['fields'] += ', last_seen'
            additional_values['last_seen'] = last_only
        else:
            main_values_for_parsing['online'] = only

        has_photo = widgets['var_photo'].get()
        main_values_for_parsing['has_photo'] = has_photo

        can_send_message = widgets['var_send_message'].get()
        if can_send_message == 0:
            pass
        else:
            main_values_for_parsing['fields'] += ', can_write_private_message'
            additional_values['can_send_message'] = True

        search_only_group = widgets['var_group_search'].get()
        if search_only_group == 1:
            group_ids = widgets['entry_group_id'].get()

            ids = self.sort_group_ids(group_ids)
            group_id = MainFunctionsForParsing.sort_group_id(ids)

            main_values_for_parsing['group_id'] = group_id

        return main_values_for_parsing, additional_values
