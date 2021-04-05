from math import ceil
from time import time as time_now
from tkinter.messagebox import showwarning

from _tkinter import TclError

from settings import (ERROR_MSG, FOLLOWERS_MAX, FRIENDS_MAX, LIST_COUNTRIES,
                      STATUS_VK_PERSON)


class AdditionalFunctionsForWindows:
    @staticmethod
    def get_groups_from_text(texts):
        need_var = ['https://vk.com/', 'https://vk.com', '/vk.com/', 'vk.com/']
        ids = []
        for item in texts.split():
            if item is not None:
                if (item[:15] in need_var) or (item[:14] in need_var) or \
                        (item[:8] in need_var) or (item[:7] in need_var):
                    group_id = item.split('vk.com/')[1]
                    if group_id[:6] == 'public':
                        group_id = group_id[6:]

                    ids.append(group_id)
                else:
                    raise ValueError('неверный id')

        ids = set(ids)
        count = len(ids)

        return {'ids': ids, 'count': count}

    @staticmethod
    def get_values_for_parse_by_groups(widgets):
        need_country, need_region_city = widgets[''], widgets['']
