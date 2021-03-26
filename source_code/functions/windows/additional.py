from _tkinter import TclError
from settings import (ERROR_MSG, LIST_COUNTRIES, STATUS_VK_PERSON,
                      value_constraints)

from windows import DialogWindows

from ..vk_api import FunctionsForAPI
from .for_windows import FunctionsForWindows


class AdditionalFunctionsForWindows(FunctionsForAPI):
    def __init__(self):
        super().__init__()
