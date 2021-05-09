import os
from sys import exit as exit_ex
from tkinter import BooleanVar, IntVar, Text, Tk, ttk
from webbrowser import open as web_open

from PIL import Image, ImageTk

from functions import FunctionsForWindows
from my_vk_api import ConfigureVkApi
from settings import (ALCOHOL, APP_COMMUNITY, APP_NAME, APP_PAGE, AUTHOR_PAGE,
                      FOLLOWERS_MAX, LABEL_DESCRIPTION, LABEL_HELP_DESCRIPTION,
                      LAST_SEEN_MAX, LIFE_MAIN, LIST_COUNTRIES, LOGGER,
                      NAME_PARSING, PEOPLE_MAIN, POLITICAL, PROGRESSBAR_MAX,
                      SMOKING, STATUS_VK_PERSON, VERSION, VK_BOT_APP, fonts,
                      path_to_dir_ico, set_position_window_on_center, styles)
from windows import TreeViewWindow

LOGGER = LOGGER('master', 'windows')


class App(Tk):
    """
    Класс отвечающий за запуск главного окна и его создание
    """

    def __init__(self, update: int, OS_NAME: str):
        """
        Создание главного окна, вкладок и управление функциями
        :param update: нужно ли проверить обновление
        :param OS_NAME: имя операционной системы
        :return
        """
        super().__init__()
        self.OS = OS_NAME
        self.app_ico = self.get_app_ico()
        self.initialize_ui()

        #  Панель вкладок в окне
        notebook = ttk.Notebook(self)
        self.main_book = ttk.Frame(notebook, padding=15)
        self.parsing_book = ttk.Frame(notebook)

        notebook.add(self.main_book, text='Главная')
        notebook.add(self.parsing_book, text='Парсинг')

        notebook.pack(expand=True, fill='both')

        # Панель вкладок во вкладке парсинг
        notebook_parsing = ttk.Notebook(self.parsing_book)

        self.parsing_book_groups = ttk.Frame(notebook_parsing, padding=15)
        self.parsing_book_by_groups = ttk.Frame(notebook_parsing, padding=10)

        notebook_parsing.add(self.parsing_book_groups,
                             text='Парсинг по группам')
        notebook_parsing.add(self.parsing_book_by_groups,
                             text='Парсинг по критериям')
        notebook_parsing.pack(expand=True, fill='both', side='top')

        self.update()
        self.build_app()
        self.function_windows = FunctionsForWindows()

        if update == 1:
            LOGGER.info('Начинаем процесс проверки обновлений')
            self.function_windows.check_update(os_name=self.OS)

        self.mainloop()

    def initialize_ui(self):
        """
        Функция настройки окна пограммы
        :return:
        """
        self.title(APP_NAME)
        self.tk.call('wm', 'iconphoto', self._w, self.app_ico['FPVK'])
        styles.set_global_style(self)
        w = 1200
        h = 660
        set_position_window_on_center(self, width=w, height=h)
        self.minsize(w, h)
        self.protocol("WM_DELETE_WINDOW", exit_ex)

    def build_app(self):
        """
        Функция отвечающая за наполнение вкладок программы
        :return:
        """
        self.build_main_book()
        self.update()
        self.build_parsing_book_groups()
        self.update()
        self.build_parsing_book_by_groups()
        self.update()

    @staticmethod
    def get_app_ico():
        """
        Функция получения всех иконок в случае ошибки запустится проверка
        иконок
        :return: Словарь {имя: переменная готовой иконки}
        """
        x48_FPVK = ImageTk.PhotoImage(Image.open(
            f'{path_to_dir_ico}/48x48_FPVK.png'
        ))
        x72_FPVK = ImageTk.PhotoImage(Image.open(
            os.path.join(path_to_dir_ico, '72x72_FPVK.png')
        ))
        x96_FPVK = ImageTk.PhotoImage(Image.open(
            os.path.join(path_to_dir_ico, '96x96_FPVK.png')
        ))
        x144_FPVK = ImageTk.PhotoImage(Image.open(
            os.path.join(path_to_dir_ico, '144x144_FPVK.png')
        ))
        x192_FPVK = ImageTk.PhotoImage(Image.open(
            os.path.join(path_to_dir_ico, '192x192_FPVK.png')
        ))
        x348_FPVK = ImageTk.PhotoImage(Image.open(
            os.path.join(path_to_dir_ico, '348x348_FPVK.png')
        ))
        x148x30_FH = ImageTk.PhotoImage(Image.open(
            os.path.join(path_to_dir_ico, '148x30_FH.png')
        ))
        FPVK = ImageTk.PhotoImage(
            file=os.path.join(path_to_dir_ico, 'FPVK.ico')
        )

        return {
            '48x48_FPVK': x48_FPVK,
            '72x72_FPVK': x72_FPVK,
            '96x96_FPVK': x96_FPVK,
            '144x144_FPVK': x144_FPVK,
            '192x192_FPVK': x192_FPVK,
            '348x348_FPVK': x348_FPVK,
            '148x30_FH': x148x30_FH,
            'FPVK': FPVK
        }

    def build_parsing_book_groups(self):
        """
        Функция отвечающая за наполнение подвкладки "Парсинг по группам"
        вкладки "Парсинг"
        :return:
        """
        left_frame = ttk.Frame(
            self.parsing_book_groups, relief='solid',
            borderwidth=1, padding=1
        )
        right_frame = ttk.Frame(
            self.parsing_book_groups, padding=5
        )
        left_frame.grid(row=0, column=0, sticky='NSWE', padx=3, pady=3)
        right_frame.grid(row=0, column=1, sticky='NSWE', padx=3, pady=3)

        lbl_progress = ttk.Label(
            self.parsing_book_groups, font=fonts.H6_FONT
        )
        progressbar = ttk.Progressbar(
            self.parsing_book_groups, orient='vertical',
            mode='determinate', maximum=PROGRESSBAR_MAX, value=0
        )
        lbl_progress.grid(row=1, column=0, columnspan=2, pady=5, sticky='SWE')
        progressbar.grid(row=2, column=0, columnspan=2, pady=5, sticky='SWE')

        #####################---------LEFT_FRAME---------#####################

        var_easy_parse = BooleanVar()
        var_easy_parse.set(0)

        #  row 0
        lbl_count = ttk.Label(
            left_frame, font=fonts.H1_FONT,
            text='Количество: 0'
        )

        #  row 1
        check_easy_parse = ttk.Checkbutton(
            left_frame, variable=var_easy_parse,
            text='Отключить сбор доп. данных(Дальнейший парсинг по выборке '
                 'недоступен)',
            onvalue=1, offvalue=0
        )

        #  row 2
        txt_groups = Text(
            left_frame, wrap='word', font=fonts.TEXT_FONT,
            foreground=styles.FOREGROUND_TEXT,
            background=styles.BACKGROUND_TEXT
        )

        #  row 3
        lbl_warning = ttk.Label(
            left_frame, foreground='#e10000', font=fonts.H6_FONT,
            text='Вводите исключительно ссылки на группы. И вводите через '
                 '"Enter" '
        )

        #####################---------RIGHT_FRAME---------#####################

        btn_parse = ttk.Button(
            right_frame, text='Парсить'
        )
        btn_up_count = ttk.Button(
            right_frame, text='Обновить кол-во', cursor='exchange'
        )
        btn_show_all = ttk.Button(
            right_frame, text='Все записи'
        )

        widgets = {
            'right_frame': right_frame,
            'left_frame': left_frame,
            'lbl_count': lbl_count,
            'var_easy_parse': var_easy_parse,
            'txt_groups': txt_groups,
            'lbl_progress': lbl_progress,
            'progressbar': progressbar
        }

        ####################-------------GRID-------------####################

        #  left_frame
        #  row 0
        lbl_count.grid(row=0, column=0, sticky='NSWE')
        #  row 1
        check_easy_parse.grid(row=1, column=0, sticky='SWE', pady=7)
        #  row 2
        txt_groups.grid(row=2, column=0, sticky='NSWE')
        #  row 3
        lbl_warning.grid(row=3, column=0, sticky='SWE')

        # right_frame
        #  row 0
        btn_parse.grid(row=0, column=0, sticky='NWE', pady=5)
        #  row 1
        btn_up_count.grid(row=1, column=0, sticky='NWE')
        #  row 2
        btn_show_all.grid(row=2, column=0, sticky='NWE', pady=5)

        left_frame.rowconfigure(2, weight=1)
        left_frame.columnconfigure(0, weight=1)

        right_frame.columnconfigure(0, weight=1)

        self.parsing_book_groups.rowconfigure(0, weight=1)
        self.parsing_book_groups.columnconfigure(0, weight=9)
        self.parsing_book_groups.columnconfigure(1, weight=1)

        btn_show_all.bind('<Button-1>',
                          lambda event: TreeViewWindow(method='view'))
        btn_up_count.bind(
            '<Button-1>',
            lambda event: FunctionsForWindows.update_label_count_group(widgets)
        )
        btn_parse.bind(
            '<Button-1>',
            lambda event: FunctionsForWindows().parsing_groups(widgets)
        )

    def build_parsing_book_by_groups(self):
        """
        Наполнение подвкладки "По критериям" вкладки "Парсинг"
        :return:
        """
        ################-------------PARSING_BOOK-------------################
        left_frame = ttk.Frame(
            self.parsing_book_by_groups, relief='solid', borderwidth=1,
            padding=3
        )
        right_frame = ttk.Frame(
            self.parsing_book_by_groups, padding=5
        )
        left_frame.grid(row=0, column=0, sticky='NSWE')
        right_frame.grid(row=0, column=1, sticky='NSWE')

        progressbar = ttk.Progressbar(
            self.parsing_book_by_groups, orient='horizontal',
            mode='determinate', maximum=PROGRESSBAR_MAX, value=0
        )
        lbl_progress = ttk.Label(
            self.parsing_book_by_groups, text='', font=fonts.H5_FONT
        )

        lbl_progress.grid(row=1, column=0, columnspan=2, pady=5, sticky='SWE')
        progressbar.grid(row=2, column=0, columnspan=2, sticky='SWE')

        #################-------------LEFT_FRAME-------------#################
        #  row 0
        var_need_country = BooleanVar()

        var_need_city_region = BooleanVar()

        var_city_region = BooleanVar()

        var_need_country.set(0)
        var_need_city_region.set(0)
        var_city_region.set(0)

        country_frame = ttk.Frame(left_frame, padding=4)
        chk_country_frame = ttk.Checkbutton(
            country_frame, text='', variable=var_need_country, onvalue=1,
            offvalue=0
        )

        lbl_country = ttk.Label(
            country_frame, text='Страна', font=fonts.H6_FONT,
            foreground=styles.NOTABLE_LABEL_FONT
        )
        __var_country__ = list(LIST_COUNTRIES.keys())
        var_country = ttk.Combobox(
            country_frame, font=fonts.COMBOBOX_FONT, width=36, state='readonly'
        )
        var_country['values'] = __var_country__
        var_country.set(__var_country__[0])

        chk_city_region = ttk.Checkbutton(
            country_frame, variable=var_need_city_region, onvalue=1,
            offvalue=0, text=''
        )
        lbl_city_region = ttk.Label(
            country_frame, text='Город/Регион', font=fonts.H6_FONT,
            foreground=styles.NOTABLE_LABEL_FONT
        )
        rdb_city = ttk.Radiobutton(
            country_frame, text='Город', value=0,
            variable=var_city_region
        )
        rdb_region = ttk.Radiobutton(
            country_frame, text='Регион', value=1,
            variable=var_city_region
        )
        cmb_city_region = ttk.Combobox(
            country_frame, font=fonts.COMBOBOX_FONT, width=36, state='readonly'
        )
        cmb_city_region.set('Нажмите "Настройка"')

        #  row 1
        var_need_relationship = BooleanVar()

        var_need_relationship.set(0)

        relationship_frame = ttk.Frame(left_frame, padding=4)

        chk_relationship_has_photo_frame = ttk.Checkbutton(
            relationship_frame, variable=var_need_relationship,
            text='', onvalue=1, offvalue=0
        )
        lbl_relationship = ttk.Label(
            relationship_frame, text='Семейное положение',
            font=fonts.H6_FONT, foreground=styles.NOTABLE_LABEL_FONT
        )
        var_relationship = ttk.Combobox(
            relationship_frame, font=fonts.COMBOBOX_FONT, width=30,
            state='readonly'
        )
        __var_relationship__ = list(STATUS_VK_PERSON.keys())
        var_relationship['values'] = __var_relationship__
        var_relationship.set(__var_relationship__[0])

        #  row 2
        var_has_photo = BooleanVar()

        var_photo_from = IntVar()
        var_photo_to = IntVar()

        has_photo_frame = ttk.Frame(
            left_frame, padding=4
        )

        lbl_has_photo = ttk.Label(
            has_photo_frame, text='Фотографии', font=fonts.H6_FONT,
            foreground=styles.NOTABLE_LABEL_FONT
        )
        rdb_not_has_photo = ttk.Radiobutton(
            has_photo_frame, variable=var_has_photo,
            text='Неважно', value=0
        )
        rdb_has_photo = ttk.Radiobutton(
            has_photo_frame, variable=var_has_photo,
            text='Есть фото', value=1
        )

        #  row 3
        var_need_old = BooleanVar()
        var_old_from = IntVar()
        var_old_to = IntVar()

        var_need_old.set(0)
        var_old_from.set(18)
        var_old_to.set(40)

        var_need_count_followers = BooleanVar()
        var_followers_from = IntVar()
        var_followers_to = IntVar()

        var_need_count_followers.set(0)
        var_followers_from.set(0)
        var_followers_to.set(50)

        count_followers_old_frame = ttk.Frame(
            left_frame, padding=4
        )

        chk_old = ttk.Checkbutton(
            count_followers_old_frame, variable=var_need_old, onvalue=1,
            offvalue=0,
            text=''
        )
        lbl_old = ttk.Label(
            count_followers_old_frame, font=fonts.H6_FONT, text='Возраст',
            foreground=styles.NOTABLE_LABEL_FONT
        )
        spn_old_from = ttk.Spinbox(
            count_followers_old_frame, width=5, font=fonts.SPINBOX_FONT,
            from_=18, to=99, textvariable=var_old_from, state='readonly'
        )
        lbl_old_to = ttk.Label(
            count_followers_old_frame, text='--', font=fonts.H6_FONT
        )
        spn_old_to = ttk.Spinbox(
            count_followers_old_frame, width=5, font=fonts.SPINBOX_FONT,
            from_=19, to=100, textvariable=var_old_to, state='readonly'
        )

        chk_need_followers = ttk.Checkbutton(
            count_followers_old_frame, variable=var_need_count_followers,
            onvalue=1, offvalue=0
        )
        lbl_followers = ttk.Label(
            count_followers_old_frame, text='Подписчиков',
            font=fonts.H6_FONT, foreground=styles.NOTABLE_LABEL_FONT
        )
        spn_followers_from = ttk.Spinbox(
            count_followers_old_frame, from_=0, to=FOLLOWERS_MAX,
            font=fonts.SPINBOX_FONT, textvariable=var_followers_from
        )
        lbl_followers_to = ttk.Label(
            count_followers_old_frame, text='--', font=fonts.H6_FONT
        )
        spn_followers_to = ttk.Spinbox(
            count_followers_old_frame, from_=1, to=FOLLOWERS_MAX,
            font=fonts.SPINBOX_FONT, textvariable=var_followers_to
        )
        #  row 4
        var_need_last_seen = BooleanVar()

        var_only = BooleanVar()

        var_last_seen_from = IntVar()
        var_last_seen_to = IntVar()

        var_need_last_seen.set(0)
        var_only.set(0)
        var_last_seen_from.set(5)
        var_last_seen_to.set(10)

        only_last_seen_frame = ttk.Frame(
            left_frame, padding=4
        )

        lbl_only = ttk.Label(
            only_last_seen_frame, text='Онлайн', font=fonts.H6_FONT,
            foreground=styles.NOTABLE_LABEL_FONT
        )
        rdb_not_only = ttk.Radiobutton(
            only_last_seen_frame, text='Неважно', variable=var_only,
            value=0
        )
        rdb_only = ttk.Radiobutton(
            only_last_seen_frame, text='Онлайн сейчас', variable=var_only,
            value=1
        )

        chk_need_last_seen = ttk.Checkbutton(
            only_last_seen_frame, variable=var_need_last_seen, onvalue=1,
            offvalue=0
        )
        lbl_last_seen = ttk.Label(
            only_last_seen_frame, text='Последний раз в сети',
            font=fonts.H6_FONT,
            foreground=styles.NOTABLE_LABEL_FONT
        )
        spn_last_seen_from = ttk.Spinbox(
            only_last_seen_frame, from_=0, to=LAST_SEEN_MAX,
            font=fonts.SPINBOX_FONT,
            textvariable=var_last_seen_from, width=5
        )
        lbl_last_seen_to = ttk.Label(
            only_last_seen_frame, text='--', font=fonts.H6_FONT
        )
        spn_last_seen_to = ttk.Spinbox(
            only_last_seen_frame, from_=2, to=LAST_SEEN_MAX,
            font=fonts.SPINBOX_FONT,
            textvariable=var_last_seen_to, width=5
        )
        lbl_last_seen_day = ttk.Label(
            only_last_seen_frame, text='дней назад', font=fonts.H6_FONT
        )

        #  row 5
        var_sex = IntVar()
        var_sex.set(0)

        var_can_send_message = BooleanVar()
        var_can_send_message.set(0)

        send_message_sex_frame = ttk.Frame(
            left_frame, padding=4
        )

        lbl_sex = ttk.Label(
            send_message_sex_frame, text='Пол', font=fonts.H6_FONT,
            foreground=styles.NOTABLE_LABEL_FONT
        )
        rdb_no_sex = ttk.Radiobutton(
            send_message_sex_frame, variable=var_sex, value=0, text='Неважно'
        )
        rdb_female = ttk.Radiobutton(
            send_message_sex_frame, variable=var_sex, value=1, text='Женский'
        )
        rdb_male = ttk.Radiobutton(
            send_message_sex_frame, variable=var_sex, value=2, text='Мужской'
        )

        lbl_send_message = ttk.Label(
            send_message_sex_frame, text='Можно отправить сообщение',
            font=fonts.H6_FONT, foreground=styles.NOTABLE_LABEL_FONT
        )
        rdb_no_matter_send_message = ttk.Radiobutton(
            send_message_sex_frame, variable=var_can_send_message,
            value=0, text='Неважно'
        )
        rdb_can_send_message = ttk.Radiobutton(
            send_message_sex_frame, variable=var_can_send_message,
            value=1, text='Можно'
        )

        #  row 6
        var_need_political = BooleanVar()
        var_need_political.set(0)

        var_need_life_main = BooleanVar()
        var_need_life_main.set(0)

        political_life_main_frame = ttk.Frame(
            left_frame, padding=4
        )

        chk_political = ttk.Checkbutton(
            political_life_main_frame, variable=var_need_political, onvalue=1,
            offvalue=0, text=''
        )
        lbl_political = ttk.Label(
            political_life_main_frame, text='Политические предпочтения',
            font=fonts.H6_FONT, foreground=styles.NOTABLE_LABEL_FONT
        )
        __var_political__ = list(POLITICAL.keys())
        var_political = ttk.Combobox(
            political_life_main_frame, font=fonts.COMBOBOX_FONT, width=25,
            state='readonly'
        )
        var_political['value'] = __var_political__
        var_political.set(__var_political__[0])

        chk_life_main = ttk.Checkbutton(
            political_life_main_frame, variable=var_need_life_main,
            onvalue=1, offvalue=0, text=''
        )
        lbl_life_main = ttk.Label(
            political_life_main_frame, text='Главное в жизни',
            font=fonts.H6_FONT, foreground=styles.NOTABLE_LABEL_FONT
        )
        __var_life_main__ = list(LIFE_MAIN.keys())
        var_life_main = ttk.Combobox(
            political_life_main_frame, font=fonts.COMBOBOX_FONT, width=25,
            state='readonly'
        )
        var_life_main['value'] = __var_life_main__
        var_life_main.set(__var_life_main__[0])

        #  row 7
        var_need_people_main = BooleanVar()
        var_need_people_main.set(0)

        var_need_smoking = BooleanVar()
        var_need_smoking.set(0)

        people_main_smoking_frame = ttk.Frame(
            left_frame, padding=4
        )

        chk_people_main = ttk.Checkbutton(
            people_main_smoking_frame, variable=var_need_people_main,
            onvalue=1, offvalue=0, text=''
        )
        lbl_people_main = ttk.Label(
            people_main_smoking_frame, font=fonts.H6_FONT,
            foreground=styles.NOTABLE_LABEL_FONT, text='Главное в людях'
        )
        __var_people_main__ = list(PEOPLE_MAIN.keys())
        var_people_main = ttk.Combobox(
            people_main_smoking_frame, font=fonts.COMBOBOX_FONT,
            state='readonly'
        )
        var_people_main['value'] = __var_people_main__
        var_people_main.set(__var_people_main__[0])
        chk_smoking = ttk.Checkbutton(
            people_main_smoking_frame, variable=var_need_smoking,
            onvalue=1, offvalue=0, text=''
        )
        lbl_smoking = ttk.Label(
            people_main_smoking_frame, font=fonts.H6_FONT,
            foreground=styles.NOTABLE_LABEL_FONT, text='Отношение к курению'
        )
        __var_smoking__ = list(SMOKING.keys())
        var_smoking = ttk.Combobox(
            people_main_smoking_frame, font=fonts.COMBOBOX_FONT,
            state='readonly'
        )
        var_smoking['value'] = __var_smoking__
        var_smoking.set(__var_smoking__[0])

        #  row 8
        var_need_alcohol = BooleanVar()
        var_need_alcohol.set(0)

        alcohol_frame = ttk.Frame(
            left_frame, padding=4
        )

        chk_alcohol = ttk.Checkbutton(
            alcohol_frame, variable=var_need_alcohol, onvalue=1, offvalue=0,
            text=''
        )
        lbl_alcohol = ttk.Label(
            alcohol_frame, font=fonts.H6_FONT,
            foreground=styles.NOTABLE_LABEL_FONT, text='Отношение к алкоголю'
        )
        __var_alcohol__ = list(ALCOHOL.keys())
        var_alcohol = ttk.Combobox(
            alcohol_frame, font=fonts.COMBOBOX_FONT, state='readonly'
        )
        var_alcohol['value'] = __var_alcohol__
        var_alcohol.set(__var_alcohol__[0])

        #  row 9
        var_need_entry_status = BooleanVar()
        var_need_entry_status.set(0)

        entry_status_frame = ttk.Frame(
            left_frame, padding=4
        )

        chk_entry_status = ttk.Checkbutton(
            entry_status_frame, variable=var_need_entry_status, onvalue=1,
            offvalue=0,
            text=''
        )
        lbl_entry_status = ttk.Label(
            entry_status_frame, text='Ключевое слово в статусе',
            font=fonts.H6_FONT,
            foreground=styles.NOTABLE_LABEL_FONT
        )
        var_entry_status = ttk.Entry(
            entry_status_frame, font=fonts.INPUT_FONT
        )

        #  row 10
        var_need_entry_about = BooleanVar()
        var_need_entry_about.set(0)

        entry_about_frame = ttk.Frame(
            left_frame, padding=4
        )

        chk_entry_about = ttk.Checkbutton(
            entry_about_frame, variable=var_need_entry_about, onvalue=1,
            offvalue=0,
            text=''
        )
        lbl_entry_about = ttk.Label(
            entry_about_frame, font=fonts.H6_FONT,
            text='Ключевое слово в "О себе"',
            foreground=styles.NOTABLE_LABEL_FONT
        )
        var_entry_about = ttk.Entry(
            entry_about_frame, font=fonts.INPUT_FONT
        )
        #  row 11
        var_deactivate = BooleanVar()
        var_deactivate.set(1)

        deactivate_frame = ttk.Frame(
            left_frame, padding=4
        )
        lbl_deactivate = ttk.Label(
            deactivate_frame, text='Заблокированные аккаунты',
            font=fonts.H6_FONT,
            foreground=styles.NOTABLE_LABEL_FONT
        )
        rdb_not_deactivate = ttk.Radiobutton(
            deactivate_frame, variable=var_deactivate, value=0,
            text='Оставить',
        )
        rdb_deactivate = ttk.Radiobutton(
            deactivate_frame, variable=var_deactivate, value=1, text='Убрать'
        )

        # right_frame
        btn_parse = ttk.Button(
            right_frame, text='Парсить'
        )
        btn_choose_record = ttk.Button(
            right_frame, text='Выбрать'
        )
        btn_settings = ttk.Button(
            right_frame, text='Настройка'
        )
        btn_all_record = ttk.Button(
            right_frame, text='Все записи'
        )

        entry_pk = ttk.Entry(
            right_frame
        )

        widgets = {
            'left_frame': left_frame,
            'right_frame': right_frame,
            'var_need_country': var_need_country,
            'var_need_relationship': var_need_relationship,
            'var_need_old': var_need_old,
            'var_need_city_region': var_need_city_region,
            'var_need_count_followers': var_need_count_followers,
            'var_need_last_seen': var_need_last_seen,
            'var_need_political': var_need_political,
            'var_need_people_main': var_need_people_main,
            'var_need_life_main': var_need_life_main,
            'var_need_smoking': var_need_smoking,
            'var_need_alcohol': var_need_alcohol,
            'var_need_entry_status': var_need_entry_status,
            'var_need_entry_about': var_need_entry_about,
            'var_country': var_country,
            'var_city_region': var_city_region,
            'cmb_city_region': cmb_city_region,
            'var_can_send_message': var_can_send_message,
            'var_relationship': var_relationship,
            'var_has_photo': var_has_photo,
            'var_photo_from': var_photo_from,
            'var_photo_to': var_photo_to,
            'var_followers_from': var_followers_from,
            'var_followers_to': var_followers_to,
            'var_last_seen_from': var_last_seen_from,
            'var_last_seen_to': var_last_seen_to,
            'var_only': var_only,
            'var_sex': var_sex,
            'var_entry_about': var_entry_about,
            'var_entry_status': var_entry_status,
            'var_political': var_political,
            'var_life_main': var_life_main,
            'var_people_main': var_people_main,
            'var_smoking': var_smoking,
            'var_alcohol': var_alcohol,
            'var_old_from': var_old_from,
            'var_old_to': var_old_to,
            'lbl_progress': lbl_progress,
            'progressbar': progressbar,
            'lbl_last_seen': lbl_last_seen,
            'lbl_last_seen_to': lbl_last_seen_to,
            'spn_last_seen_from': spn_last_seen_from,
            'spn_last_seen_to': spn_last_seen_to,
            'chk_need_last_seen': chk_need_last_seen,
            'var_deactivate': var_deactivate,
            'lbl_last_seen_day': lbl_last_seen_day,
            'entry_pk': entry_pk,
        }
        ####################-------------GRID-------------####################
        #  row 0
        country_frame.grid(row=0, column=0, sticky='NSWE', pady=6)
        chk_country_frame.grid(row=0, column=0, padx=5, sticky='SW')
        lbl_country.grid(row=0, column=1, sticky='SW')
        var_country.grid(row=0, column=2, sticky='SWE', padx=7)
        chk_city_region.grid(row=0, column=3, sticky='SW', padx=15)
        lbl_city_region.grid(row=0, column=4, sticky='SW')
        rdb_city.grid(row=0, column=5, sticky='SW', padx=5)
        rdb_region.grid(row=0, column=6, sticky='SW')
        cmb_city_region.grid(row=0, column=7, sticky='SWE', padx=5)
        #  row 1
        count_followers_old_frame.grid(row=1, column=0, sticky='NSWE')
        chk_old.grid(row=0, column=0, sticky='SW', padx=5)
        lbl_old.grid(row=0, column=1, sticky='SW')
        spn_old_from.grid(row=0, column=2, sticky='SW', padx=2)
        lbl_old_to.grid(row=0, column=3, sticky='SW', padx=5)
        spn_old_to.grid(row=0, column=4, sticky='SW', padx=2)
        chk_need_followers.grid(row=0, column=5, sticky='SW', padx=15)
        lbl_followers.grid(row=0, column=6, sticky='SW')
        spn_followers_from.grid(row=0, column=7, sticky='SW', padx=2)
        lbl_followers_to.grid(row=0, column=8, sticky='SW', padx=5)
        spn_followers_to.grid(row=0, column=9, sticky='SW', padx=2)
        #  row 2
        relationship_frame.grid(row=2, column=0, sticky='NSWE', pady=7)
        chk_relationship_has_photo_frame.grid(
            row=0, column=0, sticky='SW', padx=5
        )
        lbl_relationship.grid(row=0, column=1, sticky='SW')
        var_relationship.grid(row=0, column=2, sticky='SWE', padx=10)
        #  row 3
        send_message_sex_frame.grid(row=3, column=0, sticky='NSWE')
        lbl_sex.grid(row=0, column=0, sticky='SW', padx=5)
        rdb_no_sex.grid(row=0, column=1, sticky='SW')
        rdb_female.grid(row=0, column=2, sticky='SW', padx=2)
        rdb_male.grid(row=0, column=3, sticky='SW')
        lbl_send_message.grid(row=0, column=4, sticky='SW', padx=10)
        rdb_no_matter_send_message.grid(row=0, column=5, sticky='SW')
        rdb_can_send_message.grid(row=0, column=6, sticky='SW', padx=2)
        #  row 4
        only_last_seen_frame.grid(row=4, column=0, sticky='NSWE')
        lbl_only.grid(row=0, column=0, sticky='SW', padx=5)
        rdb_not_only.grid(row=0, column=1, sticky='SW')
        rdb_only.grid(row=0, column=2, sticky='SW', padx=3)
        chk_need_last_seen.grid(row=0, column=3, sticky='SW', padx=5)
        lbl_last_seen.grid(row=0, column=4, sticky='SW', padx=5)
        spn_last_seen_from.grid(row=0, column=5, sticky='SW')
        lbl_last_seen_to.grid(row=0, column=6, sticky='SW', padx=5)
        spn_last_seen_to.grid(row=0, column=7, sticky='SW')
        lbl_last_seen_day.grid(row=0, column=8, sticky='SW', padx=2)
        #  row 5
        has_photo_frame.grid(row=5, column=0, sticky='NSWE', pady=6)
        lbl_has_photo.grid(row=0, column=0, sticky='SW', padx=5)
        rdb_not_has_photo.grid(row=0, column=1, sticky='SW')
        rdb_has_photo.grid(row=0, column=2, sticky='SW', padx=3)
        #  row 6
        political_life_main_frame.grid(row=6, column=0, sticky='NSWE', pady=6)
        chk_political.grid(row=0, column=0, sticky='SW', padx=5)
        lbl_political.grid(row=0, column=1, sticky='SW')
        var_political.grid(row=0, column=2, sticky='SW', padx=3)
        chk_life_main.grid(row=0, column=3, sticky='SW', padx=10)
        lbl_life_main.grid(row=0, column=4, sticky='SW')
        var_life_main.grid(row=0, column=5, sticky='SW', padx=3)
        #  row 7
        people_main_smoking_frame.grid(row=7, column=0, sticky='NSWE', pady=6)
        chk_people_main.grid(row=0, column=0, sticky='SW', padx=5)
        lbl_people_main.grid(row=0, column=1, sticky='SW')
        var_people_main.grid(row=0, column=2, sticky='SW', padx=3)
        chk_smoking.grid(row=0, column=3, sticky='SW', padx=10)
        lbl_smoking.grid(row=0, column=4, sticky='SW')
        var_smoking.grid(row=0, column=5, sticky='SW', padx=3)
        #  row 8
        alcohol_frame.grid(row=8, column=0, sticky='NSWE', pady=6)
        chk_alcohol.grid(row=0, column=0, sticky='SW', padx=5)
        lbl_alcohol.grid(row=0, column=1, sticky='SW')
        var_alcohol.grid(row=0, column=2, sticky='SW', padx=3)
        #  row 9
        entry_status_frame.grid(row=9, column=0, sticky='NSWE', pady=6)
        chk_entry_status.grid(row=0, column=0, sticky='SW', padx=5)
        lbl_entry_status.grid(row=0, column=1, sticky='SW')
        var_entry_status.grid(row=0, column=2, sticky='SWE', padx=3)
        #  row 10
        entry_about_frame.grid(row=10, column=0, sticky='NSWE', pady=6)
        chk_entry_about.grid(row=0, column=0, sticky='SW', padx=5)
        lbl_entry_about.grid(row=0, column=1, sticky='SW')
        var_entry_about.grid(row=0, column=2, sticky='SWE')
        #  row 11
        deactivate_frame.grid(row=11, column=0, sticky='NSWE')
        lbl_deactivate.grid(row=0, column=0, sticky='SW', padx=5)
        rdb_not_deactivate.grid(row=0, column=1, sticky='SW')
        rdb_deactivate.grid(row=0, column=2, sticky='SW')

        btn_parse.grid(row=0, column=0, sticky='SWE', pady=5)
        btn_choose_record.grid(row=1, column=0, sticky='SWE')
        btn_settings.grid(row=2, column=0, sticky='SWE', pady=5)
        btn_all_record.grid(row=3, column=0, sticky='SWE')

        self.parsing_book_by_groups.columnconfigure(0, weight=9)
        self.parsing_book_by_groups.columnconfigure(1, weight=1)
        self.parsing_book_by_groups.rowconfigure(0, weight=1)

        left_frame.columnconfigure(0, weight=1)

        entry_status_frame.columnconfigure(2, weight=1)
        entry_about_frame.columnconfigure(2, weight=1)

        btn_all_record.bind('<Button-1>', lambda event: TreeViewWindow())
        btn_choose_record.bind(
            '<Button-1>',
            lambda event: TreeViewWindow(
                method='parse', completion_name=NAME_PARSING['by_groups'],
                entry_pk=entry_pk
            )
        )
        rdb_city.bind(
            '<Button-1>',
            lambda event: FunctionsForWindows.setting_region_city(widgets)
        )
        rdb_region.bind(
            '<Button-1>',
            lambda event: FunctionsForWindows.setting_region_city(widgets)
        )
        rdb_not_only.bind(
            '<Button-1>',
            lambda event: FunctionsForWindows.setting_only(widgets)
        )
        rdb_only.bind(
            '<Button-1>',
            lambda event: FunctionsForWindows.setting_only(widgets)
        )
        btn_settings.bind(
            '<Button-1>',
            lambda event: self.function_windows.setting_before_parsing(widgets)
        )
        btn_parse.bind(
            '<Button-1>',
            lambda event: self.function_windows.parsing_by_groups(widgets)
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
            row=0, column=1, sticky='N'
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
            left_frame, text=f'Version: {VERSION}'
        )
        label_FH = ttk.Label(
            left_frame, image=self.app_ico['148x30_FH'], cursor='heart',
            justify='center'
        )
        label_name_app = ttk.Label(
            right_frame, text=APP_NAME, justify='center',
            font=fonts.H1_FONT, foreground='#A3DAFF'
        )
        label_description = ttk.Label(
            right_frame, text=LABEL_DESCRIPTION,
            justify='center', font=fonts.H5_FONT, wraplength=750
        )
        label_help_description = ttk.Label(
            right_frame, text=LABEL_HELP_DESCRIPTION,
            justify='center', font=fonts.H6_FONT, wraplength=750
        )
        btn_open_community_app = ttk.Button(
            right_frame, text='Группа FPVK', cursor='star',
            command=lambda: web_open(APP_COMMUNITY)
        )
        btn_open_bot_app = ttk.Button(
            right_frame, text='VK бот FPVK', cursor='star',
            command=lambda: web_open(VK_BOT_APP)
        )

        label_version.grid(row=0, column=0, pady=5)
        label_FPVK.grid(row=1, rowspan=2, column=0)
        button_authorization.grid(row=4, column=0, pady=10)
        button_update.grid(row=5, column=0)
        label_FH.grid(row=6, column=0, pady=10)
        label_name_app.grid(row=0, column=0, pady=10, columnspan=2)
        label_description.grid(row=1, column=0, columnspan=2)
        label_help_description.grid(
            row=2, column=0, pady=10, columnspan=2
        )
        btn_open_community_app.grid(row=3, column=0, pady=15, sticky='SWE')
        btn_open_bot_app.grid(row=3, column=1, pady=15, sticky='SWE')

        self.main_book.columnconfigure(0, weight=1)
        self.main_book.columnconfigure(1, weight=3)
        left_frame.columnconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)
        right_frame.columnconfigure(1, weight=1)
        self.main_book.rowconfigure(0, weight=1)

        label_FPVK.bind(
            '<Button-1>', lambda event: web_open(APP_PAGE)
        )
        label_FH.bind(
            '<Button-1>', lambda event: web_open(AUTHOR_PAGE)
        )
        button_authorization.bind(
            '<Button-1>',
            lambda event: ConfigureVkApi(ignore_existing_token=True)
        )
        button_update.bind(
            '<Button-1>',
            lambda event: self.function_windows.check_update(
                call=True, os_name=self.OS
            )
        )
