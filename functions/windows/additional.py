from typing import Dict, List, Union

from my_vk_api import GetRequestsToVkApi


class AdditionalFunctionsForWindows:
    """
    Класс отвечающий за дополнительные функции для главного окна
    """

    def __init__(self):
        self.cities: Dict[str, Union[int, dict]] = {
            'country_id': None,
            'cities': {}
        }
        self.regions: Dict[str, Union[int, dict]] = {
            'country_id': None,
            'regions': {}
        }

    def get_cities(self, country_id: int) -> Dict[str, Union[int, dict]]:
        """
        Получение городов в стране
        :param country_id: id Страны
        :return: Dict
        """
        if self.cities['country_id'] is not None:
            if country_id == self.cities['country_id']:
                return self.cities['cities']

        params = {
            'country_id': country_id,
            'need_all': 1
        }

        cities = GetRequestsToVkApi().get_all_object(
            'database.getCities', **params
        )

        for item in cities['items']:
            self.cities['cities'][item['title']] = int(item['id'])

        self.cities['country_id'] = country_id

        return self.cities['cities']

    def get_regions(self, country_id: int) -> Dict[str, Union[int, dict]]:
        """
        Получение регионов в стране
        :param country_id: id Страны
        :return: Dict
        """
        if self.regions['country_id'] is not None:
            if country_id == self.cities['country_id']:
                return self.regions['regions']

        params = {
            'country_id': country_id,
        }

        cities = GetRequestsToVkApi().get_all_object(
            'database.getRegions', **params
        )

        for item in cities['items']:
            self.regions['regions'][item['title']] = int(item['id'])

        self.regions['country_id'] = country_id

        return self.regions['regions']

    @staticmethod
    def get_groups_from_text(texts: str) -> Dict[
        str, Union[int, List[Union[int, str]]]
    ]:
        """
        Функция обработки ссылок на группы и превращения их в id
        :param texts: текст с ссылками через Enter
        :return:
        """
        need_var = ['https://vk.com/', 'https://vk.com', '/vk.com/', 'vk.com/']
        ids = []
        for item in texts.split():
            if item is not None:
                if item[-1] == '/':
                    del (item[-1])
                if (item[:15] in need_var) or (item[:14] in need_var) or \
                        (item[:8] in need_var) or (item[:7] in need_var):
                    group_id = item.split('vk.com/')[1]
                    if group_id[:6] == 'public':
                        group_id = group_id[6:]
                    elif group_id[:4] == 'club':
                        group_id = group_id[4:]

                    ids.append(group_id)
                else:
                    raise ValueError('неверный id')

        ids = list(set(ids))
        count = len(ids)

        return {'ids': ids, 'count': count}
