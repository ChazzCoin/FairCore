from queue import Queue
from threading import Thread

import F
from F.CLASS import ProcessStates, FAIR_CALLBACK_CHANNEL, GLOBAL_CALLBACK_MESSAGE
from F.CLASS.Queue import FairQueue
import concurrent
from concurrent.futures import ThreadPoolExecutor

def create_function(function, arguments=None):
    return FairFunction(function, arguments)

class ArgumentTypes:
    NONE = "none"
    SINGLE = "single"
    ARGS = "args"
    KWARGS = "kwargs"

class FairFunction:
    fid = F.get_uuid()
    subscribed_functions = FairQueue()
    globalCallback = FAIR_CALLBACK_CHANNEL.getGlobalCallback()
    fname = ""
    fstate = ProcessStates.QUEUED
    func = None
    args = []
    argType = ""
    result = "None"
    message = GLOBAL_CALLBACK_MESSAGE
    thread = None

    def __init__(self, function, arguments=None, callback=None, name=None):
        self.func = function
        self.argType = F.get_func_type(function)
        self.args = arguments
        if callback:
            self.register_for_callback(callback)
        self.fname = name if name else self.fid
        self.thread = Thread(target=self.func, args=self.args)

    @classmethod
    def init_kwargs(cls, function, **kwargs):
        newCls = cls(function)
        newCls.args = kwargs
        return newCls

    @classmethod
    def init_args(cls, function, *args):
        newCls = cls(function)
        newCls.args = args
        return newCls

    def add_kwargs(self, **kwargs):
        self.args = kwargs

    def add_args(self, *args):
        self.args = args

    def add_name(self, name):
        self.fname = name

    def register_for_callback(self, ffunction):
        self.subscribed_functions.add(ffunction)

    def run(self, args=None):
        self.__set_running()
        try:
            if args:
                self.args = args
            if not self.args or self.argType == ArgumentTypes.NONE:
                return self.__finish_func(self.func())
            elif self.argType == ArgumentTypes.ARGS:
                return self.__finish_func(self.func(*self.args))
            elif self.argType == ArgumentTypes.KWARGS:
                return self.__finish_func(self.func(**self.args))
            else:
                return self.__finish_func(self.func(self.args))
        except Exception as e:
            print(f"There was an error running FairFunction. error=[ {e} ]")
            self.__set_error()

    def trigger_callbacks(self, resultMessage):
        self.send_global_callback_message(resultMessage=resultMessage)
        for i in range(self.subscribed_functions.size()):
            returnMessage = self.__get_result_message(resultMessage)
            self.send_callback_message(resultMessage=returnMessage)

    def __get_result_message(self, result):
        returnMessage = { "message": self.message, "result": result}
        return returnMessage

    def args_are_empty(self):
        if not self.args or len(self.args) <= 0:
            return True
        return False

    def __finish_func(self, result):
        self.result = result
        self.trigger_callbacks(resultMessage=result)
        return self.__set_return_complete(result)

    def __set_queued(self):
        self.fstate = ProcessStates.QUEUED

    def __set_running(self):
        self.fstate = ProcessStates.RUNNING

    def __set_return_complete(self, result):
        self.fstate = ProcessStates.COMPLETE
        return result

    def __set_error(self):
        self.fstate = ProcessStates.ERROR

    def fawait(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            task = executor.submit(self.run)
            t = task.result()
            self.result = t if t and len(t) > 0 else False
        return self.result

    def send_global_callback_message(self, resultMessage):
        try:
            if self.globalCallback:
                self.globalCallback(resultMessage)
                return "Global Callback Sent!"
        except Exception as e:
            print(f"There was an error running FairFunction. error=[ {e} ]")
            self.__set_error()

    def send_single_callback_message(self, resultMessage, callBackFunction):
        try:
            callBackFunction(resultMessage)
            return "Callback Sent!"
        except Exception as e:
            print(f"There was an error running FairFunction. error=[ {e} ]")
            self.__set_error()

    def send_callback_message(self, resultMessage):
        try:
            for i in range(self.subscribed_functions.size()):
                func: FairFunction = self.subscribed_functions.mainQueue.queue[i]
                func(resultMessage)
            return "Callbacks Sent!"
        except Exception as e:
            print(f"There was an error running FairFunction. error=[ {e} ]")
            self.__set_error()

    def runBackground(self):
        def wrapped_f(q):
            result = self.run()
            q.put(result)
            self.result = q.get()
            return self.result
        # Do Prep Work
        q = Queue()
        t = Thread(target=wrapped_f, args=(q,))
        t.start()
        return self.result

