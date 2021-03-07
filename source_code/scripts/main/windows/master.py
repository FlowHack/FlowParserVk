from sys import exit as exit_ex
from tkinter import IntVar, StringVar, Tk, ttk
from webbrowser import open as web_open

from PIL import Image, ImageTk

import scripts.main.styles as styles
from settings.style import font
from scripts.main.additional_functions import (AdditionalFunctions,
                                               AdditionalFunctionsForAPI)
from settings.settings import (LABEL_DESCRIPTION, LABEL_HELP_DESCRIPTION,
                               SettingsFunction, get_logger)
from settings import value_constraints
from settings.dicts import additional_dicts

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
        w = 1200
        h = 630
        set_position_window_on_center(self, width=w, height=h)
        self.minsize(w, h)
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

        btn_parse = ttk.Button(
            right_frame, text='Парсить'
        )
        btn_set_setting = ttk.Button(right_frame, text='Настроить')
        btn_see_old_requests = ttk.Button(
            right_frame, text='Все запросы',
            command=AdditionalFunctions.open_request_tree_view
        )

        #  row 0
        label_country = ttk.Label(
            left_frame, text='Страна*', font=font.H6_FONT
        )
        cmb_country = ttk.Combobox(
            left_frame, font=font.COMBOBOX_FONT, state='readonly'
        )
        cmb_country['values'] = list(additional_dicts.LIST_COUNTRIES.keys())
        cmb_country.set('Россия')
        #  row 1
        var_city_or_region = StringVar()
        var_city_or_region.set('city')
        label_city_or_country = ttk.Label(
            left_frame, text='Парсинг по городу или региону?',
            font=font.H6_FONT
        )
        radio_city = ttk.Radiobutton(left_frame,
                                     variable=var_city_or_region, value='city',
                                     text='Городу'
                                     )
        radio_region = ttk.Radiobutton(left_frame,
                                       variable=var_city_or_region,
                                       value='region', text='Региону'
                                       )
        cmb_city_or_region = ttk.Combobox(
            left_frame, font=font.COMBOBOX_FONT, state='readonly'
        )
        cmb_city_or_region.set('Нажмите "Настроить"')
        #  row 2
        var_sex = IntVar()
        var_sex.set(0)
        label_sex = ttk.Label(
            left_frame, text='Пол', font=font.H6_FONT
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
        #  row 3
        label_status = ttk.Label(
            left_frame, font=font.H6_FONT,
            text='Семейное положение'
        )
        cmb_status = ttk.Combobox(
            left_frame, font=font.COMBOBOX_FONT, state='readonly'
        )
        cmb_status['value'] = list(additional_dicts.STATUS_VK_PERSON.keys())
        cmb_status.set('Не выбрано')
        #  row 4
        var_old_from = IntVar()
        var_old_to = IntVar()
        var_old_from.set(20)
        var_old_to.set(40)

        label_old = ttk.Label(
            left_frame, font=font.H6_FONT, text='Возраст (От|До)'
        )
        spin_old_from = ttk.Spinbox(
            left_frame, font=font.SPINBOX_FONT,
            from_=value_constraints.OLD_YEAR_MIN,
            to=value_constraints.OLD_YEAR_MAX,
            textvariable=var_old_from, state='readonly',
            width=5
        )
        spin_old_to = ttk.Spinbox(
            left_frame, font=font.SPINBOX_FONT,
            from_=value_constraints.OLD_YEAR_MIN,
            to=value_constraints.OLD_YEAR_MAX,
            textvariable=var_old_to, state='readonly',
            width=5
        )
        #  row 5
        var_friends_to = IntVar()
        var_friends_from = IntVar()
        var_friends_from.set(0)
        var_friends_to.set(1000)

        label_friends = ttk.Label(
            left_frame, font=font.H6_FONT,
            text='Количество друзей (От|До)'
        )
        spin_friends_from = ttk.Spinbox(
            left_frame, font=font.SPINBOX_FONT,
            from_=0, to=value_constraints.FRIENDS_MAX,
            textvariable=var_friends_from, width=7
        )
        spin_friends_to = ttk.Spinbox(
            left_frame, font=font.SPINBOX_FONT,
            from_=50, to=value_constraints.FRIENDS_MAX,
            textvariable=var_friends_to, width=7
        )
        #  row 6
        var_follower_to = IntVar()
        var_follower_from = IntVar()
        var_follower_from.set(0)
        var_follower_to.set(400)

        label_follower = ttk.Label(
            left_frame, font=font.H6_FONT,
            text='Количество подписчиков (От|До)'
        )
        spin_follower_from = ttk.Spinbox(
            left_frame, font=font.SPINBOX_FONT,
            from_=0, to=value_constraints.FOLLOWERS_MAX,
            textvariable=var_follower_from, width=6
        )
        spin_follower_to = ttk.Spinbox(
            left_frame, font=font.SPINBOX_FONT,
            from_=50, to=value_constraints.FOLLOWERS_MAX,
            textvariable=var_follower_to, width=6
        )
        #  row 7
        var_only = IntVar()
        var_only.set(0)

        var_old_only = IntVar()
        var_old_only.set(5)

        label_only = ttk.Label(
            left_frame, font=font.H6_FONT, text='Онлайн'
        )
        radio_only = ttk.Radiobutton(
            left_frame, value=1, variable=var_only, text='Онлайн'
        )
        radio_offline = ttk.Radiobutton(
            left_frame, value=0, variable=var_only, text='Неважно'
        )

        label_old_only = ttk.Label(
            left_frame, font=font.H6_FONT,
            text='Последний раз был в сети'
        )
        spin_old_only = ttk.Spinbox(
            left_frame, font=font.SPINBOX_FONT,
            from_=1, to=999, textvariable=var_old_only, state='readonly',
            width=5
        )
        label_old_only_day = ttk.Label(
            left_frame, font=font.H6_FONT,
            text='д. назад'
        )
        #  row 8
        var_photo = IntVar()
        var_photo.set(0)
        label_photo = ttk.Label(
            left_frame, font=font.H6_FONT, text='Наличие фото'
        )
        radio_has_photo = ttk.Radiobutton(
            left_frame, value=1, variable=var_photo, text='Есть фото'
        )
        radio_has_not_photo = ttk.Radiobutton(
            left_frame, value=0, variable=var_photo, text='Неважно'
        )

        progressbar = ttk.Progressbar(
            self.do_book_main, orient='horizontal', length=1000,
            maximum=value_constraints.PROGRESSBAR_MAX
        )
        #  row 9
        var_send_message = IntVar()
        var_send_message.set(0)

        label_sed_message = ttk.Label(
            left_frame,
            font=font.H6_FONT, text='Отправка собщений'
        )
        radio_can_send_message = ttk.Radiobutton(
            left_frame, value=1, variable=var_send_message, text='Возможна'
        )
        radio_cannot_send_message = ttk.Radiobutton(
            left_frame, value=0, variable=var_send_message, text='Неважно'
        )
        #  row 10
        var_group_search = IntVar()
        var_group_search.set(0)

        label_group_search = ttk.Label(
            left_frame,
            font=font.H6_FONT, text='Поиск по группе'
        )
        radio_on_group_search = ttk.Radiobutton(
            left_frame, value=1, variable=var_group_search, text='Включить'
        )
        radio_off_group_search = ttk.Radiobutton(
            left_frame, value=0, variable=var_group_search, text='Отключено'
        )
        entry_group_id = ttk.Entry(
            left_frame, font=font.INPUT_FONT
        )

        #  row 0
        label_country.grid(row=0, column=0, sticky='E', padx=10, pady=15)
        cmb_country.grid(row=0, column=1, sticky='SWE', columnspan=8, pady=15)
        #  row 1
        label_city_or_country.grid(row=1, column=0, sticky='E', padx=10)
        radio_city.grid(row=1, column=1, sticky='SW')
        radio_region.grid(row=1, column=2, sticky='SW')
        cmb_city_or_region.grid(row=1, column=3, sticky='SWE', columnspan=6)
        #  row 2
        label_status.grid(row=3, column=0, sticky='E', padx=20, pady=15)
        cmb_status.grid(row=3, column=1, sticky='SWE', columnspan=8, pady=15)
        #  row 3
        label_old.grid(row=4, column=0, sticky='E', padx=20)
        spin_old_from.grid(row=4, column=1, sticky='SW')
        spin_old_to.grid(row=4, column=2, sticky='SW')
        #  row 4
        label_friends.grid(row=5, column=0, sticky='E', padx=20, pady=15)
        spin_friends_from.grid(row=5, column=1, sticky='SW', pady=15)
        spin_friends_to.grid(row=5, column=2, sticky='SW', pady=15)
        #  row 5
        label_follower.grid(row=6, column=0, sticky='E', padx=20)
        spin_follower_from.grid(row=6, column=1, sticky='SW')
        spin_follower_to.grid(row=6, column=2, sticky='SW')
        #  row 6
        label_sex.grid(row=7, column=0, sticky='E', padx=20, pady=15)
        radio_none_sex.grid(row=7, column=1, sticky='SW', pady=15)
        radio_male.grid(row=7, column=2, sticky='SW', pady=15)
        radio_female.grid(row=7, column=3, sticky='SW', pady=15)
        #  row 7
        label_only.grid(row=8, column=0, sticky='E', padx=25)
        radio_offline.grid(row=8, column=1, sticky='SW')
        radio_only.grid(row=8, column=2, sticky='SW')
        label_old_only.grid(row=8, column=3, sticky='SE')
        spin_old_only.grid(row=8, column=4, sticky='SW', padx=15)
        label_old_only_day.grid(row=8, column=5, sticky='SW')
        #  row 8
        label_photo.grid(row=9, column=0, sticky='E', padx=20, pady=15)
        radio_has_not_photo.grid(row=9, column=1, sticky='SW', pady=15)
        radio_has_photo.grid(row=9, column=2, sticky='SW', pady=15)
        #  row 9
        label_sed_message.grid(row=10, column=0, sticky='E', padx=20)
        radio_cannot_send_message.grid(row=10, column=1, sticky='SW')
        radio_can_send_message.grid(row=10, column=2, sticky='SW')
        #  row 10
        label_group_search.grid(row=11, column=0, sticky='E', padx=20, pady=15)
        radio_off_group_search.grid(row=11, column=1, sticky='SW', pady=15)
        radio_on_group_search.grid(row=11, column=2, sticky='SW', pady=15)

        progressbar.grid(row=1, column=0, columnspan=2, rowspan=2)

        btn_set_setting.grid(row=1, column=0, pady=2)
        btn_see_old_requests.grid(row=2, column=0)

        left_frame.columnconfigure(6, weight=1)

        self.do_book_main.columnconfigure(0, weight=1)

        self.do_book_main.rowconfigure(1, weight=1)
        self.do_book_main.rowconfigure(2, weight=1)

        all_widgets = {
            'window': self,
            'left_frame': left_frame,
            'right_frame': right_frame,
            'btn_set_setting': btn_set_setting,
            'cmb_country': cmb_country,
            'var_city_or_region': var_city_or_region,
            'cmb_city_or_region': cmb_city_or_region,
            'var_sex': var_sex,
            'cmb_status': cmb_status,
            'var_old_from': var_old_from,
            'var_old_to': var_old_to,
            'var_only': var_only,
            'var_photo': var_photo,
            'progressbar': progressbar,
            'btn_parse': btn_parse,
            'label_old_only': label_old_only,
            'spin_old_only': spin_old_only,
            'label_old_only_day': label_old_only_day,
            'var_group_search': var_group_search,
            'entry_group_id': entry_group_id,
            'var_follower_to': var_follower_to,
            'var_follower_from': var_follower_from,
            'var_friends_to': var_friends_to,
            'var_friends_from': var_friends_from,
            'var_send_message': var_send_message

        }
        radio_only.bind(
            '<Button-1>', lambda event: self.set_widget_old_only(
                widgets=all_widgets
            )
        )
        radio_offline.bind(
            '<Button-1>', lambda event: self.set_widget_old_only(
                widgets=all_widgets
            )
        )
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
        radio_on_group_search.bind(
            '<Button-1>', lambda event: self.set_entry_for_group_search(
                widgets=all_widgets
            )
        )
        radio_off_group_search.bind(
            '<Button-1>', lambda event: self.set_entry_for_group_search(
                widgets=all_widgets
            )
        )
        btn_set_setting.bind(
            '<Button-1>',
            lambda event: self.function_api.settings_before_parsing(
                widgets=all_widgets
            )
        )
        btn_parse.bind(
            '<Button-1>', lambda event: self.function_api.main_parsing(
                widgets=all_widgets
            )
        )

    def build_main_book(self):
        """
        Функция отрисовки главной вкладки программы
        :return: ничего
        """
        left_frame = ttk.Frame(
            self.main_book, borderwidth=2, relief='groove', padding=10
        )
        left_frame.grid(
            row=0, column=0, sticky='SN', padx=10
        )
        right_frame = ttk.Frame(
            self.main_book, padding=10, borderwidth=2, relief='groove'
        )
        right_frame.grid(
            row=0, column=1, sticky='NW'
        )

        label_FPVK = ttk.Label(
            left_frame, image=self.app_ico['348x348_FPVK'],
            cursor='heart'
        )
        button_update = ttk.Button(
            left_frame, text='Проверить обновления', cursor='exchange'
        )
        button_authorization = ttk.Button(
            left_frame, text='Авторизоваться'
        )
        label_version = ttk.Label(
            left_frame, text=f'Version: {self.settings_app.VERSION}'
        )
        label_FH = ttk.Label(
            left_frame, image=self.app_ico['148x30_FH'], cursor='heart',
            justify='center'
        )
        label_name_app = ttk.Label(
            right_frame, text=self.settings_app.APP_NAME, justify='center',
            font=font.H1_FONT, foreground='#A3DAFF'
        )
        label_description = ttk.Label(
            right_frame, text=LABEL_DESCRIPTION,
            justify='center', font=font.H5_FONT, wraplength=650
        )
        label_help_description = ttk.Label(
            right_frame, text=LABEL_HELP_DESCRIPTION,
            justify='center', font=font.H6_FONT, wraplength=650
        )
        btn_open_page_app = ttk.Button(
            right_frame, text='Сайт программы', cursor='star',
            command=lambda: web_open(self.settings_app.PAGE_APP)
        )

        label_version.grid(row=0, column=0, pady=5)
        label_FPVK.grid(row=1, rowspan=2, column=0)
        button_authorization.grid(row=4, column=0, pady=10)
        button_update.grid(row=5, column=0)
        label_FH.grid(row=6, column=0, pady=10)
        label_name_app.grid(row=0, column=0, pady=10)
        label_description.grid(row=1, column=0, sticky='SWE')
        label_help_description.grid(row=2, column=0, sticky='SWE', pady=10)
        btn_open_page_app.grid(row=3, column=0, pady=15, sticky='SWE')

        self.main_book.columnconfigure(0, weight=1)
        self.main_book.columnconfigure(1, weight=3)

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
            self.donat_book, text='Донаты', font=font.H1_FONT,
            justify='center', foreground='#A3DAFF'
        )
        label_bank_details_caption = ttk.Label(
            self.donat_book, text=caption, font=font.H5_FONT,
            justify='center', foreground='#FFC8A3'
        )
        label_bank_details = ttk.Label(
            self.donat_book, text=bank_details, font=font.H6_FONT,
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
