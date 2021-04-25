import os
import shutil
from logging import INFO, Formatter, getLogger
from logging.handlers import RotatingFileHandler
from sys import exit as exit_ex
from tempfile import TemporaryDirectory
from tkinter import Tk, ttk
from tkinter.messagebox import showerror
from tkinter.ttk import Style

from git import Repo
from git.exc import GitCommandError
from PIL import ImageTk

path = os.getcwd()
os.chdir('..')
path_app = os.getcwd()

VERSION_UPDATER = '0.1.0'
URL_REPO = 'https://github.com/FlowHack/FlowParserVk.git'
OS_NAME = os.name

if OS_NAME == 'posix':
    REPO_BRANCH = 'app/posix'
    OS = 'Linux система'
elif OS_NAME == 'nt':
    REPO_BRANCH = 'app/windows'
    OS = 'Windows'
else:
    REPO_BRANCH = 'app/posix'
    OS = 'Неподдерживаемая система'

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


def set_global_style():
    default_style = 'alt'

    style = Style()
    style.theme_use(default_style)


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

    def compile_old_app(self):
        os.chdir(path_app)

        if os.path.exists('old_version'):
            shutil.rmtree('old_version', ignore_errors=True, onerror=None)

        listdir = os.listdir(path_app)

        os.mkdir('old_version')
        path_old = os.path.join(path_app, 'old_version')
        path_to_bd = os.path.join(path_old, 'settings', 'settings.bd')

        for item in listdir:
            if item == 'updater':
                continue

            shutil.move(os.path.join(path_app, item), path_old)

        return path_to_bd

    def updater(self):
        self.info_lbl.configure(text='Подготовка файлов')
        self.progressbar['value'] = 25
        path_to_bd = self.compile_old_app()
        self.progressbar['value'] = 50
        self.info_lbl.configure(text='Скачивание новой программы')
        self.progressbar['value'] = 75
        new_app = os.path.join(path_app, 'new')
        os.mkdir(new_app)

        try:
            logger.info('Клонирую репозиторий windows')
            Repo.clone_from(URL_REPO, new_app, branch=REPO_BRANCH, depth=1)
        except GitCommandError as error:
            logger.error(
                f'Произошла ошибка при клонировании проекта {error}'
            )
            showerror(
                'Невозможно выполнить обновление',
                '\n\nМы не смогли выполнить обновление. '
                'Вы можете скачать новую версию самостоятельно через бота VK, '
                'либо рассказать об ошибке в боте ВК'
            )

            return

    @staticmethod
    def get_version():
        with TemporaryDirectory() as temp:
            version = temp + '/' + 'version.txt'

            try:
                logger.info('Клонируем проект')
                Repo.clone_from(
                    URL_REPO, temp, branch='control/version', depth=1
                )
                logger.info('Удачно склонирован')
            except GitCommandError as error:
                logger.error(
                    f'Произошла ошибка при клонировании проекта {error}'
                )
                showerror(
                    'Невозможно выполнить обновление',
                    '\n\nМы не смогли выполнить обновление. '
                    'Вы можете скачать новую версию '
                    'самостоятельно, либо рассказать об ошибке в боте ВК'
                )

                return

            with open(version, encoding='utf-8') as file:
                file = file.readline().strip().split('&')

            return file[0]


if __name__ == '__main__':
    update = Updater()
