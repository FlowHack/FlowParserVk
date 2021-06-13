import os
from sys import exit as exit_ex
from time import time
from tkinter import Text, Tk, Toplevel, messagebox, ttk

from PIL import ImageTk
import clipboard

from settings import (DEFAULT_VALUE_FOR_BD, LOGGER, WARNING_MSG, fonts,
                      path_to_dir_ico, set_position_window_on_center, styles, LICENSE_AGREEMENT)


class PersonAndAgreementData:
    """
    Класс отвечающий за окно персонального соглашения и лицензионного
    """

    def __init__(self):
        self.start_function_time = time()
        self.agreement = False
        self.lose_agreement_count: int = 0

        self.agreement_window = Tk()
        self.initialize_ui()

        main_frame = ttk.Frame(self.agreement_window, padding=10)
        main_frame.pack(side='top', fill='both', expand=True)

        text = Text(main_frame, wrap='word', width=71, height=14)
        text.insert(1.0, LICENSE_AGREEMENT)
        text.grid(row=0, column=0, sticky='NSEW', columnspan=2)

        btn_agreement = ttk.Button(main_frame, text='Принять')
        btn_agreement.grid(row=1, column=0, sticky='EW', pady=5)
        ttk.Button(
            main_frame, text='Отмена', command=exit_ex
        ).grid(row=1, column=1, sticky='EW')

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        btn_agreement.bind(
            '<Button-3>', lambda event: self.done_agreement()
        )
        btn_agreement.bind(
            '<Button-1>', lambda event: self.lose_agreement()
        )

    def initialize_ui(self):
        """
        Инициализация окна
        :return:
        """
        styles.set_global_style(self.agreement_window)
        styles.style_for_ok_and_close_btn()
        styles.style_for_warning_entry()

        w = 600
        h = 300
        FPVK = ImageTk.PhotoImage(
            file=os.path.join(path_to_dir_ico, 'FPVK.ico')
        )
        self.agreement_window.title('Пользовательское соглашение!')
        set_position_window_on_center(self.agreement_window, w, h)
        self.agreement_window.tk.call(
            'wm', 'iconphoto', self.agreement_window._w, FPVK
        )
        self.agreement_window.protocol("WM_DELETE_WINDOW", exit_ex)

    def done_agreement(self):
        """
        Обработка нажатия
        :return:
        """
        self.agreement = True
        self.agreement_window.destroy()

    def lose_agreement(self):
        """
        Шуточная обработка неправильного подтверждения прочтения
        :return:
        """
        if self.lose_agreement_count == 0:
            messagebox.showinfo(
                'Прочтите пользовательское соглашение!',
                'Вы не прочитали соглашение!'
            )
            self.lose_agreement_count = 1
        elif self.lose_agreement_count == 1:
            messagebox.showinfo(
                'Прочтите пользовательское соглашение!',
                'Вы не собираетесь читать пользовательское '
                'соглашение?!\n\nЯ всё же настаиваю на его прочтении! '
            )
            self.lose_agreement_count = 2
        elif self.lose_agreement_count == 2:
            lose_time = time() - self.start_function_time
            messagebox.showwarning(
                'Прочтите пользовательское соглашение!',
                f'Я придумал! Буду считать сколько времени вы тратите '
                f'впустую.\nНа данный момент вы потратили '
                f'{lose_time:.0f}сек.\n\nПрочитайте пользовательское '
                f'соглашение! '
            )
            self.lose_agreement_count = 3
        else:
            lose_time = time() - self.start_function_time
            messagebox.showwarning(
                'Прочтите пользовательское соглашение!',
                f'На данный момент вы потратили {lose_time:.0f}сек.\n\nНе '
                f'тратьте своё время просто так. Прочитайте '
                f'пользовательское соглашение! '
            )


