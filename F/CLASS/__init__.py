import F
from F import DICT, LIST
import os
from F.LOG import Log
from .Queue import FairQueue
from .Callback import FairCallbackChannel
Log = Log("FClass.FairClass")


GLOBAL_CALLBACK_MESSAGE_TEMPLATE = lambda msg: f"Global-Callback: {msg}"
GLOBAL_CALLBACK_MESSAGE = GLOBAL_CALLBACK_MESSAGE_TEMPLATE("FairClass Global Callback.")
GLOBAL_CALLBACKS = FairCallbackChannel()


class ProcessStates:
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETE = "complete"
    ERROR = "error"

class FairClass:
    pid = None
    isTest = False

    def __init__(self, **kwargs):
        super().__init__()
        self.pid = os.getpid()
        self.handle_kwargs(**kwargs)

    def handle_kwargs(self, **kwargs):
        if not kwargs:
            return
        for key in kwargs.keys():
            self.set_variable(key, DICT.get(key, kwargs, default=False))

    def add_kwargs(self, **kwargs):
        self.handle_kwargs(**kwargs)

    def get_func(self, func):
        """ Get a function within the class.
        -> Call with ()
            i = t.get_func(r[38])
            u = i()
        """
        return getattr(self, func)

    def get_callable(self, attr):
        return callable(attr)

    def get_attribute(self, attr):
        try:
            item = getattr(self, attr)
            return item
        except Exception as e:
            Log.e("Failed to get attribute/function.", error=e)
            return False

    def get_method_names(self):
        return [func for func in dir(self)
                if self.get_callable(self.get_func(func))
                                       and not func.startswith("__")
                           and func.islower()
                           and not func.startswith("constructor")
                           and not func.startswith("construct")]

    def get_list_of_variables(self):
        return [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a))]

    def parse_from_json(self, js: {}):
        ats = self.get_list_of_variables()
        for key in js.keys():
            for at in ats:
                if str(key) == str(at):
                    item = js[key]
                    setattr(self, at, item)
        return self

    def set_variable(self, varName, varValue):
        try:
            setattr(self, varName, varValue)
            return True
        except Exception as e:
            return False

    @staticmethod
    def get_new_uuid():
        return F.get_uuid()

    @staticmethod
    def get_arg(key, value, default=False):
        return DICT.get(key, value, default=default)

    @staticmethod
    def get_dict(key, dic, default=False):
        return DICT.get(key, dic, default=default)

    @staticmethod
    def get_list(index, listObj, default=False):
        return LIST.get(index, listObj, default)