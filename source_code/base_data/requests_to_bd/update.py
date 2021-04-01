from base_data import GetRequestsToDB, MainDB
from settings import LOGGER


class UpdateRequestsToDB(MainDB):
    def update_data_on_user_table(self,
                                  access_token: str):
        self.remote_control_bd.execute(
            f'''
            UPDATE UserData
            SET access_token = "{access_token}"
            '''
        )
        self.connect_bd.commit()
        LOGGER.warning('Обновлены данные таблицы UserData')

    def update_settings_app_table(self,
                                  auto_update=None, person_agreement=None,
                                  start_free_version=None):
        if (auto_update is None) or (person_agreement is None) or \
                (start_free_version is None):
            values = GetRequestsToDB().get_settings_table_value(hide_result=False)
            last_auto_update = values['auto_update']
            last_person_agreement = values['first_start']
            last_start_free_version = values['start_free_version']

            auto_update = (last_auto_update, auto_update)[auto_update is not None]
            person_agreement = (last_person_agreement,
                                person_agreement)[person_agreement is not None]
            start_free_version = (last_start_free_version,
                                  start_free_version)[start_free_version is not None]

        self.remote_control_bd.execute(
            f'''
            UPDATE AppSettings
            SET auto_update = {auto_update},
            first_start = {person_agreement},
            start_free_version = {start_free_version}
            '''
        )
        self.connect_bd.commit()
        LOGGER.warning('Обновлены данные таблицы AppSettings')

    def update_get_people_bd(self, type_request, count_people, response, time):
        self.remote_control_bd.execute(
            f'''
            INSERT INTO GetRequestsApi (type_request,count_people,response,time_request) 
            VALUES("{type_request}",{count_people},"{response}",{time})
            '''
        )
        self.connect_bd.commit()
        LOGGER.warning('Добавлены данные в таблицу GetRequestsApi')
