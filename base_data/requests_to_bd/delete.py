from settings import LOGGER

from ..base_data import MainDB

LOGGER = LOGGER('delete_request', 'base_data')


class DeleteRequestsToDB(MainDB):
    """
    Класс отвечающий за DELETE запросы к базы данных
    """

    def __init__(self):
        super().__init__()

    def delete_all_records(self, name_table: str) -> None:
        """
        Функция удаления всех записей в таблице
        :param name_table: имя очищаемой таблицы
        :return: None
        """
        LOGGER.warning(f'Начинаю удаление таблицы {name_table}')
        self.remote_control_bd.execute(f'DROP TABLE IF EXISTS {name_table}')
        self.connect_bd.commit()

        MainDB()
        LOGGER.info('Успешно удалена')

    def delete_record_in_bd(self, tb_name: str, where: str) -> None:
        """
        Функция удаления записи из таблицы
        :param tb_name: имя таблицы из которой удаляется запись
        :param where: параметры по которым искать нужную запись
        :return:
        """
        LOGGER.warning(
            f'Начинаю удаление записи where={where}, таблица GetRequestsApi'
        )
        self.remote_control_bd.execute(f'DELETE FROM {tb_name} WHERE {where}')
        self.connect_bd.commit()

        LOGGER.info('Успешно удалена')
