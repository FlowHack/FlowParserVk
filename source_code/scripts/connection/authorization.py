from settings.settings import SettingsFunction
from scripts.scripts.base_data import RequestToBD
import vk_api

logger = SettingsFunction.get_logger('authorization')


class Authorize:
    def __init__(self, preview_window):
        self.preview_window = preview_window
        base_data_requests = RequestToBD()
        user_data_table_value = base_data_requests.get_user_data_table_value()
        self.vk_login = user_data_table_value['vk_login']
        self.vk_password = user_data_table_value['vk_password']
        self.get_vk_session(self.vk_login, self.vk_password)

    def get_vk_session(self, vk_login, vk_password):
        if (vk_login is None) or (vk_password is None):
            self.preview_window.destroy()
            vk_login, vk_password = self.get_data_for_authorization()

        vk_session = vk_api.VkApi(
            login=vk_login,
            password=vk_password,
            auth_handler=self.auth_handler,
            captcha_handler=self.captcha_handler,
            scope=2
        )

        try:
            vk_session.auth()
        except vk_api.exceptions.BadPassword as error:
            if str(error) == 'Bad password':
                self.get_data_for_authorization(
                    header='Неправильный логин или пароль!'
                )
            else:
                print(error)

    def auth_handler(self):
        pass

    def captcha_handler(self, captcha):
        pass

    def get_data_for_authorization(
            self, header='Введите ваши данные от аккаунта VK'):
        from scripts.main.app import DialogWindows
        response = DialogWindows.get_two_params(
            title='Введите ваши данные от аккаунта Vk',
            text_field_one='Логин',
            text_field_two='Пароль',
            header=header
        )

        return response
