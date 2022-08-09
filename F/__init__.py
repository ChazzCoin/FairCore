
import uuid
from inspect import signature

def get_uuid():
    return str(uuid.uuid4())

def get_type(obj, toStr=True):
    return str(type(obj)) if toStr else type(obj)

def is_function(obj):
    if hasattr(obj, '__call__'):
        return True
    return False

def get_function_name(obj):
    if is_function(obj):
        return obj.__name__
    return False

def is_string(obj):
    if not obj:
        return False
    if type(obj) in [str]:
        return True
    return False

def is_dict(obj):
    if not obj:
        return False
    if type(obj) in [dict]:
        return True
    return False

def is_list(obj):
    if not obj:
        return False
    if type(obj) in [list]:
        return True
    return False

def is_list_OR_tuple(obj):
    if not obj:
        return False
    if type(obj) in [list, tuple]:
        return True
    return False

def is_list_OR_tuple_OR_set(obj):
    if not obj:
        return False
    if type(obj) in [list, tuple, set]:
        return True
    return False

def is_kwargs(obj):
    if str(obj).startswith("**"):
        return True
    return False

def is_args(obj):
    if str(obj).startswith("*") and not is_kwargs(obj):
        return True
    return False

def get_signature(function, toStr=True):
    sig = signature(function)
    return sig if not toStr else str(sig).replace("(", "").replace(")", "")

def convert_signature_arguments(strObj):
    totalCount = len(strObj) - 1
    current_index = 0
    start_index = 0
    args_list = []
    for char in strObj:
        if current_index == totalCount:
            argTemp = strObj[start_index:current_index+1]
            args_list.append(argTemp)
        elif str(char) == ",":
            if strObj[current_index+1] == " ":
                argTemp = strObj[start_index:current_index]
                start_index = current_index + 2
                args_list.append(argTemp)
        current_index += 1

    if args_list and len(args_list) == 1:
        return args_list[0]
    return args_list

def get_func_type(func):
    sig = get_signature(func)
    sigStr = str(sig).replace("(", "").replace(")", "")
    t = convert_signature_arguments(sigStr)
    if is_args(t) and t and len(t) >= 2:
        return "args"
    elif is_kwargs(t):
        return "kwargs"
    elif not t or str(t) == '':
        return "none"
    else:
        return "single"

def to_single_string(func):
    """ For *args to str only. """
    def wrapper(*items) -> []:
        from F import LIST
        temp = LIST.flatten(items)
        tempString = ""
        for item in temp:
            tempString += " " + item
        return func(tempString)
    return wrapper

def safe_args(func):
    """ For *args only. """
    def wrapper(*items) -> []:
        from F import LIST
        temp = LIST.flatten(items)
        return func(*temp)
    return wrapper
