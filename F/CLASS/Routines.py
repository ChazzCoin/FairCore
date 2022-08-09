from F.CLASS import FairClass, ProcessStates, FAIR_CALLBACK_CHANNEL
from F.CLASS.Function import FairFunction
from F import LIST
import F
import concurrent
from concurrent.futures import ThreadPoolExecutor

def create_routine(functions:[]):
    return FairRoutine(functions=functions)

class FairRoutine(FairClass):
    rid = F.get_uuid()
    rstate = ProcessStates.QUEUED
    functions: [FairFunction] = []
    subscriptions = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_status(self):
        print(f"Routine[{self.rid}]")
        return self.rstate

    def start(self):
        """ Run Each Function, One At a Time. """
        if not self.functions:
            return "No Functions in Queue."
        self.__set_prepare_running()
        for func in self.functions:
            func: FairFunction = func
            func.run()

    def start_async(self):
        """ Run Each Function, All At Once, Keep Going. """
        if not self.functions:
            return "No Functions in Queue."
        self.__set_prepare_running()
        for func in self.functions:
            func: FairFunction = func
            func.register_for_callback(FAIR_CALLBACK_CHANNEL.getGlobalCallback())
            func.runBackground()
        self.__set_complete()

    def start_await(self):
        """ Run Each Function, All At Once, Wait for All Results. """
        if not self.functions:
            return "No Functions in Queue."
        self.__set_prepare_running()
        result = self.__awaitRoutine()
        return self.__set_return_complete(result)

    def add_func(self, func, arguments=None):
        ffunc = FairFunction(func, arguments=arguments)
        self.functions.append(ffunc)

    def add_ffunction(self, function:FairFunction):
        self.functions.append(function)

    def add_ffunctions(self, *functions:FairFunction):
        functions = LIST.flatten(functions)
        for function in functions:
            self.functions.append(function)

    def add_result_to_function(self, fid_OR_name, result):
        index = 0
        for func in self.functions:
            if fid_OR_name == func.fid or fid_OR_name == func.fname:
                func.result = result
                self.functions[index] = func
                return True
            index += 1
        return False

    def __set_queued(self):
        self.rstate = ProcessStates.QUEUED

    def __set_running(self):
        self.rstate = ProcessStates.RUNNING

    def __set_prepare_running(self):
        self.functions = LIST.flatten(self.functions)
        self.rstate = ProcessStates.RUNNING

    def __set_complete(self):
        self.rstate = ProcessStates.COMPLETE

    def __set_return_complete(self, result):
        self.rstate = ProcessStates.COMPLETE
        return result

    def __awaitRoutine(self):
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            tasks = []
            for func in self.functions:
                task = func.fid, executor.submit(func.run)
                tasks.append(task)
            for item in tasks:
                fid = LIST.get(0, item, default=False)
                r1 = LIST.get(1, item, default=False)
                r = r1.result() if len(r1.result()) > 0 else False
                self.add_result_to_function(fid, r)
                results.append(r)
        return results

