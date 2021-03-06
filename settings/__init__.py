from .additional.functions import *
from .additional.value_constraints import *
from .additional.variables import *
from .dicts.additional_dicts import *
from .settings import *
from .style import fonts, styles

__all__ = [
    #  additional_functions
    'set_position_window_on_center',
    'copy_in_clipboard',
    'time_now',
    'configure_progress_lbl',
    'paste_into_widget',
    #  additional_value_constraints
    'FOLLOWERS_MAX',
    'FRIENDS_MAX',
    'OLD_YEAR_MAX',
    'OLD_YEAR_MIN',
    'PROGRESSBAR_MAX',
    'MACH_PHOTO_MIN',
    'MACH_PHOTO_MAX',
    'LAST_SEEN_MAX',
    #  additional_variables
    'VERSION',
    'VERSION_API',
    'APP_NAME',
    'AUTHOR_PAGE',
    'VK_BOT_APP',
    'REQUIRES_DATA',
    'path',
    'path_to_dir_settings',
    'path_to_dir_dicts',
    'path_to_dir_ico',
    'path_to_dir_style',
    'path_to_db',
    'HTTP_GET_TOKEN',
    'HTTP_FOR_REQUESTS',
    'DEFAULT_VALUE_FOR_BD',
    'ID_GROUP_VK',
    'TIME_FREE_VERSION',
    'FORMAT_DATE',
    'NAME_PARSING',
    'APP_PAGE',
    'UPDATE_WIN',
    'UPDATE_LINUX',
    'APP_COMMUNITY',
    'REPO_BRANCH_VERSION',
    'REPO_URL_VERSION',
    'REPO_URL_UPDATER',
    'REPO_BRANCH_UPDATER',
    'path_to_updater',
    'path_to_version',
    'REPO_BRANCH_MASTER',
    #  additional_dicts
    'LIST_COUNTRIES',
    'ERROR_MSG',
    'WARNING_MSG',
    'INFO_MSG',
    'STATUS_VK_PERSON',
    'POLITICAL',
    'PEOPLE_MAIN',
    'LIFE_MAIN',
    'SMOKING',
    'ALCOHOL',
    'ASKS',
    #  settings
    'LABEL_DESCRIPTION',
    'LABEL_HELP_DESCRIPTION',
    'LICENSE_AGREEMENT',
    'LOGGER',
    'LABEL_PLEASE_HELP_BOT',
    #  style
    'fonts',
    'styles',
]
