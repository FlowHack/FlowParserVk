from tkinter import ttk, Tk, messagebox
from settings.settings import SettingsFunction
import scripts.main.styles as styles
from sys import exit as exit_ex
from scripts.main.windows.master import set_position_window_on_center

logger = SettingsFunction.get_logger('dialog_windows')

one_value = None
two_value = None


class DialogWindows:

    @staticmethod
    def get_one_or_two_params(
            title, text_field_one, text_field_two=None,
            header='Заполните!', count_field=1):
        """
        Функция создания диалогового окна с двумя полями или одним для ввода
        данных
        :param count_field: Количество используемых полей (1 или 2)
        :param title: Заголовок окна
        :param text_field_one: Label к первому полю
        :param text_field_two: Label ко второму полю
        :param header: Необязательно поле. Label-заголовок
        :return: информацию из двух полей в виде списка
        """
        global one_value, two_value
        one_value, two_value = None, None

        def press_ok_btn(parent, one_entry, two_entry=None):
            """
            Обработка нажатия на кнопку ok
            :param parent: объект инпут окна
            :param one_entry: объект первого инпута
            :param two_entry: объект второго инпута
            :return: данные из полей
            """
            global one_value, two_value

            one_value = one_entry.get()
            if count_field == 2:
                two_value = two_entry.get()

            if (one_value == '') or (two_value == ''):
                one_entry.configure(style='Warning.TEntry', foreground='black')
                if count_field == 2:
                    two_entry.configure(
                        style='Warning.TEntry', foreground='black'
                    )
                parent.update()
            else:
                parent.destroy()

                if count_field == 2:
                    return one_value, two_value

                return one_value

        def press_close_btn(parent):
            """
            Обработка события нажатия на кнопку отмены ввода данных
            :param parent: объект инпут окна
            :return: ничего
            """
            parent.destroy()

        get_window = Tk()
        get_window.resizable(0, 0)
        styles.set_global_style(get_window)
        styles.style_for_ok_and_close_btn()
        styles.style_for_warning_entry()
        get_window.title(title)
        w = 450
        h = (125, 150)[count_field == 2]
        set_position_window_on_center(get_window, width=w, height=h)
        get_window.protocol("WM_DELETE_WINDOW", exit_ex)

        top_frame = ttk.Frame(
            get_window, padding=5, borderwidth=2, relief='groove'
        )
        top_frame.pack(side='top', fill='x')
        ttk.Label(
            top_frame,
            text=header,
            justify='center',
            font=SettingsFunction.H6_FONT
        ).pack(side='top')

        bottom_frame = ttk.Frame(get_window, padding=10)
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
                command=lambda: press_ok_btn(get_window, entry_one, entry_two)
            )
        else:
            btn_ok = ttk.Button(
                bottom_frame, text='OK', style='OK.TButton',
                command=lambda: press_ok_btn(get_window, entry_one)
            )
        btn_ok.grid(row=3, column=1, padx=5, sticky='WE', pady=5)
        btn_close = ttk.Button(
            bottom_frame, text='Отмена', style='Close.TButton',
            cursor='X_cursor', command=lambda: press_close_btn(get_window)
        )
        btn_close.grid(row=3, column=2, sticky='WE')

        bottom_frame.columnconfigure(1, weight=1)
        bottom_frame.columnconfigure(2, weight=1)

        if count_field == 2:
            get_window.bind(
                '<Return>', lambda event: press_ok_btn(
                    get_window, entry_one, entry_two
                )
            )
        else:
            get_window.bind(
                '<Return>', lambda event: press_ok_btn(
                    get_window, entry_one
                )
            )
        get_window.bind(
            '<Escape>', lambda event: press_close_btn(get_window)
        )

        get_window.mainloop()

        return one_value, two_value

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
