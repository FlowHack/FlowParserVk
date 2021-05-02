import json
import os
from time import gmtime, strftime
from tkinter import Toplevel, ttk
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import askyesno

from PIL import ImageTk

from base_data import DeleteRequestsToDB, GetRequestsToDB
from settings import (FORMAT_DATE, LOGGER, NAME_PARSING, path_to_dir_ico,
                      set_position_window_on_center, styles)

LOGGER = LOGGER('dialog', 'windows')


class TreeViewWindow:
    """
    Класс отвечающий за окно просмотра запросов
    """

    def __init__(self, method: str = 'view', completion_name: str = None,
                 entry_pk: object = None):
        """
        Запуск окна просмотра запросов
        :param method: метод просмотра (view-обычный просмотр всех запросов)
        :param completion_name: имя запроса default: None
        :param entry_pk: виджет Entry для записи выбранного pk default: None
        """
        self.method = method
        self.completion_name = completion_name
        self.entry_pk = entry_pk
        self.select = ['pk', 'type_request', 'count_people', 'time_request']
        self.get_requests_db = GetRequestsToDB()
        self.values = []

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
        self.tree_view.column('#2', minwidth=50, width=130, stretch=0,
                              anchor='center')
        self.tree_view.column('#3', minwidth=100, width=100, stretch=0,
                              anchor='center')

        self.tree_view.grid(row=0, column=0, columnspan=4, rowspan=3,
                            sticky='NSEW')

        if method == 'view':
            btn_clear = ttk.Button(right_frame, text='Очистить')
            btn_delete = ttk.Button(right_frame, text='Удалить')
            btn_download = ttk.Button(right_frame, text='Выгрузить txt')

            btn_clear.grid(row=0, column=0, sticky='WE')
            btn_delete.grid(row=1, column=0, pady=5, sticky='WE')
            btn_download.grid(row=2, column=0, sticky='WE')

            btn_clear.bind('<Button-1>', lambda event: self.clear_values())
            btn_delete.bind('<Button-1>', lambda event: self.delete_value())
            btn_download.bind('<Button-1>',
                              lambda event: self.download_on_txt())
        else:
            btn_choose = ttk.Button(right_frame, text='Выбрать')
            btn_cancel = ttk.Button(
                right_frame, text='Отмена',
                command=lambda: self.window.destroy()
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

        self.__get_records__()
        self.completion_tree_view()

    def initialize_ui(self):
        """
        Инициализация окна
        :return:
        """
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
        """
        Функция отвечающая за обработку двойного клика в случае выбора записи
        :return:
        """
        try:
            pk = self.get_choose_value()['pk']
        except IndexError:
            return

        self.entry_pk.delete(0, 'end')
        self.entry_pk.insert('end', str(pk))
        self.window.destroy()

    def cancel(self):
        """
        Кнопка отмены выбора pk
        :return:
        """
        self.entry_pk.delete(0, 'end')
        self.window.destroy()

    def get_choose_value(self):
        """
        Получить объект выбранной записи
        :return:
        """
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
        """
        Функция заполняет TreeView данным из BaseData
        :return:
        """
        if len(self.values) == 0:
            return
        if type(self.values) == dict:
            self.values = [self.values]

        index = 0
        for item in self.values:
            time = gmtime(int(item['time_request']))
            data = strftime(FORMAT_DATE, time)
            self.tree_view.insert(
                '', index=index, text=data,
                values=(item['type_request'], item['count_people'], item['pk'])
            )
            index += 1

    def clear_values(self):
        """
        Очищает все записи в BD
        :return:
        """
        ask = askyesno(
            'Очистка записей', 'Вы уверены, что хотите удалить все записи?'
        )
        if ask is True:
            LOGGER.warning('Запрос на удаление таблицы GetRequestsApi')
            delete_request_db = DeleteRequestsToDB()
            delete_request_db.delete_all_records(
                delete_request_db.get_requests
            )
            delete_request_db.delete_all_records(
                delete_request_db.additional_get_requests
            )

        self.window.destroy()

    def delete_value(self):
        """
        Удаляет выбранную запись
        :return:
        """
        try:
            values = self.get_choose_value()
            pk = values['pk']

            LOGGER.warning(
                'Запрос на удаление элемента в таблице GetRequestsApi'
            )
            delete_request_db = DeleteRequestsToDB()
            delete_request_db.delete_record_in_bd(
                tb_name=delete_request_db.get_requests,
                where=f'pk={pk}'
            )
            delete_request_db.delete_record_in_bd(
                tb_name=delete_request_db.additional_get_requests,
                where=f'pk_attachment={pk}'
            )
        except IndexError as error:
            if str(error) == 'не выбран элемент':
                return
        for row in self.tree_view.get_children():
            self.tree_view.delete(row)

        self.__get_records__()
        self.completion_tree_view()

    def download_on_txt(self):
        """
        Выгрузка ID в txt формате
        :return:
        """
        new_result = []
        try:
            values = self.get_choose_value()
        except IndexError:
            return

        pk = values['pk']
        values = self.get_requests_db.get_records_get_requests(
            pk=pk, method=True, last_parse=True
        )
        method = values['method']
        result = values['response']
        result = json.loads(result)

        if method == NAME_PARSING['by_groups']:
            last_parse = values['last_parse']
            if last_parse == 1:
                for item in result:
                    new_result.append(str(item['id']))
                result = new_result
            else:
                result = [str(item) for item in result]

        result = '\n'.join(result)
        directory = asksaveasfilename()
        if directory[-4:] != '.txt':
            directory += '.txt'

        with open(directory, 'w', encoding='utf-8') as file:
            file.write(result)

    def __get_records__(self):
        if self.method == 'view':
            values = self.get_requests_db.get_records(
                select=self.select, order='pk DESC', one_record=True,
                tb_name=self.get_requests_db.get_requests,
            )
            self.values = [] if len(values) == 0 else [values]

            values = self.get_requests_db.get_records(
                select=self.select, order='pk DESC',
                tb_name=self.get_requests_db.get_requests,
            )
            self.values += values if type(values) == list else [values]
        else:
            self.entry_pk = self.entry_pk
            values = self.get_requests_db.get_records(
                select=self.select, order='pk DESC', one_record=True,
                tb_name=self.get_requests_db.get_requests,
                where=f' (type_request = "{self.completion_name}") '
                      'and (last_parse = 1)'
            )
            self.values = [] if len(values) == 0 else [values]

            values = self.get_requests_db.get_records(
                select=self.select,
                tb_name=self.get_requests_db.get_requests,
                order=' pk DESC',
                where=f' (type_request = "{self.completion_name}") '
                      'and (last_parse = 1)'
            )
            self.values += values if type(values) == list else [values]
