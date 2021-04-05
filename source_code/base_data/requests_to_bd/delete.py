from settings import LOGGER

from ..base_data import MainDB


class DeleteRequestsToDB(MainDB):
    def delete_all_records(self, name_table):
        LOGGER.warning(f'Начинаю удаление таблицы {name_table}')
        self.remote_control_bd.execute(f'DROP TABLE IF EXISTS {name_table}')
        self.connect_bd.commit()
        LOGGER.info('Успешно удалена')

    def delete_record_in_people_request_bd(self, pk):
        LOGGER.warning(f'Начинаю удаление записи pk:{pk}, таблица GetRequestsApi')
        self.remote_control_bd.execute(f'DELETE FROM GetRequestsApi WHERE pk={pk}')
        self.connect_bd.commit()
        LOGGER.info('Успешно удалена')
