from _tkinter import TclError
from settings import (ERROR_MSG, LIST_COUNTRIES, STATUS_VK_PERSON,
                      value_constraints)


class AdditionalFunctionsVkApi:
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

    def get_values_for_main_parsing(
            self, widgets, city_or_region, cities=None, regions=None):
        main_values_for_parsing = {'fields': 'counters'}
        additional_values = {}

        country = widgets['cmb_country'].get()
        country = LIST_COUNTRIES[country]
        main_values_for_parsing['country'] = country

        city_region = widgets['cmb_city_or_region'].get()
        if city_or_region == 'city':
            city_region = cities[city_region]
            main_values_for_parsing['city'] = city_region
        else:
            from functions import FunctionsForAPI
            city_region = regions[city_region]
            city_region = FunctionsForAPI().get_all_cities_in_region(
                country_id=country, region_id=city_region
            )
            if city_region is None:
                return None
            additional_values['cities'] = city_region

        try:
            friend_from = int(widgets['var_friends_from'].get())
            friend_to = int(widgets['var_friends_to'].get())

            follower_from = int(widgets['var_follower_from'].get())
            follower_to = int(widgets['var_follower_to'].get())

            if (friend_to > value_constraints.FRIENDS_MAX) or \
                    (friend_from > value_constraints.FRIENDS_MAX) or \
                    (friend_from > friend_to):
                raise TclError('Неверное значение в поле "Друзья"')

            if (follower_to > value_constraints.FOLLOWERS_MAX) or \
                    (follower_from > value_constraints.FOLLOWERS_MAX) or \
                    (follower_from > follower_to):
                raise TclError('Неверное значение в поле "Подписчики"')

            main_values_for_parsing['friends_from'] = friend_from
            main_values_for_parsing['friends_to'] = friend_to

            main_values_for_parsing['followers_from'] = follower_from
            main_values_for_parsing['followers_to'] = follower_to

        except TclError as error:
            from windows import DialogWindows
            if str(error) == 'Неверное значение в поле "Друзья"':
                error = ERROR_MSG['Preparation_of_data']
                error = error['invalid_friends_value']
                DialogWindows.error_window(
                    title='Неверное значение',
                    error_txt=error.format(value_constraints.FRIENDS_MAX)
                )
            if str(error) == 'Неверное значение в поле "Подписчики"':
                error = ERROR_MSG['Preparation_of_data']
                error = error['invalid_followers_value']
                DialogWindows.error_window(
                    title='Неверное значение',
                    error_txt=error.format(value_constraints.FOLLOWERS_MAX)
                )
            error = ERROR_MSG['Preparation_of_data']
            error = error['invalid_value_friends_or_followers']
            DialogWindows.error_window(
                title='Неверное значение',
                error_txt=error
            )

        status = widgets['cmb_status'].get()
        status = STATUS_VK_PERSON[status]
        if status is not False:
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

            main_values_for_parsing['online'] = only
            main_values_for_parsing['fields'] += ', last_seen'
            additional_values['last_only'] = last_only
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

            group_id = self.sort_group_id(group_ids)

            main_values_for_parsing['group_id'] = group_id

        return main_values_for_parsing, additional_values
