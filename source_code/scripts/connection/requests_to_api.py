from scripts.connection.authorization import Authorize
from settings.settings import get_logger
from settings.settings import SettingsFunction
from math import ceil

logger = get_logger('requests_to_api')


class RequestsAPI(Authorize):
    def __init__(self):
        authorize = Authorize()
        self.vk_session = authorize.vk_session
        self.api = self.vk_session.get_api()
        self.v_api = SettingsFunction.VERSION_API

    def get_all_regions_in_country(self, country_id: int, progressbar):
        count = 1000
        offset = 0
        result = {}
        request = self.api.database.getRegions(
            v=self.v_api, country_id=country_id, count=count, offset=offset
        )

        count_return = int(request.get('count'))
        if count_return > count:
            need_iteration = ceil(count_return / count)
            step_progressbar = \
                SettingsFunction.PROGRESSBAR_MAXIMUM / need_iteration
            iteration = 0
            result_json = request.get('items')
            while iteration < need_iteration:
                progressbar['value'] += step_progressbar
                progressbar.update()
                offset += 1000
                request = self.api.database.getRegions(
                    v=self.v_api, country_id=country_id, count=count,
                    offset=offset
                )
                result_json += request.get('items')
                iteration += 1
        else:
            result_json = request.get('items')

        progressbar['value'] = 0
        for item in result_json:
            result[item['title']] = item['id']

        return result

    def get_all_city_in_country(self, country_id: int, progressbar):
        count = 1000
        offset = 0
        result = {}
        request = self.api.database.getCities(
            v=self.v_api, country_id=country_id, need_all=1, count=count,
            offset=offset
        )
        count_return = int(request.get('count'))
        if count_return > count:
            need_iteration = ceil(count_return / count)
            step_progressbar = \
                SettingsFunction.PROGRESSBAR_MAXIMUM / need_iteration
            iteration = 0
            result_json = request.get('items')
            while iteration < need_iteration:
                progressbar['value'] += step_progressbar
                progressbar.update()
                offset += 1000
                request = self.api.database.getCities(
                    v=self.v_api, country_id=country_id, need_all=1,
                    count=count,
                    offset=offset
                )
                result_json += request.get('items')
                iteration += 1
        else:
            result_json = request.get('items')

        progressbar['value'] = 0
        for item in result_json:
            result[item['title']] = item['id']

        return result
