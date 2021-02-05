from FlowParserVK import BrainForApp
from tkinter import ttk
from tkinter import Tk, messagebox
import scripts.main.styles as styles

one_value = None
two_value = None


class App(BrainForApp):
    pass


class AdditionalWindows(App):
    def license_and_agreement_data(self):
        pass


class DialogWindows:

    @staticmethod
    def get_two_params(
            title, text_field_one, text_field_two, header='Заполните поля'):
        """
        Функция создания диалогового окна с двумя полями для ввода данных
        :param title: Заголовок окна
        :param text_field_one: Label к первому полю
        :param text_field_two: Label ко второму полю
        :param header: Необязательно поле. Label-заголовок
        :return: информацию из двух полей в виде списка
        """
        global one_value, two_value

        def press_ok_btn(parent, one_entry, two_entry):
            global one_value, two_value
            styles.style_for_warning_entry()

            one_value = one_entry.get()
            two_value = two_entry.get()

            if (one_value == '') or (two_value == ''):
                one_entry.configure(style='Warning.TEntry', foreground='black')
                two_entry.configure(style='Warning.TEntry', foreground='black')
                parent.update()
            else:
                parent.destroy()

                return one_value, two_value

        def press_close_btn(parent):
            parent.destroy()

        get_window = Tk()
        styles.style_for_ok_and_close_btn(get_window)
        get_window.title(title)
        w = 450
        h = 150
        sw = get_window.winfo_screenwidth()
        sh = get_window.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        get_window.geometry('%dx%d+%d+%d' % (w, h, x, y))

        top_frame = ttk.Frame(
            get_window, padding=5, borderwidth=2, relief='groove'
        )
        top_frame.pack(side='top', fill='x')
        ttk.Label(
            top_frame,
            text=header,
            justify='center',
            font=('Times New Roman', 15, 'italic bold')
        ).pack(side='top')

        bottom_frame = ttk.Frame(get_window, padding=10)
        bottom_frame.pack(side='top', fill='both', expand=True)
        ttk.Label(bottom_frame, text=text_field_one).grid(
            row=0, column=0, sticky='NW', pady=5, padx=2
        )
        ttk.Label(bottom_frame, text=text_field_two).grid(
            row=1, column=0, sticky='NW', pady=5, padx=2
        )
        entry_one = ttk.Entry(
            bottom_frame, font=('Times New Roman', 10, 'italic bold')
        )
        entry_one.grid(row=0, column=1, sticky='WE', columnspan=2)
        entry_two = ttk.Entry(
            bottom_frame, font=('Times New Roman', 10, 'italic bold')
        )
        entry_two.grid(row=1, column=1, sticky='WE', columnspan=2)
        btn_ok = ttk.Button(
            bottom_frame, text='OK', style='OK.TButton',
            command=lambda: press_ok_btn(get_window, entry_one, entry_two)
        )
        btn_ok.grid(row=3, column=1, padx=5, sticky='WE', pady=5)
        btn_close = ttk.Button(
            bottom_frame, text='Отмена', style='Close.TButton',
            cursor='X_cursor', command=lambda: press_close_btn(get_window)
        )
        btn_close.grid(row=3, column=2, sticky='WE')

        bottom_frame.columnconfigure(1, weight=1)
        bottom_frame.columnconfigure(2, weight=1)

        get_window.bind(
            '<Return>', lambda event: press_ok_btn(
                get_window, entry_one, entry_two
            )
        )
        get_window.bind(
            '<Escape>', lambda event: press_close_btn(get_window)
        )

        get_window.mainloop()

        return one_value, two_value

    @staticmethod
    def info_window(title, info_txt):
        messagebox.showinfo(title, info_txt)

    @staticmethod
    def warning_window(title, warning_txt):
        messagebox.showwarning(title, warning_txt)

    @staticmethod
    def error_window(title, error_txt):
        messagebox.showerror(title, error_txt)
