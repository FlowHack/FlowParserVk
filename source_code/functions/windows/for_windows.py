import json
from time import time as time_now
from tkinter.messagebox import showinfo, showwarning

from base_data import UpdateRequestsToDB
from settings import LIST_COUNTRIES, LOGGER, NAME_PARSING

from ..vk_api import ParsingVk
from .additional import AdditionalFunctionsForWindows


class FunctionsForWindows:
    @staticmethod
    def update_label_count_group(widgets):
        text, lbl = widgets['txt_groups'], widgets['lbl_count']
        text = text.get('1.0', 'end')

        try:
            count = AdditionalFunctionsForWindows.get_groups_from_text(text)['count']
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
        method = NAME_PARSING['by_groups']
        time = time_now()

        try:
            ids = AdditionalFunctionsForWindows.get_groups_from_text(text)['ids']
        except ValueError as error:
            if str(error) == 'неверный id':
                showwarning(
                    'Неверный id',
                    'Проверьте ваши id, среди них есть неверный!'
                )
                return

        values = ParsingVk.parse_by_groups(progressbar, lbl_progress, ids, last_parse)

        count, peoples = values['count'], values['result']

        if count == 0:
            showinfo(
                'Не найдено пользователей',
                'Пользователи не найдены!\n\nВозможно, что лимит запросов на сегодня '
                'исчерпан!'
            )
            return

        peoples = json.dumps(peoples, ensure_ascii=False)

        UpdateRequestsToDB().update_get_people_bd(
            type_request=method, count_people=count, time=time, response=peoples,
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
        spn_from, spn_to = widgets['spn_last_seen_from'], widgets['spn_last_seen_to']
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

    @staticmethod
    def setting_photo(widgets):
        var, chk = widgets['var_has_photo'], widgets['chk_need_mach_photo']
        lbl, lbl_to = widgets['lbl_how_mach_photo'], widgets['lbl_photo_to']
        spn_from, spn_to = widgets['spn_photo_from'], widgets['spn_photo_to']

        if var.get() == 1:
            var.set(0)
            chk.grid_remove()
            lbl.grid_remove()
            lbl_to.grid_remove()
            spn_from.grid_remove()
            spn_to.grid_remove()
        elif var.get() == 0:
            var.set(1)
            chk.grid()
            lbl.grid()
            lbl_to.grid()
            spn_from.grid()
            spn_to.grid()

    def parsing_by_groups(self, widgets):
        pass
