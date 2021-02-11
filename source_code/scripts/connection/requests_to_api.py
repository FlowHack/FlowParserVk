from scripts.connection.authorization import Authorize
from settings.settings import get_logger


logger = get_logger('requests_to_api')


class RequestsAPI(Authorize):
    def __init__(self):
        super().__init__()

    def get_all_regions_in_country(self, country):
        pass
