import os, tempfile, zipfile, requests
from requests.exceptions import ConnectionError
import shutil
from logging import INFO, Formatter, getLogger
from logging.handlers import RotatingFileHandler
from sys import exit as exit_ex
from tempfile import TemporaryDirectory
from tkinter import Tk, ttk
from tkinter.messagebox import showerror, showinfo
from tkinter.ttk import Style

from PIL import ImageTk

path = os.getcwd()
os.chdir('..')
path_app = os.getcwd()

VERSION_UPDATER = '0.1.0'
URL_REPO = 'https://github.com/FlowHack/FlowParserVk/archive/refs/heads/master.zip'
URL_VERSION_REPO = 'https://github.com/FlowHack/FlowParserVk/archive/refs/heads/control/version.zip'
REPO_BRANCH = 'FlowParserVk-master'
REPO_VERSION_BRANCH = 'FlowParserVk-control-version'
REPO_UPDATER_BRANCH = 'FlowParserVk-control-updater'

OS = 'Windows'

lbl_head_font = ('Times New Roman', 14, 'italic bold')
lbl_progress_font = ('Times New Roman', 11, 'italic bold')
lbl_font = ('Times New Roman', 10, 'italic bold')

logger = getLogger('updater')
logger.setLevel(INFO)

logger_format = '[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'
formatter = Formatter(fmt=logger_format, datefmt=date_format)

handler = RotatingFileHandler(
    f'{path}/main.log',
    maxBytes=5252880,
    backupCount=5,
)

handler.setFormatter(formatter)
logger.addHandler(handler)


