from tkinter.ttk import Style
from _tkinter import TclError
from settings.settings import SettingsFunction

PATH_TO_STYLE = SettingsFunction.path_to_dir_style
BACKGROUND = '#33393B'
BUTTON_BACKGROUND = '#6D6D6D'
DEFAULT_STYLE = 'awdark'


def set_global_style(parent):
    default_style = DEFAULT_STYLE

    try:
        parent.tk.call('lappend', 'auto_path', f'{PATH_TO_STYLE}')
        parent.tk.call('package', 'require', DEFAULT_STYLE)
    except TclError as error:
        if str(error) == 'can\'t find package awdark':
            default_style = 'alt'

    return default_style


def style_for_ok_and_close_btn(parent):
    default_style = set_global_style(parent)
    style = Style()
    style.theme_use(default_style)
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


def style_for_warning_entry():
    style = Style()
    style.element_create('plain.field', 'from', 'clam')
    style.layout('Warning.TEntry',
                 [('Entry.plain.field', {'children': [(
                     'Entry.background', {'children': [(
                         'Entry.padding', {'children': [(
                             'Entry.textarea', {'sticky': 'nswe'})],
                             'sticky': 'nswe'})], 'sticky': 'nswe'})],
                     'border': '2', 'sticky': 'nswe'})])
    style.configure('Warning.TEntry', fieldbackground='#FFA3AD')
