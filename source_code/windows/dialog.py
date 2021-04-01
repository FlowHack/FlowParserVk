from tkinter import YES, Toplevel, ttk, VERTICAL, E

from settings import LOGGER, fonts, set_position_window_on_center, styles
from base_data import UpdateRequestsToDB, GetRequestsToDB
from time import strftime, gmtime

one_value = None
two_value = None


class GetWindow:
    def __init__(self, title, text_field_one, text_field_two=None,
                 header='Заполните!', count_field=1):
        def press_ok_btn(parent, one_entry, two_entry=None):
            """
            Обработка нажатия на кнопку ok
            :param parent: объект инпут окна
            :param one_entry: объект первого инпута
            :param two_entry: объект второго инпута
            :return: данные из полей
            """
            empty = False

            value_one = one_entry.get()
            if value_one == '':
                one_entry.configure(
                    style='Warning.TEntry', foreground='black'
                )
                empty = True

            if count_field == 2:
                value_two = two_entry.get()

                if value_two == '':
                    two_entry.configure(
                        style='Warning.TEntry', foreground='black'
                    )
                    empty = True
            else:
                value_two = None

            if empty is True:
                parent.update()
            else:
                self.one_value = value_one
                self.two_value = value_two
                parent.destroy()

        def press_close_btn(parent):
            """
            Обработка события нажатия на кнопку отмены ввода данных
            :param parent: объект инпут окна
            :return: ничего
            """
            parent.destroy()

        self.one_value = None
        self.two_value = None

        self.get_window = Toplevel()
        self.get_window.resizable(0, 0)
        styles.set_global_style(self.get_window)
        styles.style_for_ok_and_close_btn()
        styles.style_for_warning_entry()
        self.get_window.title(title)
        w = 450
        h = (125, 150)[count_field == 2]
        set_position_window_on_center(self.get_window, width=w, height=h)

        top_frame = ttk.Frame(
            self.get_window, padding=5, borderwidth=2, relief='groove'
        )
        top_frame.pack(side='top', fill='x')
        ttk.Label(
            top_frame,
            text=header,
            justify='center',
            font=fonts.H6_FONT
        ).pack(side='top')

        bottom_frame = ttk.Frame(self.get_window, padding=10)
        bottom_frame.pack(side='top', fill='both', expand=True)

        ttk.Label(bottom_frame, text=text_field_one).grid(
            row=0, column=0, sticky='NW', pady=5, padx=10
        )
        entry_one = ttk.Entry(
            bottom_frame, font=fonts.INPUT_FONT
        )
        entry_one.grid(row=0, column=1, sticky='WE', columnspan=2)

        if count_field == 2:
            ttk.Label(bottom_frame, text=text_field_two).grid(
                row=1, column=0, sticky='NW', pady=5, padx=2
            )
            entry_two = ttk.Entry(
                bottom_frame, font=fonts.INPUT_FONT
            )
            entry_two.grid(row=1, column=1, sticky='WE', columnspan=2)
            btn_ok = ttk.Button(
                bottom_frame, text='OK', style='OK.TButton',
                command=lambda: press_ok_btn(self.get_window, entry_one,
                                             entry_two)
            )
        else:
            btn_ok = ttk.Button(
                bottom_frame, text='OK', style='OK.TButton',
                command=lambda: press_ok_btn(self.get_window, entry_one)
            )
        btn_ok.grid(row=3, column=1, padx=5, sticky='WE', pady=5)
        btn_close = ttk.Button(
            bottom_frame, text='Отмена', style='Close.TButton',
            cursor='X_cursor', command=lambda: press_close_btn(self.get_window)
        )
        btn_close.grid(row=3, column=2, sticky='WE')

        bottom_frame.columnconfigure(1, weight=1)
        bottom_frame.columnconfigure(2, weight=1)

        if count_field == 2:
            self.get_window.bind(
                '<Return>', lambda event: press_ok_btn(
                    self.get_window, entry_one, entry_two
                )
            )
        else:
            self.get_window.bind(
                '<Return>', lambda event: press_ok_btn(
                    self.get_window, entry_one
                )
            )
        self.get_window.bind(
            '<Escape>', lambda event: press_close_btn(self.get_window)
        )


class TreeViewWindowMain:
    def __init__(self):
        self.values = GetRequestsToDB().get_get_requests_people_table_value()

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

        btn_clear = ttk.Button(right_frame, text='Очистить')
        btn_delete = ttk.Button(right_frame, text='Удалить')
        btn_download = ttk.Button(right_frame, text='Выгрузить txt')

        self.tree_view.grid(row=0, column=0, columnspan=4, rowspan=3, sticky='NSEW')
        btn_clear.grid(row=0, column=0, sticky='WE')
        btn_delete.grid(row=1, column=0, pady=5, sticky='WE')
        btn_download.grid(row=2, column=0, sticky='WE')

        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=9)
        self.window.columnconfigure(1, weight=1)

        left_frame.rowconfigure(0, weight=1)
        left_frame.columnconfigure(0, weight=1)

        btn_clear.bind('<Button-1>', lambda event: self.get_choose_value())

        self.completion_tree_view()

    def initialize_ui(self):
        styles.set_global_style(self.window)

        w = 800
        h = 600
        self.window.title('Основные запросы')
        set_position_window_on_center(self.window, width=w, height=h)

    def get_choose_value(self):
        if not self.tree_view.selection():
            raise IndexError('not choose item')

        item = self.tree_view.selection()[0]
        values = self.tree_view.item(item, option="values")
        return values

    def completion_tree_view(self):
        index = 0
        for item in self.values:
            time = gmtime(int(item[4]))
            data = strftime('%A  %x %H:%M', time)
            self.tree_view.insert(
                '', index=index, text=data,
                values=(item[1], item[2], item[0])
            )
            index += 1

    def clear_values(self):
        pass

    def delete_value(self):
        pass

    def download_on_txt(self):
        pass


class DialogWindows:
    def __init__(self):
        self.window_get_two_params = GetWindow
        self.window_tree_view_main = TreeViewWindowMain

    @staticmethod
    def get_one_or_two_params(
                              title, text_field_one, text_field_two=None,
                              header='Заполните!', count_field=1
                              ):

        get_window = GetWindow(title, text_field_one, text_field_two,
                               header, count_field)

        get_window.get_window.wait_window()

        return get_window.one_value, get_window.two_value
