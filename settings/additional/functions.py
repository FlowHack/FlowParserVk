from typing import Union

import clipboard


def set_position_window_on_center(parent, width: int, height: int) -> None:
    """
    Функция установки окна по середине окна
    :param parent: объект окна, которое нужно расположить посередине
    :param width: параметр длины окна
    :param height: параметр высоты окна
    :return:
    """
    sw = parent.winfo_screenwidth()
    sh = parent.winfo_screenheight()
    x = (sw - width) / 2
    y = (sh - height) / 2
    parent.geometry('%dx%d+%d+%d' % (width, height, x, y))


def copy_in_clipboard(widget: object, value: Union[int, str]) -> None:
    """
    Функция управляющая наполнением буфера обмена
    :param widget: виджет от лица которого будет происходить копирование
    :param value: строковое значение, которое надо скопировать
    :return:
    """
    widget.clipboard_clear()
    widget.clipboard_append(value)


def paste_into_widget(widget: object, text=False) -> None:
    """
    Функция управляющая наполнением из буфера обмена
    :param widget: виджет в который вставить объект
    :param text: Текстовое ли поле
    :return:
    """
    txt = clipboard.paste()

    if text is True:
        widget.insert(1.0, txt)
        return

    widget.insert(0, txt)


def configure_progress_lbl(pg: object = None,
                           lbl: object = None,
                           pg_val: int = 0, lbl_text: str = '',
                           lbl_color: str = 'white',
                           lbl_back: str = None) -> None:
    """
    Функция отвечает за конфигурацию прогрессбара и Label с информацией
    :param pg: Progressbar
    :param lbl: Label
    :param pg_val: значение progressbar
    :param lbl_text: значение Label
    :param lbl_color: цвет текста Label
    :param lbl_back: цвет фона Label
    :return:
    """
    if pg is not None:
        pg['value'] = pg_val
        pg.update()

    if lbl is not None:
        lbl.configure(text=lbl_text)
        lbl.configure(foreground=lbl_color)
        if lbl_back is not None:
            lbl.configure(background=lbl_back)
        lbl.update()


def time_now() -> float:
    from time import localtime, mktime
    local_time = localtime()
    time = mktime(local_time)

    return time
