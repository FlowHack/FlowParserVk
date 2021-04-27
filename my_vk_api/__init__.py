from FlowParserVk import ConfigureVkApi

from .requests.get import GetRequestsToVkApi
from .requests.vk_scripts import *

__all__ = [
    'ConfigureVkApi',
    'GetRequestsToVkApi',
    'PARSE_BY_GROUP_CODE',
    'EASY_PARSE_BY_GROUP_CODE'
]
