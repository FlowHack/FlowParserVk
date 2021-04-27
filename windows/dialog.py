import json
from time import gmtime, strftime
from tkinter import Toplevel, ttk
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import askyesno

from base_data import DeleteRequestsToDB, GetRequestsToDB
from settings import (FORMAT_DATE, LOGGER, NAME_PARSING, fonts,
                      set_position_window_on_center, styles, path_to_dir_ico)
import os
from PIL import ImageTk


class TreeViewWindow:
    def __init__(self, method='view', completion_name=None, entry_pk=None):
        if method == 'view':
            self.values = \
                GetRequestsToDB().get_get_requests_people_table_value()
        else:
            self.entry_pk = entry_pk
            self.values = GetRequestsToDB().get_get_requests_people_for_parse(
                completion_name
            )

        self.window = Toplevel()
        self.initialize_ui()

        left_frame = ttk.Frame(self.window)
        left_frame.grid(row=0, column=0, sticky='NSWE')

        right_frame = ttk.Frame(self.window, padding=5)
        right_frame.grid(row=0, column=1, sticky='NSWE')

        self.tree_view = ttk.Treeview(
            left_frame, columns=('Тип', 'Количество id', 'Дата')
        )

        self.tree_view.heading('#0', text='Дата')
        self.tree_view.heading('#1', text='Тип')
        self.tree_view.heading('#2', text='Количество id')
        self.tree_view.heading('#3', text='ID')

        self.tree_view.column('#0', minwidth=200, width=200, stretch=0)
        self.tree_view.column('#1', minwidth=200, width=220, stretch=0)
        self.tree_view.column('#2', minwidth=50, width=130, stretch=0, anchor='center')
        self.tree_view.column('#3', minwidth=100, width=100, stretch=0, anchor='center')

        self.tree_view.grid(row=0, column=0, columnspan=4, rowspan=3, sticky='NSEW')

        if method == 'view':
            btn_clear = ttk.Button(right_frame, text='Очистить')
            btn_delete = ttk.Button(right_frame, text='Удалить')
            btn_download = ttk.Button(right_frame, text='Выгрузить txt')

            btn_clear.grid(row=0, column=0, sticky='WE')
            btn_delete.grid(row=1, column=0, pady=5, sticky='WE')
            btn_download.grid(row=2, column=0, sticky='WE')

            btn_clear.bind('<Button-1>', lambda event: self.clear_values())
            btn_delete.bind('<Button-1>', lambda event: self.delete_value())
            btn_download.bind('<Button-1>', lambda event: self.download_on_txt())
        else:
            btn_choose = ttk.Button(right_frame, text='Выбрать')
            btn_cancel = ttk.Button(
                right_frame, text='Отмена', command=lambda: self.window.destroy()
            )

            btn_choose.grid(row=0, column=0, sticky='SWE')
            btn_cancel.grid(row=1, column=0, sticky='SWE', pady=5)

            btn_cancel.bind('<Button-1>', lambda event: self.cancel())
            btn_choose.bind(
                '<Button-1>',
                lambda event: self.choose_value_for_parsing()
            )
            self.tree_view.bind(
                '<Double-Button-1>',
                lambda event: self.choose_value_for_parsing()
            )

        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=9)
        self.window.columnconfigure(1, weight=1)

        left_frame.rowconfigure(0, weight=1)
        left_frame.columnconfigure(0, weight=1)

        self.completion_tree_view()

    def initialize_ui(self):
        FPVK = ImageTk.PhotoImage(
            file=os.path.join(path_to_dir_ico, 'FPVK.ico')
        )
        styles.set_global_style(self.window)

        w = 800
        h = 600
        self.window.title('Основные запросы')
        set_position_window_on_center(self.window, width=w, height=h)
        self.window.tk.call('wm', 'iconphoto', self.window._w, FPVK)

    def choose_value_for_parsing(self):
        try:
            pk = self.get_choose_value()['pk']
        except IndexError:
            return

        self.entry_pk.delete(0, 'end')
        self.entry_pk.insert('end', str(pk))
        self.window.destroy()

    def cancel(self):
        self.entry_pk.delete(0, 'end')
        self.window.destroy()

    def get_choose_value(self):
        if not self.tree_view.selection():
            raise IndexError('не выбран элемент')

        item = self.tree_view.selection()[0]
        values = self.tree_view.item(item, option="values")
        result = {
            'pk': values[2],
            'method': values[0],
            'count': values[1]
        }

        return result

    def completion_tree_view(self):
        if self.values is None:
            return

        index = 0
        for item in self.values:
            time = gmtime(int(item[4]))
            data = strftime(FORMAT_DATE, time)
            self.tree_view.insert(
                '', index=index, text=data,
                values=(item[1], item[2], item[0])
            )
            index += 1

    def clear_values(self):
        ask = askyesno('Очистка записей', 'Вы уверены, что хотите удалить все записи?')
        if ask is True:
            LOGGER.warning('Запрос на удаление таблицы GetRequestsApi')
            DeleteRequestsToDB().delete_all_records('GetRequestsApi')

        for row in self.tree_view.get_children():
            self.tree_view.delete(row)

        self.values = GetRequestsToDB().get_get_requests_people_table_value()
        self.completion_tree_view()

    def delete_value(self):
        try:
            values = self.get_choose_value()
            pk = values['pk']

            LOGGER.warning('Запрос на удаление элемента в таблице GetRequestsApi')
            DeleteRequestsToDB().delete_record_in_people_request_bd(pk)
        except IndexError as error:
            if str(error) == 'не выбран элемент':
                return
        for row in self.tree_view.get_children():
            self.tree_view.delete(row)

        self.values = GetRequestsToDB().get_get_requests_people_table_value()
        self.completion_tree_view()

    def download_on_txt(self):
        new_result = []
        try:
            values = self.get_choose_value()
        except IndexError:
            return

        pk = values['pk']
        values = GetRequestsToDB().get_one_get_requests_table(pk)
        method = values['method']
        result = values['result']
        result = json.loads(result)

        if method == NAME_PARSING['by_groups']:
            last_parse = values['last_parse']
            if last_parse == 1:
                for item in result:
                    new_result.append(str(item['id']))

                result = new_result

        result = '\n'.join(list(map(str, result)))
        directory = asksaveasfilename()
        if directory[-4:] != '.txt':
            directory += '.txt'

        with open(directory, 'w') as file:
            file.write(result)