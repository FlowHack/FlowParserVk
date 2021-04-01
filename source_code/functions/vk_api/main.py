from vk_api import GetRequestsToVkApi


class MainFunctionsForParsing:
    @staticmethod
    def get_objects(do: int, progressbar=None, **kwargs):
        get_requests_to_vk_api = GetRequestsToVkApi()

        if do == 1:
            api_method = 'database.getCities'
            action_arguments = {
                'need_all': 1,
                'country_id': kwargs['country_id']
            }
        elif do == 2:
            api_method = 'database.getRegions'
            action_arguments = {
                'country_id': kwargs['country_id']
            }
        elif do == 3:
            api_method = 'database.getCities'
            action_arguments = {
                'country_id': kwargs['country_id'],
                'region_id': kwargs['region_id'],
                'need_all': 1
            }
        else:
            raise ValueError('неверный do')

        try:
            response = get_requests_to_vk_api.get_all_object(
                api_method=api_method,
                progressbar=progressbar,
                **action_arguments
            )
        except ValueError as error:
            if str(error) == 'неверный токен':
                return None
            else:
                return None

        return response

    @staticmethod
    def sort_group_id(ids):
        group_id = GetRequestsToVkApi().get_group_id(ids)
        group_id = group_id[0].get('id')

        return group_id
