import os

VERSION = '0.4.23'  # TODO Не забыть изменить

UPDATE_WIN = 'updater.exe'
UPDATE_LINUX = 'updater.sh'

REPO_URL_VERSION = 'https://github.com/FlowHack/FlowParserVk/archive/refs/heads/control/version.zip'
REPO_URL_UPDATER = 'https://github.com/FlowHack/FlowParserVk/archive/refs/heads/control/updater.zip'
REPO_BRANCH_VERSION = 'FlowParserVk-control-version'
REPO_BRANCH_UPDATER = 'FlowParserVk-control-updater'
REPO_BRANCH_MASTER = 'FlowParserVk-master'

APP_NAME = 'FlowParserVK'
AUTHOR_PAGE = 'https://vk.com/id311966436'
APP_PAGE = 'https://github.com/FlowHack/FlowParserVk'
APP_COMMUNITY = 'https://vk.com/club203683544'
VK_BOT_APP = 'https://vk.com/im?media=&sel=-203683544'
ID_GROUP_VK = '-203683544'


path = os.getcwd()
path_to_version = os.path.join(path, REPO_BRANCH_VERSION)
path_to_updater = os.path.join(path, REPO_BRANCH_UPDATER)
path_to_dir_settings = os.path.join(path, 'settings')
path_to_dir_dicts = os.path.join(path_to_dir_settings, 'dicts')
path_to_dir_ico = os.path.join(path_to_dir_settings, 'ico')
__path_to_dir_style__ = os.path.join(path_to_dir_settings, 'style')
path_to_dir_style = os.path.join(__path_to_dir_style__, 'awthemes-10.2.0')
path_to_db = os.path.join(path_to_dir_settings, 'settings.db')

VERSION_API = '5.130'
REQUIRES_DATA = 'requires_data'
HTTP_FOR_REQUESTS = 'https://api.vk.com/method/{method}'
HTTP_GET_TOKEN = 'https://oauth.vk.com/authorize?client_id=7743684&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=327680&response_type=token&v=5.52'

DEFAULT_VALUE_FOR_BD = 'none_value'
TIME_FREE_VERSION = 7200

FORMAT_DATE = '%A  %x %H:%M'
NAME_PARSING = {
    'by_groups': 'По группам',
    'by_criteria': 'По критериям'
}
