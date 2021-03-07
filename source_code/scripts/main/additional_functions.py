from scripts.connection.requests_to_api import RequestsAPI
from settings.settings import SettingsFunction, get_logger
from scripts.main.windows.dialog import RequestTreeView
from _tkinter import TclError
from settings import value_constraints
from settings.dicts import additional_dicts
from scripts.main.windows.dialog import DialogWindows
from tkinter import ttk
from pprint import pprint

logger = get_logger('additional_functions_master')


class AdditionalFunctions:
    @staticmethod
    def set_label_and_var_city_or_region(widgets):
        var = widgets['var_city_or_region']
        cmb = widgets['cmb_city_or_region']
        btn_parse = widgets['btn_parse']
        btn_settings = widgets['btn_set_setting']
        if var.get() == 'city':
            var.set('region')
            btn_parse.grid_remove()
            cmb['values'] = []
            cmb.set('Нажмите "Настроить"')
            btn_settings.configure(text='Настроить')

        elif var.get() == 'region':
            var.set('city')
            btn_parse.grid_remove()
            cmb['values'] = []
            cmb.set('Нажмите "Настроить"')
            btn_settings.configure(text='Настроить')

    @staticmethod
    def set_widget_old_only(widgets):
        var = widgets['var_only']
        label_old_only = widgets['label_old_only']
        spin_old_only = widgets['spin_old_only']
        label_old_only_day = widgets['label_old_only_day']

        if var.get() == 1:
            var.set(0)
            label_old_only.grid(row=8, column=3, sticky='SE')
            spin_old_only.grid(row=8, column=4, sticky='SW', padx=15)
            label_old_only_day.grid(row=8, column=5, sticky='SW')
        elif var.get() == 0:
            var.set(1)
            label_old_only.grid_remove()
            spin_old_only.grid_remove()
            label_old_only_day.grid_remove()

    @staticmethod
    def set_entry_for_group_search(widgets):
        var = widgets['var_group_search']
        entry = widgets['entry_group_id']

        if var.get() == 0:
            var.set(1)
            entry.grid(
                row=11, column=3, sticky='SWE', columnspan=4, pady=15, padx=10
            )
        elif var.get() == 1:
            var.set(0)
            entry.grid_remove()

    @staticmethod
    def open_request_tree_view():
        tree_view = RequestTreeView()

        tree_view.window.wait_window()

    @staticmethod
    def sort_group_id(ids):
        if ids[:15] == 'https://vk.com/':
            group_id = ids[15:]

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

        if ids is not None:
            group_id = ids

            return group_id

        return None


class AdditionalFunctionsForAPI(RequestsAPI):
    def __init__(self):
        super().__init__()
        self.settings_app = SettingsFunction()
        self.additional_functions = AdditionalFunctions()
        self.list_city = None
        self.list_region = None

    def settings_before_parsing(self, widgets):
        variable = widgets['var_city_or_region']
        cmb_country = widgets['cmb_country']
        combobox = widgets['cmb_city_or_region']
        progressbar = widgets['progressbar']
        btn_parse = widgets['btn_parse']
        var = variable.get()

        country_name: str = cmb_country.get()
        country_id: int = additional_dicts.LIST_COUNTRIES[country_name]

        if var == 'city':
            if self.list_city is None:
                objects_cities_or_regions = self.get_cities(
                    country_id=country_id,
                    progressbar=progressbar
                )
                if objects_cities_or_regions is None:
                    return None

                self.list_city = objects_cities_or_regions
            else:
                objects_cities_or_regions = self.list_city

        else:
            if self.list_region is None:
                objects_cities_or_regions = self.get_regions(
                    country_id=country_id,
                    progressbar=progressbar
                )
                if objects_cities_or_regions is None:
                    return None

                self.list_region = objects_cities_or_regions
            else:
                objects_cities_or_regions = self.list_region

        values = list(objects_cities_or_regions.keys())
        combobox['values'] = values
        combobox.set(values[0])
        btn_parse.grid(row=0, column=0)

    def main_parsing(self, widgets):
        var = widgets['var_city_or_region']

        if var == 'city':
            self.main_parsing_city(widgets=widgets)
        else:
            self.main_parsing_region(widgets=widgets)

    def main_parsing_city(self, widgets):
        pass

    def main_parsing_region(self, widgets):
        country = widgets['cmb_country'].get()
        country = additional_dicts.LIST_COUNTRIES[country]

        region = widgets['cmb_city_or_region'].get()
        region = self.list_region[region]
        cities = self.cities_on_region(country_id=country, region_id=region)
        if cities is None:
            return None

        status = widgets['cmb_status'].get()
        status = additional_dicts.STATUS_VK_PERSON[status]

        old_from = int(widgets['var_old_from'].get())
        old_to = int(widgets['var_old_to'].get())

        try:
            friend_from = widgets['var_friends_from'].get()
            friend_to = widgets['var_friends_to'].get()

            if (friend_to > value_constraints.FRIENDS_MAX) or \
                    (friend_from > value_constraints.FRIENDS_MAX) or \
                    (friend_from > friend_to):

                raise TclError('Неверное значение')

        except TclError:
            error = additional_dicts.ERROR_MSG['Preparation_of_data']
            error = error['invalid_friends_value']
            DialogWindows.error_window(
                title='Неверное значение',
                error_txt=error.format(value_constraints.FRIENDS_MAX)
            )

        try:
            follower_from = widgets['var_follower_from'].get()
            follower_to = widgets['var_follower_to'].get()

            if (follower_to > value_constraints.FOLLOWERS_MAX) or \
                    (follower_from > value_constraints.FOLLOWERS_MAX) or \
                    (follower_from > follower_to):
                raise TclError('Неверное значение')

        except TclError:
            error = additional_dicts.ERROR_MSG['Preparation_of_data']
            error = error['invalid_followers_value']
            DialogWindows.error_window(
                title='Неверное значение',
                error_txt=error.format(value_constraints.FOLLOWERS_MAX)
            )

        sex = widgets['var_sex'].get()

        only = widgets['var_only'].get()
        if only == 0:
            last_only = widgets['spin_old_only'].get()

        has_photo = widgets['var_photo'].get()

        can_send_message = widgets['var_send_message'].get()

        search_only_group = widgets['var_group_search'].get()
        if search_only_group == 1:
            group_ids = widgets['entry_group_id'].get()

            group_id = self.additional_functions.sort_group_id(group_ids)

            if group_id is None:
                warning = additional_dicts.ERROR_MSG['Preparation_of_data']
                warning = warning['invalid_group_id_value']
                DialogWindows.warning_window(
                    title='Неверное значение',
                    warning_txt=warning.format(group_ids)
                )
            if type(group_id) != int:
                group_id = self.get_id_group(group_id)
                if group_id is None:
                    warning = additional_dicts.ERROR_MSG['Preparation_of_data']
                    warning = warning['invalid_group_id_value']
                    DialogWindows.warning_window(
                        title='Неверное значение',
                        warning_txt=warning.format(group_ids)
                    )
