from scripts.connection.requests_to_api import RequestsAPI
from settings.settings import SettingsFunction, get_logger
from scripts.main.windows.dialog import RequestTreeView
from tkinter import ttk

logger = get_logger('additional_functions_master')


class AdditionalFunctionsForAPI(RequestsAPI):
    def __init__(self):
        super().__init__()
        self.settings_app = SettingsFunction()
        self.list_city = None
        self.list_region = None

    def get_cities_or_regions_combobox(self, widgets):
        right_frame = widgets['right_frame']
        variable = widgets['var_city_or_region']
        cmb_country = widgets['cmb_country']
        combobox = widgets['cmb_city_or_region']
        progressbar = widgets['progressbar']
        var = variable.get()
        country_name: str = cmb_country.get()
        country_id: int = self.settings_app.LIST_COUNTRIES[country_name]
        if var == 'city':
            if self.list_city is None:
                objects_cities_or_regions = self.get_response(
                    api_method='database.getCities',
                    progressbar=progressbar,
                    country_id=country_id
                )
                self.list_city = objects_cities_or_regions
            else:
                objects_cities_or_regions = self.list_city

            action = self.main_parsing_city
        else:
            if self.list_region is None:
                objects_cities_or_regions = self.get_response(
                    api_method='database.getRegions',
                    progressbar=progressbar,
                    country_id=country_id
                )
                self.list_region = objects_cities_or_regions
            else:
                objects_cities_or_regions = self.list_region

            action = self.main_parsing_region

        values = list(objects_cities_or_regions.keys())
        combobox['values'] = values
        combobox.set(values[0])
        btn_parse = ttk.Button(
            right_frame, text='Парсить', command=lambda: action(widgets)
        )
        btn_parse.grid(row=1, column=0)

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
        print(result)

    def main_parsing_region(self, widgets):
        pass


class AdditionalFunctions:
    @staticmethod
    def set_label_and_var_city_or_region(widgets):
        var = widgets['var_city_or_region']
        label = widgets['label_var_city_or_country']
        cmb = widgets['cmb_city_or_region']
        btn_settings = widgets['btn_set_setting']
        if var.get() == 'city':
            var.set('region')
            label.configure(text='Регион')
            cmb['values'] = []
            cmb.set('Нажмите "Настроить"')
            btn_settings.configure(text='Настроить')

        elif var.get() == 'region':
            var.set('city')
            label.configure(text='Город')
            cmb['values'] = []
            cmb.set('Нажмите "Настроить"')
            btn_settings.configure(text='Настроить')

    @staticmethod
    def open_request_tree_view():
        tree_view = RequestTreeView()

        tree_view.window.wait_window()

    def parse_for_main_book(
            self, country,
    ):
        pass
