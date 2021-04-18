from math import ceil
from time import time as time_now
from tkinter.messagebox import showinfo, showwarning
from webbrowser import open_new_tab as web_open_new_tab

import requests
import vk_api

from base_data import GetRequestsToDB, UpdateRequestsToDB
from settings import (DEFAULT_VALUE_FOR_BD, HTTP_FOR_REQUESTS, HTTP_GET_TOKEN,
                      ID_GROUP_VK, INFO_MSG, LOGGER, TIME_FREE_VERSION,
                      VERSION_API, WARNING_MSG)
from windows import AdditionalWindows



