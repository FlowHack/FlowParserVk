from tkinter.ttk import Style

from _tkinter import TclError

from settings.additional.variables import path_to_dir_style

BACKGROUND = '#33393B'
BACKGROUND_TEXT = '#33393B'
FOREGROUND_TEXT = '#c8c8c8'
BUTTON_BACKGROUND = '#6D6D6D'
DEFAULT_STYLE = 'awdark'
NOTABLE_LABEL_FONT = '#00c7ff'


def set_global_style(parent: object) -> None:
    """
    Функция утановки стиля для окна
    :param parent: объект окна
    :return:
    """
    default_style = DEFAULT_STYLE

    try:
        parent.tk.call('lappend', 'auto_path', f'{path_to_dir_style}')
        parent.tk.call('package', 'require', DEFAULT_STYLE)
    except TclError as error:
        if str(error) == 'can\'t find package awdark':
            default_style = 'alt'

    style = Style()
    style.theme_use(default_style)


def style_for_ok_and_close_btn() -> None:
    """
    Функция создания стилей для кнопок Ок и Отмена
    :return:
    """
    style = Style()
    style.map("OK.TButton",
              foreground=[
                  ('pressed', 'white'), ('active', 'green')
              ],
              background=[
                  ('pressed', '#5CFF5D'),
                  ('active', '#A5FF99'),
                  ('!disabled', BUTTON_BACKGROUND)
              ],
              )
    style.map(
        'Close.TButton',
        foreground=[('pressed', 'black'), ('active', '#B20007')],
        background=[('pressed', '#B20007'), ('active', '#FFA3B5')]
    )


def style_for_warning_entry() -> None:
    """
    Функция создания стиля для пустого Entry
    :return:
    """
    style = Style()
    try:
        style.element_create('plain.field', 'from', 'clam')
    except TclError as error:
        if str(error) == 'Duplicate element plain.field':
            pass
    style.layout('Warning.TEntry',
                 [('Entry.plain.field', {'children': [(
                     'Entry.background', {'children': [(
                         'Entry.padding', {'children': [(
                             'Entry.textarea', {'sticky': 'nswe'})],
                             'sticky': 'nswe'})], 'sticky': 'nswe'})],
                     'border': '2', 'sticky': 'nswe'})])
    style.configure('Warning.TEntry', fieldbackground='#FFA3AD')
