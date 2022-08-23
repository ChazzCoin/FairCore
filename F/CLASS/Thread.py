from queue import Queue
from threading import Thread
from multiprocessing import Process

"""
    -> a "thread" will run within the same python runtime
        as a job.
"""
def get_single_thread(target, args=None) -> Thread:
    if not args:
        return Thread(target=target)
    return Thread(target=target, args=args)
#
# def startThreads_NoReturn(*threads: [Thread]):
#     for thread in threads:
#         thread: Thread = thread
#         thread.start()
#         thread.join()

def runFuncInBackground(function, arguments=None, callback=None):
    """ Pass in Function + Optional Arguments and Callback Function """
    from .Function import FairFunction
    fairFunc = FairFunction(function, arguments=arguments, callback=callback)
    def wrapped_f(q):
        result = fairFunc.run()
        q.put(result)
        fairFunc.result = q.get()
        return fairFunc.result
    # Do Prep Work
    q = Queue()
    t = Thread(target=wrapped_f, args=(q,))
    t.start()
    return fairFunc.result


def runInBackground(callback=None):
    """ DECORATOR FOR ANY METHOD """
    from .Function import FairFunction
    def functionWrapper(f):
        fairFunc = FairFunction(function=f, callback=callback)
        def threadWrapper(args):
            def runner(q, args):
                fairFunc.args = args
                result = fairFunc.run()
                q.put(result)
                fairFunc.result = q.get()
            # Do Prep Work
            q = Queue()
            t = Thread(target=runner, args=(q, args))
            t.start()
            return fairFunc.result
        return threadWrapper
    return functionWrapper


def wrapped_f(fairFunc):
    result = fairFunc.run()
    # q.put(result)
    # fairFunc.result = q.get()
    return fairFunc.result

def runMultiProcess(function, arguments=None, callback=None):
    """ Pass in Function + Optional Arguments and Callback Function """
    from .Function import FairFunction
    fairFunc = FairFunction(function, arguments=arguments, callback=callback)
    # Do Prep Work
    # q = Queue()
    t = Process(target=wrapped_f, args=(fairFunc,))
    t.start()
    return fairFunc.result




def __test_await():
    import time, F.OS
    U = F.get_uuid()
    pid = F.OS.get_pid()
    print(f"pid=[ {pid} ] : STARTING : TestFunctionId=[ {U} ]")
    for i in range(10):
        print(f"pid=[ {pid} ] : Test Counting=[ {i} ] : TestFunctionId=[ {U} ]")
        time.sleep(1)
    print(f"pid=[ {pid} ] : FINISHED : TestFunctionId=[ {U} ]")
    return U





