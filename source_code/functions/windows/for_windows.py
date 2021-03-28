from settings import LIST_COUNTRIES, get_logger
from windows.dialog import RequestTreeView

from ..vk_api import FunctionsForRequestToAPI
from .additional import AdditionalFunctionsForWindows
from time import time as  time_now

logger = get_logger('additional_functions_for_windows')


class FunctionsForWindows(AdditionalFunctionsForWindows):
    def __init__(self):
        super().__init__()
        self.functions_for_api = FunctionsForRequestToAPI
        self.cities = None
        self.regions = None

    def settings_before_parsing(self, widgets):
        variable = widgets['var_city_or_region']
        cmb_country = widgets['cmb_country']
        combobox = widgets['cmb_city_or_region']
        progressbar = widgets['progressbar']
        btn_parse = widgets['btn_parse']
        var = variable.get()

        country_name: str = cmb_country.get()
        country_id: int = LIST_COUNTRIES[country_name]

        if var == 'city':
            if self.cities is None:
                objects_cities_or_regions = \
                    self.functions_for_api().get_all_cities(
                        country_id=country_id,
                        progressbar=progressbar
                    )
                if objects_cities_or_regions is None:
                    return None

                self.cities = objects_cities_or_regions
            else:
                objects_cities_or_regions = self.cities
        else:
            if self.regions is None:
                objects_cities_or_regions = \
                    self.functions_for_api().get_all_regions(
                        country_id=country_id,
                        progressbar=progressbar
                    )
                if objects_cities_or_regions is None:
                    return None

                self.regions = objects_cities_or_regions
            else:
                objects_cities_or_regions = self.regions

        values = list(objects_cities_or_regions.keys())
        combobox['values'] = values
        combobox.set(values[0])
        btn_parse.grid(row=0, column=0)

    def main_parsing(self, widgets):
        var = widgets['var_city_or_region']
        progressbar = widgets['progressbar']

        if var == 'city':
            main_values, additional_values = self.data_preparation_for_main_parsing(
                widgets=widgets,
                city_or_region='city',
                regions=self.cities
            )

            self.functions_for_api().main_parsing_city(
                main_values=main_values,
                additional_values=additional_values
            )
        else:
            main_values, additional_values = self.data_preparation_for_main_parsing(
                widgets=widgets,
                city_or_region='region',
                regions=self.regions
            )
            if 'last_only' in additional_values.keys():
                last_only = additional_values['last_only']
                last_only = time_now() - (int(last_only) * 24 * 60 * 60)
                additional_values['last_only'] = last_only

            self.functions_for_api().main_parsing_region(
                main_values=main_values,
                additional_values=additional_values,
                progressbar=progressbar
            )

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