class Updater(Tk):
    def __init__(self):
        super().__init__()
        self.initialize_ui()

        version = self.get_version()

        top_frame = ttk.Frame(
            self, padding=10, relief='groove', borderwidth=0.5
        )
        button_frame = ttk.Frame(
            self, padding=10, relief='solid', borderwidth=0.5
        )

        top_frame.grid(row=0, column=0, sticky='NSWE')
        button_frame.grid(row=1, column=0, sticky='NSWE')

        main_lbl = ttk.Label(
            top_frame, text='Обновление FlowParserVk',
            font=lbl_head_font, justify='center'
        )
        os_lbl = ttk.Label(
            top_frame, text=f'Операционная система: {OS}',
            font=lbl_font
        )
        new_version_lbl = ttk.Label(
            top_frame, text=f'Будет установлена версия: {version}',
            font=lbl_font
        )
        beta_lbl = ttk.Label(
            top_frame, text=f'Версия загрузчика: {VERSION_UPDATER}',
            font=lbl_font
        )

        self.info_lbl = ttk.Label(
            button_frame, font=lbl_progress_font, justify='center',
            text='Нажмите кнопку "Начать", чтобы обновить приложение',
            wraplength=600
        )
        self.progressbar = ttk.Progressbar(
            button_frame, orient='horizontal',
            mode='determinate', maximum=100, value=0
        )
        self.btn_start = ttk.Button(
            button_frame, text='Начать'
        )

        main_lbl.grid(row=0, column=0, pady=5)
        os_lbl.grid(row=1, column=0, sticky='SWE')
        new_version_lbl.grid(row=2, column=0, sticky='SWE')
        beta_lbl.grid(row=3, column=0, sticky='SWE')
        self.info_lbl.grid(row=0, column=0)
        self.progressbar.grid(row=1, column=0, sticky='SWE', pady=10)
        self.btn_start.grid(row=2, column=0, sticky='S')

        self.columnconfigure(0, weight=1)
        top_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.btn_start.bind('<Button-1>', lambda event: self.updater())

        self.mainloop()

    def initialize_ui(self):
        FPVK = ImageTk.PhotoImage(file=os.path.join(path, 'FPVK.ico'))
        w = 450
        h = 220

        self.title('Установщик')
        self.tk.call('wm', 'iconphoto', self._w, FPVK)
        self.protocol("WM_DELETE_WINDOW", exit_ex)

        style = Style()
        style.theme_use('alt')
        self.set_window_on_center(w, h)
        self.resizable(0, 0)

    def set_window_on_center(self, width, height):
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - width) / 2
        y = (sh - height) / 2
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

    @staticmethod
    def compile_old_app():
        os.chdir(path_app)

        if os.path.exists('old_version'):
            shutil.rmtree('old_version', ignore_errors=True, onerror=None)

        listdir = os.listdir(path_app)

        os.mkdir('old_version')
        path_old = os.path.join(path_app, 'old_version')
        path_settings = os.path.join(path_old, 'settings')

        for item in listdir:
            if item == REPO_UPDATER_BRANCH or item == 'old_version':
                continue

            shutil.move(os.path.join(path_app, item), path_old)

        if 'settings.db' in os.listdir(path_settings):
            path_to_db = os.path.join(path_old, 'settings', 'settings.db')
        else:
            path_to_db = None

        return path_to_db

    @staticmethod
    def compile_new_app(new_app):
        listdir = os.listdir(new_app)

        for item in listdir:
            shutil.move(os.path.join(new_app, item), path_app)

        shutil.rmtree(new_app, ignore_errors=True, onerror=None)

    def updater(self):
        self.info_lbl.configure(text='Подготовка файлов')
        logger.info('Создание папки со старой программой')
        self.info_lbl.update()

        path_to_db = self.compile_old_app()

        self.progressbar['value'] = 25
        self.progressbar.update()
        self.info_lbl.configure(text='Скачивание новой программы')
        logger.info(f'Клонирование репозитория {REPO_BRANCH}')
        self.info_lbl.update()

        new_app = os.path.join(path_app, REPO_BRANCH)

        try:
            response = requests.get(URL_REPO)

            with tempfile.TemporaryFile() as file:
                file.write(response.content)
                with zipfile.ZipFile(file) as fzip:
                    fzip.extractall(path_app)

        except ConnectionError as error:
            logger.error(
                f'Произошла ошибка при клонировании проекта {error}'
            )
            showerror(
                'Невозможно выполнить обновление',
                '\n\nМы не смогли выполнить обновление. '
                'Вы можете скачать новую версию самостоятельно через бота VK, '
                f'либо рассказать об ошибке в боте ВК\n\n{error}'
            )

            self.btn_start.configure(text='Закрыть', command=lambda: exit_ex())
            self.btn_start.update()

        self.progressbar['value'] = 50
        self.progressbar.update()
        self.info_lbl.configure(text='Подготовка файлов')
        self.info_lbl.update()

        self.compile_new_app(new_app)
        if path_to_db is not None:
            shutil.copy(path_to_db, os.path.join(path_app, 'settings'))

        self.progressbar['value'] = 100
        self.progressbar.update()
        self.info_lbl.configure(text='Готово!')
        self.info_lbl.update()

        showinfo(
            'Готово',
            'Обновлние закончено!\n\nВ случае ошибок, просто возьмите '
            'программу из папки "old_version"'
        )

    @staticmethod
    def get_version():
        path_version = os.path.join(path, REPO_VERSION_BRANCH)
        version = os.path.join(path_version, 'version.txt')

        try:
            logger.info('Клонируем ветку version')
            response = requests.get(URL_VERSION_REPO)

            with tempfile.TemporaryFile() as file:
                file.write(response.content)
                with zipfile.ZipFile(file) as fzip:
                    fzip.extractall(path)

        except ConnectionError as error:
            logger.error(
                f'Произошла ошибка при клонировании проекта {error}'
            )
            showerror(
                'Невозможно выполнить обновление',
                '\n\nМы не смогли выполнить обновление. '
                'Вы можете скачать новую версию '
                'самостоятельно, либо рассказать об ошибке в боте ВК'
            )

            exit_ex()

        logger.info('Удачно склонирован')

        with open(version, 'r', encoding='utf-8') as file:
            file = file.read().strip().split('&')

        shutil.rmtree(path_version, ignore_errors=True, onerror=None)

        return file[0]


if __name__ == '__main__':
    try:
        update = Updater()
    except SystemExit:
        pass
    except BaseException as error:
        logger.error(f'Непредвиденная ошибка {error}')
        showerror(
            'Невозможно выполнить обновление',
            '\n\nМы не смогли выполнить обновление. '
            'Вы можете скачать новую версию '
            f'самостоятельно, либо рассказать об ошибке в боте ВК\n\n{error}'
        )

        exit_ex()
