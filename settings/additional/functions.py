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


def copy_in_clipboard(widget, value):
    """
    Функция управляющая наполнением буфера обмена
    :param widget: виджет от лица которого будет происходить копирование
    :param value: строковое значение, которое надо скопировать
    :return: ничего
    """
    widget.clipboard_clear()
    widget.clipboard_append(value)
