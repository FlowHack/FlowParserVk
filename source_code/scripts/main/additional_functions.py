from scripts.connection.requests_to_api import RequestsAPI
from settings.settings import SettingsFunction, get_logger
from scripts.main.windows.dialog import RequestTreeView
from tkinter import ttk
from pprint import pprint

logger = get_logger('additional_functions_master')


class AdditionalFunctionsForAPI(RequestsAPI):
    def __init__(self):
        super().__init__()
        self.settings_app = SettingsFunction()
        self.list_city = None
        self.list_region = None

    def get_cities_or_regions_combobox(self, widgets):
        variable = widgets['var_city_or_region']
        cmb_country = widgets['cmb_country']
        combobox = widgets['cmb_city_or_region']
        progressbar = widgets['progressbar']
        btn_parse = widgets['btn_parse']
        var = variable.get()

        country_name: str = cmb_country.get()
        country_id: int = self.settings_app.LIST_COUNTRIES[country_name]

        if var == 'city':
            if self.list_city is None:
                objects_cities_or_regions = self.get_cities(
                    country_id=country_id,
                    progressbar=progressbar
                )

                self.list_city = objects_cities_or_regions
            else:
                objects_cities_or_regions = self.list_city

        else:
            if self.list_region is None:
                objects_cities_or_regions = self.get_regions(
                    country_id=country_id,
                    progressbar=progressbar
                )
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
        country = widgets['cmb_country'].get()
        country = SettingsFunction.LIST_COUNTRIES[country]
        city = widgets['cmb_city_or_region'].get()
        city = self.list_city[city]
        sex = widgets['var_sex'].get()
        has_photo = widgets['var_photo'].get()
        status = widgets['cmb_status'].get()
        status = SettingsFunction.STATUS_VK_PERSON[status]
        online = widgets['var_only'].get()
        age_from = widgets['var_old_from'].get()
        age_to = widgets['var_old_to'].get()
        progressbar = widgets['progressbar']
        arguments = {
            'country': country,
            'city': city,
            'sex': sex,
            'online': online,
            'has_photo': has_photo,
            'age_from': age_from,
            'age_to': age_to,
            'status': status
        }
        result = RequestsAPI().get_response(
            api_method='users.search', progressbar=progressbar, **arguments
        )
        pprint(result)

    def main_parsing_region(self, widgets):
        pass


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
    def open_request_tree_view():
        tree_view = RequestTreeView()

        tree_view.window.wait_window()

    def parse_for_main_book(
            self, country,
    ):
        pass
