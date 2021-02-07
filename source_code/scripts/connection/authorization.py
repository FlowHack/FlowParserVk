from settings.settings import SettingsFunction
from scripts.scripts.base_data import RequestToBD
from webbrowser import open as web_open
import vk_api

logger = SettingsFunction.get_logger('authorization')


class Authorize:
    def __init__(self, preview_window):
        self.preview_window = preview_window
        self.base_data_requests = RequestToBD()
        user_data_table_value = \
            self.base_data_requests.get_user_data_table_value()
        self.vk_login = user_data_table_value['vk_login']
        self.vk_password = user_data_table_value['vk_password']
        self.vk_session = self.get_vk_session(self.vk_login, self.vk_password)

    def get_vk_session(self, elementary_vk_login, elementary_vk_password):
        if (elementary_vk_login == 'none_value') or \
                (elementary_vk_password == 'none_value'):
            self.preview_window.destroy()
            vk_login, vk_password = self.get_data_for_authorization()
        else:
            vk_login, vk_password = elementary_vk_login, elementary_vk_password

        try:
            vk_session = vk_api.VkApi(
                login=vk_login,
                password=vk_password,
                auth_handler=self.auth_handler,
                captcha_handler=self.captcha_handler,
                scope=2
            )
            vk_session.auth()

        except vk_api.exceptions.BadPassword:
            vk_login, vk_password = self.get_data_for_authorization(
                header='Неправильный логин или пароль!'
            )
            self.get_vk_session(vk_login, vk_password)

        except vk_api.exceptions.LoginRequired:
            from scripts.main.app import DialogWindows
            DialogWindows.warning_window(
                title='Вы не авторизовались',
                warning_txt='Вы не авторизовались!\n\nВы можете '
                            'продолжить использование программы, '
                            'но делать запросы к VK вы не сможете.\n\nВы '
                            'в любой момент можете авторизоваться на '
                            'главной странице! '
            )

            return None

        except BaseException as error:
            logger.error(f'Неизвестная ошибка! {error}')

        if (elementary_vk_login != vk_login) or \
                (elementary_vk_password != vk_password):
            self.base_data_requests.update_data_on_user_table(
                new_vk_login=vk_login, new_vk_password=vk_password
            )

        return vk_session

    @staticmethod
    def auth_handler():
        from scripts.main.app import DialogWindows
        key = DialogWindows.get_one_or_two_params(
            title='Двухфакторная аутентификация', text_field_one='Код',
            header='Введите код из смс/vk'
        )
        remember_device = True

        return key, remember_device

    @staticmethod
    def captcha_handler(captcha):
        from scripts.main.app import DialogWindows
        web_open(captcha.get_url())
        key = DialogWindows.get_one_or_two_params(
            title='Капча', text_field_one='Капча',
            header='Пройдите капчу из браузера.'
        )

        return captcha.try_again(key)

    @staticmethod
    def get_data_for_authorization(
            header='Введите ваши данные от аккаунта VK'):
        from scripts.main.app import DialogWindows
        response = DialogWindows.get_one_or_two_params(
            title='Введите ваши данные от аккаунта Vk', text_field_one='Логин',
            text_field_two='Пароль', header=header, count_field=2
        )

        return response
