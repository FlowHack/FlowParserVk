from tkinter import Toplevel, messagebox, ttk, YES

from settings.settings import get_logger

logger = get_logger('dialog_windows')

one_value = None
two_value = None


class GetWindow:
    def __init__(self, title, text_field_one, text_field_two=None,
                 header='Заполните!', count_field=1):
        """
        Функция создания диалогового окна с двумя полями или одним для ввода
        данных
        :param count_field: Количество используемых полей (1 или 2)
        :param title: Заголовок окна
        :param text_field_one: Label к первому полю
        :param text_field_two: Label ко второму полю
        :param header: Необязательно поле. Label-заголовок
        :return: ничего
        """
        import scripts.main.styles as styles
        from scripts.main.windows.master import set_position_window_on_center
        from settings.settings import SettingsFunction

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
            font=SettingsFunction.H6_FONT
        ).pack(side='top')

        bottom_frame = ttk.Frame(self.get_window, padding=10)
        bottom_frame.pack(side='top', fill='both', expand=True)

        ttk.Label(bottom_frame, text=text_field_one).grid(
            row=0, column=0, sticky='NW', pady=5, padx=10
        )
        entry_one = ttk.Entry(
            bottom_frame, font=SettingsFunction.INPUT_FONT
        )
        entry_one.grid(row=0, column=1, sticky='WE', columnspan=2)

        if count_field == 2:
            ttk.Label(bottom_frame, text=text_field_two).grid(
                row=1, column=0, sticky='NW', pady=5, padx=2
            )
            entry_two = ttk.Entry(
                bottom_frame, font=SettingsFunction.INPUT_FONT
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


class RequestTreeView:
    def __init__(self):
        import scripts.main.styles as styles
        from scripts.main.windows.master import set_position_window_on_center
        self.window = Toplevel()
        styles.set_global_style(self.window)
        self.window.title('Все запросы')
        w = 700
        h = 500
        set_position_window_on_center(self.window, width=w, height=h)

        self.main_frame = ttk.Frame(self.window)
        self.main_frame.pack(side='top', fill='both', expand=True)

        self.tree_view = ttk.Treeview(
            self.main_frame, columns=('Количество id', 'Параметры')
        )

        self.tree_view.heading('#0', text='Дата')
        self.tree_view.heading('#1', text='Количество id')
        self.tree_view.heading('#2', text='Параметры')

        self.tree_view.column('#1', stretch=YES)
        self.tree_view.column('#2', stretch=YES)
        self.tree_view.column('#0', stretch=YES)

        self.tree_view.grid(row=0, column=0, columnspan=3, sticky='NSEW')


class DialogWindows:
    @staticmethod
    def get_one_or_two_params(
                              title, text_field_one, text_field_two=None,
                              header='Заполните!', count_field=1
                              ):

        get_window = GetWindow(title, text_field_one, text_field_two,
                               header, count_field)

        get_window.get_window.wait_window()

        return get_window.one_value, get_window.two_value

    @staticmethod
    def info_window(title, info_txt):
        """
        Функция создания информационного окна
        :param title: титул окна
        :param info_txt: информационный текст
        :return: ничего
        """
        messagebox.showinfo(title, info_txt)

    @staticmethod
    def warning_window(title, warning_txt):
        """
        Функция создания предупреждающего окна
        :param title: титул окна
        :param warning_txt: предупреждающий текст
        :return: ничего
        """
        messagebox.showwarning(title, warning_txt)

    @staticmethod
    def error_window(title, error_txt):
        """
        Функция создания окна ошибки
        :param title: титул окна
        :param error_txt: текст ошибки
        :return: ничего
        """
        messagebox.showerror(title, error_txt)