class GetTokenWindow:
    """
    Класс отвечающий за окно получения токена
    """

    def __init__(self):
        self.token = None

        self.token_window = Toplevel()
        self.initialize_ui()

        top_frame = ttk.Frame(
            self.token_window, padding=5, borderwidth=2, relief='groove'
        )
        top_frame.pack(side='top', fill='x')

        text_label = 'Скопируйте значение URL и вставьте его ниже.'
        ttk.Label(
            top_frame, text=text_label, justify='center', font=fonts.H6_FONT
        ).pack(side='top')

        bottom_frame = ttk.Frame(
            self.token_window, padding=10
        )
        bottom_frame.pack(side='top', fill='both', expand=True)
        label_token = ttk.Label(
            bottom_frame, justify='center', text='Ссылка', font=fonts.H6_FONT
        )
        self.entry_token = ttk.Entry(
            bottom_frame, font=fonts.INPUT_FONT
        )
        btn_ok = ttk.Button(
            bottom_frame, text='OK', style='OK.TButton',
        )
        btn_paste = ttk.Button(
            bottom_frame, text='Вставить ссылку',
        )
        btn_cancel = ttk.Button(
            bottom_frame, text='Отмена', style='Close.TButton',
        )

        label_token.grid(row=0, column=0, sticky='SE', pady=10, padx=5)
        self.entry_token.grid(
            row=0, column=1, sticky='SWE', columnspan=3, pady=10
        )
        btn_ok.grid(row=1, column=1, sticky='SWE', pady=10)
        btn_paste.grid(row=1, column=2, sticky='SWE', pady=10)
        btn_cancel.grid(row=1, column=3, sticky='SWE', pady=10)

        bottom_frame.columnconfigure(1, weight=1)
        bottom_frame.columnconfigure(2, weight=1)
        bottom_frame.columnconfigure(3, weight=1)

        btn_ok.bind('<Button-1>', lambda event: self.ok())
        btn_cancel.bind('<Button-1>', lambda event: self.cancel())
        btn_paste.bind('<Button-1>', lambda event: self.paste())

    def initialize_ui(self):
        """
        Инициализация окна
        :return:
        """
        styles.set_global_style(self.token_window)
        styles.style_for_ok_and_close_btn()
        styles.style_for_warning_entry()

        w = 850
        h = 150
        FPVK = ImageTk.PhotoImage(
            file=os.path.join(path_to_dir_ico, 'FPVK.ico')
        )
        self.token_window.resizable(0, 0)
        self.token_window.title('Получение токена VK')
        set_position_window_on_center(self.token_window, width=w, height=h)
        self.token_window.tk.call(
            'wm', 'iconphoto', self.token_window._w, FPVK
        )

    def paste(self):
        url = clipboard.paste()
        self.entry_token.insert(0, url)

    def cancel(self):
        """
        Обработка нажатия отмены введения токена
        :return:
        """
        self.token = DEFAULT_VALUE_FOR_BD
        messagebox.showwarning(
            'Отмена авторизации', WARNING_MSG['VK_API']['cancel_get_token']
        )
        LOGGER.warning('Во время выполнения метода get_token, он был отменён')
        self.token_window.destroy()

    def ok(self):
        """
        Обработка нажатия Ок
        :return:
        """
        value = self.entry_token.get()

        if value is None:
            self.entry_token.configure(
                style='Warning.TEntry', foreground='black'
            )
            return

        self.token = value
        self.token_window.destroy()


class AdditionalWindows:
    """
    Класс дополнительных окон
    """

    def __init__(self):
        self.get_token_window = GetTokenWindow
        self.person_and_agreement_data_window = PersonAndAgreementData

    def person_and_agreement_data(self):
        """
        Функция запуска окна лицензионного соглашения и получения из него
        данных
        :return:
        """
        window = self.person_and_agreement_data_window()

        window.agreement_window.wait_window()

        return window.agreement

    def get_token(self):
        """
        Функция запуска окна получения токена и получения из него данных
        :return:
        """
        window = self.get_token_window()

        window.token_window.wait_window()

        return window.token
