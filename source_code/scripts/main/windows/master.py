from sys import exit as exit_ex
from tkinter import IntVar, StringVar, Tk, ttk
from webbrowser import open as web_open

from PIL import Image, ImageTk

import scripts.main.styles as styles
from scripts.main.additional_functions import (AdditionalFunctions,
                                               AdditionalFunctionsForAPI)
from settings.settings import (LABEL_DESCRIPTION, LABEL_HELP_DESCRIPTION,
                               SettingsFunction, get_logger)

logger = get_logger('master_windows')


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


class App(Tk, AdditionalFunctions):
    def __init__(self):
        """
        Создание главного окна, вкладок и управление функциями
        """
        self.settings_app = SettingsFunction()
        super().__init__()
        self.app_ico = self.get_app_ico()
        self.initialize_ui()

        #  Панель вкладок в окне
        notebook = ttk.Notebook(self)
        self.main_book = ttk.Frame(notebook, padding=15)
        self.donat_book = ttk.Frame(notebook, padding=20)
        self.do_book = ttk.Frame(notebook)

        notebook.add(self.main_book, text='Главная')
        notebook.add(self.do_book, text='Действия')
        notebook.add(self.donat_book, text='Донаты')

        notebook.pack(expand=True, fill='both')

        # Панель вкладок во вкладке действий
        notebook_do = ttk.Notebook(self.do_book)

        self.do_book_main = ttk.Frame(notebook_do, padding=15)

        notebook_do.add(self.do_book_main, text='Общий парсинг')
        notebook_do.pack(expand=True, fill='both', side='top')

        self.update()
        self.build_app()
        self.function_api = AdditionalFunctionsForAPI()

        self.mainloop()

    def initialize_ui(self):
        """
        Функция настройки окна пограммы
        :return: ничего
        """
        self.title(self.settings_app.APP_NAME)
        styles.set_global_style(self)
        set_position_window_on_center(self, width=1200, height=500)
        self.minsize(1200, 500)
        self.protocol("WM_DELETE_WINDOW", exit_ex)

    def build_app(self):
        """
        Функция отвечающая за наполнение вкладок программы
        :return:
        """
        self.build_main_book()
        self.build_donat_book()
        self.build_do_book_main()
        self.update()

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

    def build_do_book_main(self):
        left_frame = ttk.Frame(
            self.do_book_main, padding=10, borderwidth=2, relief='groove'
        )
        left_frame.grid(
            row=0, column=0, sticky='SWE', padx=10
        )
        right_frame = ttk.Frame(
            self.do_book_main, padding=10, borderwidth=2, relief='groove'
        )
        right_frame.grid(
            row=0, column=1, sticky='NW'
        )

        btn_set_setting = ttk.Button(right_frame, text='Настроить')
        btn_see_old_requests = ttk.Button(
            right_frame, text='Все запросы',
            command=AdditionalFunctions.open_request_tree_view
        )

        #  row 0
        label_country = ttk.Label(
            left_frame, text='Страна*', font=self.settings_app.H6_FONT
        )
        cmb_country = ttk.Combobox(
            left_frame, font=self.settings_app.COMBOBOX_FONT, state='readonly'
        )
        cmb_country['values'] = list(self.settings_app.LIST_COUNTRIES.keys())
        cmb_country.set('Россия')
        #  row 1
        var_city_or_region = StringVar()
        var_city_or_region.set('city')
        label_city_or_country = ttk.Label(
            left_frame, text='Парсинг по городу или региону?',
            font=self.settings_app.H6_FONT
        )
        radio_city = ttk.Radiobutton(left_frame,
                                     variable=var_city_or_region, value='city',
                                     text='Городу'
                                     )
        radio_region = ttk.Radiobutton(left_frame,
                                       variable=var_city_or_region,
                                       value='region', text='Региону'
                                       )
        #  row 2
        label_var_city_or_country = ttk.Label(
            left_frame, text='Город', font=self.settings_app.H6_FONT
        )
        cmb_city_or_region = ttk.Combobox(
            left_frame, font=self.settings_app.COMBOBOX_FONT, state='readonly'
        )
        cmb_city_or_region.set('Нажмите "Настроить"')
        #  row 3
        var_sex = IntVar()
        var_sex.set(0)
        label_sex = ttk.Label(
            left_frame, text='Пол', font=self.settings_app.H6_FONT
        )
        radio_male = ttk.Radiobutton(
            left_frame, variable=var_sex, value=2, text='Мужской'
        )
        radio_female = ttk.Radiobutton(
            left_frame, variable=var_sex, value=1, text='Женский'
        )
        radio_none_sex = ttk.Radiobutton(
            left_frame, variable=var_sex, value=0, text='Не выбрано'
        )
        #  row 4
        label_status = ttk.Label(
            left_frame, font=self.settings_app.H6_FONT,
            text='Семейное положение'
        )
        cmb_status = ttk.Combobox(
            left_frame, font=self.settings_app.COMBOBOX_FONT, state='readonly'
        )
        cmb_status['value'] = list(SettingsFunction.STATUS_VK_PERSON.keys())
        cmb_status.set('Не выбрано')
        #  row 5
        var_old_from = StringVar()
        var_old_from.set(20)
        var_old_to = StringVar()
        var_old_to.set(40)
        label_old = ttk.Label(
            left_frame, font=self.settings_app.H6_FONT, text='Возраст'
        )
        spin_old_from = ttk.Spinbox(
            left_frame, font=self.settings_app.SPINBOX_FONT,
            from_=14, to=90, textvariable=var_old_from, state='readonly',
            width=5
        )
        spin_old_to = ttk.Spinbox(
            left_frame, font=self.settings_app.SPINBOX_FONT,
            from_=14, to=90, textvariable=var_old_to, state='readonly',
            width=5
        )
        #  row 6
        var_only = IntVar()
        var_only.set(1)
        label_only = ttk.Label(
            left_frame, font=self.settings_app.H6_FONT, text='Онлайн'
        )
        radio_only = ttk.Radiobutton(
            left_frame, value=1, variable=var_only, text='Онлайн'
        )
        radio_offline = ttk.Radiobutton(
            left_frame, value=0, variable=var_only, text='Неважно'
        )
        #  row 7
        var_photo = IntVar()
        var_photo.set(1)
        label_photo = ttk.Label(
            left_frame, font=self.settings_app.H6_FONT, text='Наличие фото'
        )
        radio_has_photo = ttk.Radiobutton(
            left_frame, value=1, variable=var_photo, text='Есть фото'
        )
        radio_has_not_photo = ttk.Radiobutton(
            left_frame, value=0, variable=var_photo, text='Неважно'
        )

        progressbar = ttk.Progressbar(
            self.do_book_main, orient='horizontal', length=1000,
            maximum=self.settings_app.PROGRESSBAR_MAXIMUM
        )

        #  row 0
        label_country.grid(row=0, column=0, sticky='E', padx=10)
        cmb_country.grid(row=0, column=1, sticky='SWE', columnspan=4)
        #  row 1
        label_city_or_country.grid(row=1, column=0, sticky='W', pady=15,
                                   padx=10)
        radio_city.grid(row=1, column=1, sticky='SW', pady=15)
        radio_region.grid(row=1, column=2, sticky='SW', pady=15)
        #  row 2
        label_var_city_or_country.grid(row=2, column=0, sticky='E', padx=20)
        cmb_city_or_region.grid(row=2, column=1, sticky='SWE', columnspan=4)
        #  row 3
        label_sex.grid(row=3, column=0, sticky='E', padx=25, pady=15)
        radio_none_sex.grid(row=3, column=1, sticky='SW', pady=15)
        radio_male.grid(row=3, column=2, sticky='SW', pady=15, padx=10)
        radio_female.grid(row=3, column=3, sticky='SW', pady=15)
        #  row 4
        label_status.grid(row=4, column=0, sticky='E', padx=25)
        cmb_status.grid(row=4, column=1, sticky='SWE', columnspan=4)
        #  row 5
        label_old.grid(row=5, column=0, sticky='E', padx=25, pady=15)
        spin_old_from.grid(row=5, column=1, sticky='SW', pady=15)
        spin_old_to.grid(row=5, column=2, sticky='SW', pady=15)
        #  row 6
        label_only.grid(row=6, column=0, sticky='E', padx=25)
        radio_only.grid(row=6, column=1, sticky='SW')
        radio_offline.grid(row=6, column=2, sticky='SW', padx=10)
        #  row 7
        label_photo.grid(row=7, column=0, sticky='E', padx=25, pady=15)
        radio_has_photo.grid(row=7, column=1, sticky='SW', pady=15)
        radio_has_not_photo.grid(
            row=7, column=2, sticky='SW', padx=10, pady=15
        )

        progressbar.grid(row=1, column=0, columnspan=2, pady=35)

        btn_set_setting.grid(row=0, column=0)
        btn_see_old_requests.grid(row=2, column=0)

        left_frame.columnconfigure(4, weight=1)

        self.do_book_main.columnconfigure(0, weight=1)

        all_widgets = {
            'window': self.main_book,
            'left_frame': left_frame,
            'right_frame': right_frame,
            'btn_set_setting': btn_set_setting,
            'label_var_city_or_country': label_var_city_or_country,
            'cmb_country': cmb_country,
            'var_city_or_region': var_city_or_region,
            'cmb_city_or_region': cmb_city_or_region,
            'var_sex': var_sex,
            'cmb_status': cmb_status,
            'var_old_from': var_old_from,
            'var_old_to': var_old_to,
            'var_only': var_only,
            'var_photo': var_photo,
            'progressbar': progressbar
        }

        radio_region.bind(
            '<Button-1>', lambda event: self.set_label_and_var_city_or_region(
                widgets=all_widgets
            )
        )
        radio_city.bind(
            '<Button-1>', lambda event: self.set_label_and_var_city_or_region(
                widgets=all_widgets
            )
        )
        btn_set_setting.bind(
            '<Button-1>',
            lambda event: self.function_api.get_cities_or_regions_combobox(
                widgets=all_widgets
            )
        )

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
        """
        Функция постройки вкладки донатов
        :return: ничего
        """
        caption = 'Бесплатность проекта зависит от ваших пожертвований!'
        bank_details = (
            'Номер счёта: '
            f'{self.settings_app.BANK_DETAILS["sberbank"]} (Сбербанк)\n'
            f'ЮMoney: {self.settings_app.BANK_DETAILS["ymoney"]} '
            '(Яндекс деньги)\n'
            f'VISA: {self.settings_app.BANK_DETAILS["qiwi_visa"]} (QIWI VISA)'
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
        btn_copy_qiwi_visa = ttk.Button(
            self.donat_book, text='Копировать счёт VISA',
            command=lambda: self.settings_app.copy_in_clipboard(
                btn_copy_qiwi_visa, self.settings_app.BANK_DETAILS['qiwi_visa']
            )
        )

        label_main.grid(row=0, column=0, sticky='S', columnspan=5)
        label_bank_details_caption.grid(
            row=1, column=0, sticky='S', columnspan=5, pady=20
        )
        label_bank_details.grid(row=2, column=0, sticky='N', columnspan=5)
        label_FPVK_1.grid(row=2, column=0, sticky='NW')
        label_FPVK_2.grid(row=2, column=4, sticky='NE')
        btn_copy_sber.grid(row=3, column=1, sticky='WES')
        btn_copy_ymoney.grid(row=3, column=2, sticky='SWE')
        btn_copy_qiwi_visa.grid(row=3, column=3, sticky='SWE')

        self.donat_book.columnconfigure(0, weight=1)
        self.donat_book.columnconfigure(1, weight=1)
        self.donat_book.columnconfigure(2, weight=1)
        self.donat_book.columnconfigure(3, weight=1)
        self.donat_book.columnconfigure(4, weight=1)
        self.donat_book.rowconfigure(1, weight=1)
        self.donat_book.rowconfigure(2, weight=2)

        label_FPVK_1.bind(
            '<Button-1>', lambda: web_open(self.settings_app.PAGE_APP)
        )
        label_FPVK_2.bind(
            '<Button-1>', lambda: web_open(self.settings_app.PAGE_APP)
        )
