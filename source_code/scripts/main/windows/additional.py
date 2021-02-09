from tkinter import Tk, ttk, messagebox, Text
from time import time
import scripts.main.styles as styles
from sys import exit as exit_ex
from scripts.main.windows.master import set_position_window_on_center
from settings.settings import SettingsFunction

lose_agreement_count: int = 0
logger = SettingsFunction.get_logger('additional_windows')


class AdditionalWindows:

    @staticmethod
    def person_and_agreement_data(window_preview):
        """
        Функция создания окна пользовательского соглашения
        :param window_preview: объект превью программы
        :return: Ничего
        """
        global lose_agreement_count
        from settings.settings import LICENSE_AGREEMENT

        def lose_agreement(start):
            """
            Функция шуточной обработки неправильного нажатия на кнопку
            подтверждения
            :param start: время запуска функции person_and_agreement_data
            :return: ничего
            """
            global lose_agreement_count
            if lose_agreement_count == 0:
                messagebox.showinfo(
                    'Прочтите пользовательское соглашение!',
                    'Вы не прочитали соглашение!'
                )
                lose_agreement_count = 1
            elif lose_agreement_count == 1:
                messagebox.showinfo(
                    'Прочтите пользовательское соглашение!',
                    'Вы не собираетесь читать пользовательское '
                    'соглашение?!\n\nЯ всё же настаиваю на его прочтении! '
                )
                lose_agreement_count = 2
            elif lose_agreement_count == 2:
                now_time = time() - start
                messagebox.showwarning(
                    'Прочтите пользовательское соглашение!',
                    f'Я придумал! Буду считать сколько времени вы тратите '
                    f'впустую.\nНа данный момент вы потратили '
                    f'{now_time:.0f}сек.\n\nПрочитайте пользовательское '
                    f'соглашение! '
                )
                lose_agreement_count = 3
            else:
                now_time = time() - start
                messagebox.showwarning(
                    'Прочтите пользовательское соглашение!',
                    f'На данный момент вы потратили {now_time:.0f}сек.\n\nНе '
                    f'тратьте своё время просто так. Прочитайте '
                    f'пользовательское соглашение! '
                )

        start_function_time = time()
        window_preview.destroy()
        agreement_window = Tk()
        styles.set_global_style(agreement_window)
        styles.style_for_ok_and_close_btn()
        styles.style_for_warning_entry()
        agreement_window.title('Пользовательское соглашение!')
        w = 600
        h = 300
        set_position_window_on_center(agreement_window, width=w, height=h)
        agreement_window.protocol("WM_DELETE_WINDOW", exit_ex)

        main_frame = ttk.Frame(agreement_window, padding=10)
        main_frame.pack(side='top', fill='both', expand=True)

        text = Text(main_frame, wrap='word', width=71, height=14)
        text.insert(1.0, LICENSE_AGREEMENT)
        text.grid(row=0, column=0, sticky='NSEW', columnspan=2)

        btn_agreement = ttk.Button(main_frame, text='Принять')
        btn_agreement.grid(row=1, column=0, sticky='EW', pady=5)
        ttk.Button(
            main_frame, text='Отмена', command=exit_ex
        ).grid(row=1, column=1, sticky='EW')

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        btn_agreement.bind(
            '<Button-3>', lambda event: agreement_window.destroy()
        )
        btn_agreement.bind(
            '<Button-1>', lambda event: lose_agreement(start_function_time)
        )

        agreement_window.mainloop()
