import time

from F import OS
import F
from F.CLASS.Function import FairFunction
from F import LIST

from F.CLASS.Routines import FairRoutine
import concurrent
from concurrent.futures import ThreadPoolExecutor

def test_await():
    U = F.get_uuid()
    pid = OS.get_pid()
    print(f"pid=[ {pid} ] : STARTING : TestFunctionId=[ {U} ]")
    for i in range(10):
        print(f"pid=[ {pid} ] : Test Counting=[ {i} ] : TestFunctionId=[ {U} ]")
        time.sleep(1)
    print(f"pid=[ {pid} ] : FINISHED : TestFunctionId=[ {U} ]")
    return U

def awaitRoutine(routine:FairRoutine):
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        tasks = []
        for func in routine.functions:
            task = func.fid, executor.submit(func.run)
            tasks.append(task)
        for item in tasks:
            fid = LIST.get(0, item, default=False)
            r1 = LIST.get(1, item, default=False)
            r = r1.result() if len(r1.result()) > 0 else False
            routine.add_result_to_function(fid, r)
            results.append(r)
    return results

def awaitFunctions(*funcs:[FairFunction]):
    funcs = LIST.flatten(funcs)
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        tasks = []
        for func in funcs:
            task = executor.submit(func.run)
            tasks.append(task)
        for item in tasks:
            r = item.result() if len(item.result()) > 0 else False
            results.append(r)
    if results and len(results) == 1:
        return results[0]
    return results

def awaitThisFunction(func):
    print("--WRAPPED AWAIT FUNCTION--")
    def wrapper(args):
        fresult= FairFunction(func, args, name="wrapped").fawait()
        return fresult
    return wrapper