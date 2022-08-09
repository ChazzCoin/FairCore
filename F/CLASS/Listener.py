import F
from .Function import FairFunction
# import typing as t

class FairListener:
    lid = F.get_uuid()
    registered_functions: [FairFunction] = []
    callback_function: FairFunction = None

    def add_callback_function(self, func:FairFunction):
        self.callback_function = func

    def run_func(self):
        self.callback_function.fawait()
        self.trigger_callbacks(self.callback_function.result)

    def register_for_callback(self, function:FairFunction):
        self.registered_functions.append(function)

    def trigger_callbacks(self, resultMessage):
        for func in self.registered_functions:
            func: FairFunction = func
            message = "This is your callback!"
            returnMessage = { "message": message, "result": resultMessage}
            func.send_callback_message(resultMessage=returnMessage)

    def register_this_function(self):
        listener = self
        def wrapper1(func):
            fairFunc = FairFunction(func)
            listener.register_for_callback(fairFunc)
            return
        return wrapper1


class FairListener2:
    lid = F.get_uuid()
    registered_functions: [FairFunction] = []
    callback_functions: [FairFunction] = []

    def add_callback_function(self, func:FairFunction):
        self.callback_functions.append(func)

    def run_func_for_id(self, fid):
        for item in self.callback_functions:
            item: FairFunction = item
            if item.fid == fid:
                item.fawait()
                self.trigger_callbacks(item.result)

    def register_for_callback(self, function:FairFunction):
        self.registered_functions.append(function)

    def trigger_callbacks(self, resultMessage):
        for func in self.registered_functions:
            func: FairFunction = func
            message = f"{self.lid} - This is your callback!"
            returnMessage = { "message": message, "result": resultMessage}
            func.send_callback_message(resultMessage=returnMessage)

    def register_this_function(self, func):
        listener = self
        fairFunc = FairFunction(func)
        listener.register_for_callback(fairFunc)

    def make_this_function_a_callback(self, func):
        listener = self
        def wrapper1(args=None):
            fairFunc = FairFunction(func)
            fairFunc.args = args
            result = fairFunc.runBackground()
            listener.trigger_callbacks(resultMessage=result)
            return result
        return wrapper1
