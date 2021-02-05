import time
from tkinter import Label, Tk

from PIL import Image, ImageTk
from _tkinter import TclError

from settings.settings import SettingsFunction
from scripts.scripts.base_data import MainBD
from scripts.connection.authorization import Authorize

logger = SettingsFunction.get_logger('main')


class BrainForApp:

    def __init__(self, window_preview):
        """
        Создаёт превью и проверяет нужные настройки для программы
        :param window_preview: объект окна превью
        """
        png_preview_open, png_preview = self.preview_image_open()
        self.preview_image_set(png_preview_open, png_preview, window_preview)
        window_preview.update()

        MainBD()
        Authorize(window_preview)
        time.sleep(2)

        try:
            window_preview.destroy()
        except TclError as error:
            pass

    @staticmethod
    def check_ico():
        """
        Проверяет наличие иконок
        """
        pass

    def check_vk_data(self):
        """
        Проверяет наличие данных пользователя Вконтакте
        """
        pass

    def check_update(self):
        """
        Проверяет наличие обновлений
        """
        pass

    def preview_image_open(self):
        """
        Возвращает первью картинку
        """
        while True:
            try:
                png_preview_open = Image.open(
                    fr'{SettingsFunction.path_to_dir_ico}/preview.png'
                )
                png_preview = ImageTk.PhotoImage(png_preview_open)
                return png_preview_open, png_preview
            except FileNotFoundError as error:
                logger.error(str(error))
                self.check_ico()

    @staticmethod
    def preview_image_set(png_preview_open, png_preview, window_preview):
        """
        Устанавливает размеры окна, ставит его по середине, устанавливает
        картинку как фон
        """
        x_img, y_img = png_preview_open.size
        x = (window_preview.winfo_screenwidth() - x_img) // 2
        y = (window_preview.winfo_screenheight() - y_img) // 2
        window_preview.geometry("%ix%i+%i+%i" % (x_img, y_img, x, y))
        Label(window_preview, image=png_preview).pack()


if __name__ == '__main__':
    master = Tk()
    master.overrideredirect(True)

    app_brain = BrainForApp(master)
