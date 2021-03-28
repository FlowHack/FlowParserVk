from webbrowser import open as web_open

import vk_api
from base_data import GetRequestsToDB, UpdateRequestsToDB
from requests import exceptions as requests_except
from settings import ERROR_MSG, get_logger

logger = get_logger('authorization')


class ConnectionToVk(GetRequestsToDB, UpdateRequestsToDB):
    def __init__(self):
        super().__init__()
        vk_login, vk_password = self.get_login_and_password_vk()
        vk_session = self.get_vk_session(vk_login, vk_password)

        if vk_session is not None:
            self.session = vk_session
            self.api = vk_session.get_api()
            # from windows import DialogWindows
            # DialogWindows.info_window(
            #     'Авторизовн!', 'Вы удачно авторизовались!'
            # )
        else:
            self.session = None
            self.api = None

    def get_login_and_password_vk(self):
        user_data_table_value = \
            self.get_user_data_table_value()
        vk_login = user_data_table_value['vk_login']
        vk_password = user_data_table_value['vk_password']

        return vk_login, vk_password

    def get_vk_session(self, elementary_vk_login, elementary_vk_password):
        """
        Функция получения объекта сесси VK
        :param elementary_vk_login: логин из базы
        :param elementary_vk_password: пароль из базы
        :return: объект сессии VK
        """

        if (elementary_vk_login == 'none_value') or \
                (elementary_vk_password == 'none_value'):
            vk_login, vk_password = self.get_data_for_authorization()
        else:
            vk_login, vk_password = elementary_vk_login, elementary_vk_password

        try:
            vk_session = vk_api.VkApi(
                login=vk_login,
                password=vk_password,
                auth_handler=self.auth_handler,
                captcha_handler=self.captcha_handler,
                app_id=7743684,
                scope=65536
            )
            vk_session.auth()

        except vk_api.exceptions.BadPassword:
            vk_login, vk_password = self.get_data_for_authorization(
                header='Неправильный логин или пароль!'
            )
            self.get_vk_session(vk_login, vk_password)

        except vk_api.exceptions.LoginRequired:
            from windows import DialogWindows
            DialogWindows.warning_window(
                title='Вы не авторизовались',
                warning_txt=ERROR_MSG['Authorization']['not_authorization']
            )

            return None

        except requests_except.ConnectionError as error:
            from windows import DialogWindows
            logger.warning(f'Отсутствует подключение! {error}')
            DialogWindows.warning_window(
                title='Нет сети',
                warning_txt=ERROR_MSG['Authorization']['not_authorization']
            )

        except BaseException as error:
            from windows import DialogWindows
            logger.error(f'Неизвестная ошибка! {error}')
            DialogWindows.error_window(
                title='Непредвиденная ошибка',
                error_txt=ERROR_MSG['Unforeseen_error'].format(error)
            )

            return None
        else:
            if (elementary_vk_login != vk_login) or \
                    (elementary_vk_password != vk_password):
                self.update_data_on_user_table(
                    new_vk_login=vk_login, new_vk_password=vk_password
                )

            return vk_session

    @staticmethod
    def auth_handler():
        """
        Связующий между человеком и двухфакторной авторизацией
        :return: код, булево (сохранять ли устройство)
        """
        from windows import DialogWindows
        key = DialogWindows.get_one_or_two_params(
            title='Двухфакторная аутентификация', text_field_one='Код',
            header='Введите код из смс/vk'
        )
        remember_device = True

        return key, remember_device

    @staticmethod
    def captcha_handler(captcha):
        """
        Связующий между человеком и каптчей
        :param captcha: объект капчи
        :return: результат прохождения
        """
        from windows import DialogWindows
        web_open(captcha.get_url())
        key = DialogWindows.get_one_or_two_params(
            title='Капча', text_field_one='Капча',
            header='Пройдите капчу из браузера.'
        )

        return captcha.try_again(key)

    @staticmethod
    def get_data_for_authorization(
            header='Введите ваши данные от аккаунта VK'):
        """
        Получение логина и пароля от аккаунта Вконтакте
        :param header: Заголовок инпут окна.
        :return: Возваращает результат получения данных
        """
        from windows import DialogWindows
        response = DialogWindows().get_one_or_two_params(
            title='Введите ваши данные от аккаунта Vk', text_field_one='Логин',
            text_field_two='Пароль', header=header, count_field=2
        )

        return response
