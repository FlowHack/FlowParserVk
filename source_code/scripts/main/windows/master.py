from settings.settings import (LABEL_DESCRIPTION, LABEL_HELP_DESCRIPTION,
                               SettingsFunction)
from tkinter import Tk, ttk
import scripts.main.styles as styles
from sys import exit as exit_ex
from PIL import Image, ImageTk
from webbrowser import open as web_open

logger = SettingsFunction.get_logger('master_windows')


def set_position_window_on_center(parent, width: int, height: int):
    """
    Функция установки окна по середине окна
    :param parent: объект окна, которое нужно расположить посередине
    :param width: параметр длины окна
    :param height: параметр высоты окна
    :return: ничего
    """
    sw = parent.winfo_screenwidth()
    sh = parent.winfo_screenheight()
    x = (sw - width) / 2
    y = (sh - height) / 2
    parent.geometry('%dx%d+%d+%d' % (width, height, x, y))


class App(Tk):
    def __init__(self):
        """
        Создание главного окна, вкладок и управление функциями
        """
        self.settings_app = SettingsFunction()
        super().__init__()
        self.app_ico = self.get_app_ico()
        self.initialize_ui()

        notebook = ttk.Notebook(self)
        self.main_book = ttk.Frame(notebook, padding=15)
        self.donat_book = ttk.Frame(notebook, padding=20)

        notebook.add(self.main_book, text='Главная')
        notebook.add(self.donat_book, text='Донаты')
        notebook.pack(expand=True, fill='both')

        self.update()
        self.build_app()

        self.mainloop()

    def initialize_ui(self):
        """
        Функция настройки окна пограммы
        :return: ничего
        """
        self.title(self.settings_app.APP_NAME)
        styles.set_global_style(self)
        set_position_window_on_center(self, width=1100, height=500)
        self.protocol("WM_DELETE_WINDOW", exit_ex)

    def build_app(self):
        self.build_main_book()
        self.build_donat_book()

    def get_app_ico(self):
        """
        Функция получения всех иконок в случае ошибки запустится проверка
        иконок
        :return: Словарь имя: переменная готовой иконки
        """
        x48_FPVK = ImageTk.PhotoImage(Image.open(
            f'{self.settings_app.path_to_dir_ico}/48x48_FPVK.png'
        ))
        x72_FPVK = ImageTk.PhotoImage(Image.open(
            f'{self.settings_app.path_to_dir_ico}/72x72_FPVK.png'
        ))
        x96_FPVK = ImageTk.PhotoImage(Image.open(
            f'{self.settings_app.path_to_dir_ico}/96x96_FPVK.png'
        ))
        x144_FPVK = ImageTk.PhotoImage(Image.open(
            f'{self.settings_app.path_to_dir_ico}/144x144_FPVK.png'
        ))
        x192_FPVK = ImageTk.PhotoImage(Image.open(
            f'{self.settings_app.path_to_dir_ico}/192x192_FPVK.png'
        ))
        x348_FPVK = ImageTk.PhotoImage(Image.open(
            f'{self.settings_app.path_to_dir_ico}/348x348_FPVK.png'
        ))
        x148x30_FH = ImageTk.PhotoImage(Image.open(
            f'{self.settings_app.path_to_dir_ico}/148x30_FH.png'
        ))

        return {
            '48x48_FPVK': x48_FPVK,
            '72x72_FPVK': x72_FPVK,
            '96x96_FPVK': x96_FPVK,
            '144x144_FPVK': x144_FPVK,
            '192x192_FPVK': x192_FPVK,
            '348x348_FPVK': x348_FPVK,
            '148x30_FH': x148x30_FH
        }

    def build_main_book(self):
        """
        Функция отрисовки главной вкладки программы
        :return: ничего
        """
        label_FPVK = ttk.Label(
            self.main_book, image=self.app_ico['348x348_FPVK'],
            cursor='heart'
        )
        button_update = ttk.Button(
            self.main_book, text='Проверить обновления', cursor='exchange'
        )
        label_version = ttk.Label(
            self.main_book, text=f'Version: {self.settings_app.VERSION}'
        )
        label_name_app = ttk.Label(
            self.main_book, text=self.settings_app.APP_NAME, justify='center',
            font=self.settings_app.H1_FONT, foreground='#A3DAFF'
        )
        label_description = ttk.Label(
            self.main_book, text=LABEL_DESCRIPTION,
            justify='center', font=self.settings_app.H5_FONT, wraplength=650
        )
        label_help_description = ttk.Label(
            self.main_book, text=LABEL_HELP_DESCRIPTION,
            justify='center', font=self.settings_app.H6_FONT, wraplength=650
        )
        label_FH = ttk.Label(
            self.main_book, image=self.app_ico['148x30_FH'], cursor='heart',
            justify='center'
        )
        btn_open_page_app = ttk.Button(
            self.main_book, text='Сайт программы', cursor='star',
            command=lambda: web_open(self.settings_app.PAGE_APP)
        )
        btn_open_bot_tg = ttk.Button(
            self.main_book, text='Бот Telegram', cursor='star',
            command=lambda: web_open(self.settings_app.TELEGRAM_BOT_APP)
        )
        btn_open_bot_vk = ttk.Button(
            self.main_book, text='Бот VK', cursor='star',
            command=lambda: web_open(self.settings_app.VK_BOT_APP)
        )

        label_FPVK.grid(row=0, column=0, sticky='EW', padx=15, rowspan=3)
        button_update.grid(row=4, column=0, sticky='S', pady=10)
        label_version.grid(row=5, column=0, sticky='S')
        label_name_app.grid(row=0, column=1, sticky='N', columnspan=4)
        label_description.grid(row=1, column=1, sticky='N', columnspan=4)
        label_help_description.grid(row=2, column=1, sticky='N', columnspan=4)
        label_FH.grid(row=5, column=4, sticky='SWE')
        btn_open_page_app.grid(row=5, column=1, sticky='SWE', padx=10)
        btn_open_bot_tg.grid(row=5, column=2, sticky='SWE')
        btn_open_bot_vk.grid(row=5, column=3, sticky='SWE', padx=10)

        self.main_book.columnconfigure(1, weight=1)
        self.main_book.columnconfigure(2, weight=1)
        self.main_book.columnconfigure(3, weight=1)
        self.main_book.columnconfigure(4, weight=1)

        label_FPVK.bind(
            '<Button-1>', lambda event: web_open(self.settings_app.PAGE_APP)
        )
        label_FH.bind(
            '<Button-1>', lambda event: web_open(self.settings_app.AUTHOR_PAGE)
        )

    def build_donat_book(self):
        caption = 'Бесплатность программы зависит от ваших пожертвований!'
        bank_details = (
            'Номер счёта: '
            f'{self.settings_app.BANK_DETAILS["sberbank"]} (Сбербанк)\n'
            f'ЮMoney: {self.settings_app.BANK_DETAILS["ymoney"]} '
            '(Яндекс деньги)'
        )
        label_main = ttk.Label(
            self.donat_book, text='Донаты', font=self.settings_app.H1_FONT,
            justify='center', foreground='#A3DAFF'
        )
        label_bank_details_caption = ttk.Label(
            self.donat_book, text=caption, font=self.settings_app.H5_FONT,
            justify='center', foreground='#FFC8A3'
        )
        label_bank_details = ttk.Label(
            self.donat_book, text=bank_details, font=self.settings_app.H6_FONT,
            justify='center'
        )
        label_FPVK_1 = ttk.Label(
            self.donat_book, cursor='heart', image=self.app_ico['96x96_FPVK']
        )
        label_FPVK_2 = ttk.Label(
            self.donat_book, cursor='heart', image=self.app_ico['96x96_FPVK']
        )
        btn_copy_sber = ttk.Button(
            self.donat_book, text='Копировать счёт Сбербанка',
            command=lambda: self.settings_app.copy_in_clipboard(
                btn_copy_sber, self.settings_app.BANK_DETAILS['sberbank']
            )
        )
        btn_copy_ymoney = ttk.Button(
            self.donat_book, text='Копировать счёт ЮMoney',
            command=lambda: self.settings_app.copy_in_clipboard(
                btn_copy_ymoney, self.settings_app.BANK_DETAILS['ymoney']
            )
        )

        label_main.grid(row=0, column=0, sticky='S', columnspan=4)
        label_bank_details_caption.grid(
            row=1, column=0, sticky='S', columnspan=4, pady=20
        )
        label_bank_details.grid(row=2, column=0, sticky='N', columnspan=4)
        label_FPVK_1.grid(row=2, column=0, sticky='NW')
        label_FPVK_2.grid(row=2, column=3, sticky='NE')
        btn_copy_sber.grid(row=3, column=1, sticky='WES')
        btn_copy_ymoney.grid(row=3, column=2, sticky='SWE')

        self.donat_book.columnconfigure(0, weight=1)
        self.donat_book.columnconfigure(1, weight=1)
        self.donat_book.columnconfigure(2, weight=1)
        self.donat_book.columnconfigure(3, weight=1)
        self.donat_book.rowconfigure(1, weight=1)
        self.donat_book.rowconfigure(2, weight=2)

        label_FPVK_1.bind(
            '<Button-1>', lambda: web_open(self.settings_app.PAGE_APP)
        )
        label_FPVK_2.bind(
            '<Button-1>', lambda: web_open(self.settings_app.PAGE_APP)
        )
