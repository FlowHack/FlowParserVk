from os import getcwd

VERSION = '0.1.0'
APP_NAME = 'FlowParserVK'
AUTHOR_PAGE = 'https://vk.com/id311966436'
APP_PAGE = ''
APP_BOT = ''
APP_COMMUNITY = ''
PAGE_APP = ''
TELEGRAM_BOT_APP = ''
VK_BOT_APP = ''
ID_GROUP_VK = '-203683544'
BANK_DETAILS = {
    'sberbank': '5469560018109591',
    'ymoney': '410017514569348',
    'qiwi_visa': '4890494702214891'
}

path = getcwd()
path_to_dir_settings = f'{path}/settings'
path_to_dir_dicts = f'{path_to_dir_settings}/dicts'
path_to_dir_ico = f'{path_to_dir_settings}/ico'
path_to_dir_style = f'{path_to_dir_settings}/style/awthemes-10.2.0'
path_to_db = f'{path_to_dir_settings}/settings.db'

VERSION_API = '5.130'
HTTP_FOR_REQUESTS = 'https://api.vk.com/method/{method}'
HTTP_GET_TOKEN = 'https://oauth.vk.com/authorize?client_id=7743684&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=327680&response_type=token&v=5.52'

DEFAULT_VALUE_FOR_BD = 'non_value'
TIME_FREE_VERSION = 7200

FORMAT_DATE = '%A  %x %H:%M'
NAME_PARSING = {
    'by_groups': 'По группам',
    'by_criteria': 'По критериям'
}
URL_REPO = 'https://github.com/FlowHack/FlowParserVk.git'
