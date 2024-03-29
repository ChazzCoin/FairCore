import F
from F import DICT, LIST
import os
from F.LOG import Log
from .Queue import FairQueue
from .Callback import FairCallbackChannel
Log = Log("FClass.FairClass")


GLOBAL_CALLBACK_MESSAGE_TEMPLATE = lambda msg: f"Global-Callback: {msg}"
GLOBAL_CALLBACK_MESSAGE = GLOBAL_CALLBACK_MESSAGE_TEMPLATE("FairClass Global Callback.")
FAIR_CALLBACK_CHANNEL = FairCallbackChannel()


class ProcessStates:
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETE = "complete"
    ERROR = "error"

class Flass:
    def __init__(self, **kwargs):
        super().__init__()
        self.handle_kwargs(**kwargs)
    def handle_kwargs(self, **kwargs):
        if not kwargs:
            return
        for key in kwargs.keys():
            self.set_variable(key, DICT.get(key, kwargs, default=False))

    def toJson(self, removeNone=False):
        result = {}
        for var in self.get_list_of_variables():
            item = self.get_attribute(var)
            if removeNone and item is None:
                continue
            if str(item).startswith("pid"):
                continue
            if str(item).startswith("_"):
                continue
            result[var] = item
        return result

    def fromJson(self, jsonObj: {}):
        if type(jsonObj) not in [dict]:
            jsonObj = jsonObj.__dict__
        if type(jsonObj) not in [dict] or not jsonObj:
            return None
        ats = self.get_list_of_variables()
        for key in jsonObj.keys():
            for at in ats:
                if str(key) == str(at):
                    item = jsonObj[key]
                    setattr(self, at, item)
        return self
    def get_list_of_variables(self):
        return [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a))]
    def get_attribute(self, attr):
        try:
            item = getattr(self, attr)
            return item
        except Exception as e:
            Log.e("Failed to get attribute/function.", error=e)
            return None
    def set_variable(self, varName, varValue):
        try:
            setattr(self, varName, varValue)
            return True
        except:
            return None

    def get_func(self, func):
        """ Get a function within the class.
        -> Call with ()
            i = t.get_func(r[38])
            u = i()
        """
        try:
            return getattr(self, func)
        except:
            return None

    @staticmethod
    def get_callable(attr):
        try:
            return callable(attr)
        except:
            return None

    @staticmethod
    def get_method_names(self):
        return [func for func in dir(self)
                if self.get_callable(self.get_func(func))
                                       and not func.startswith("__")
                           and not func.startswith("constructor")
                           and not func.startswith("construct")]
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


class FairClass(Flass):
    pid = None
    isTest = False

    def __init__(self, **kwargs):
        super().__init__()
        self.pid = os.getpid()

    def add_kwargs(self, **kwargs):
        self.handle_kwargs(**kwargs)