import random
from F.LOG import Log

Log = Log("FCoRE.LIST")

"""
-> "list" object extension/helper functions
"""

SORT_BY_DICT_KEY = lambda listObj, dictKey: sorted(listObj, key=lambda k: k.get(f"{dictKey}"), reverse=True)

""" Master Search """
def get(index, items, default=False):
    """ Safely get index """
    if type(index) in [bool, list, tuple, dict]:
        return default
    _index = int(index)
    try:
        count = _index + 1
        l = len(items)
        if count > l:
            return default
        return items[_index]
    except Exception as e:
        Log.d(f"Failed to get index. error=[ {e} ]")
        return default

def get_random(items, default=False):
    if not items or type(items) not in [list, tuple]:
        return default
    count = len(items)
    if count <= 0:
        return default
    ran_index  =random.randint(0, count)
    return get(ran_index, items, default)

def find_str(term: str, items, default=False):
    """ Safely get index """
    # TODO: Build this to go DEEP!
    try:
        for item in items:
            if type(item) in [list, tuple, dict]:
                continue
            if str(term) == str(item):
                return item
        return default
    except Exception as e:
        Log.d(f"Failed to find {term}. error=[ {e} ]")
        return default

def remove_index(index: int, items: []):
    count = 0
    new_list = []
    for item in items:
        if count == index:
            count += 1
            continue
        count += 1
        new_list.append(item)
    return new_list

""" Manipulation """
def scramble(orig):
    """ Randomize List """
    try:
        dest = orig[:]
        random.shuffle(dest)
        return dest
    except Exception as e:
        Log.d(f"Failed to Scramble List. error=[ {e} ]")
        return orig

def flatten(*args):
    """ Flatten lists into one single list.
            (1, 2, ['b', 'a' , ['c', 'd']], 3)
            [1, 2, 'b', 'a', 'c', 'd', 3]
        :param args: items and lists to be combined into a single list
        :rtype: list
    """
    x = []
    list(args)
    for l in args:
        if not isinstance(l, (list, tuple)):
            l = [l]
        for item in l:
            if isinstance(item, (list, tuple)):
                x.extend(flatten(item))
            else:
                x.append(item)
    return x

def flatten_v2(args):
    """ Flatten lists into one single list.
            (1, 2, ['b', 'a' , ['c', 'd']], 3)
            [1, 2, 'b', 'a', 'c', 'd', 3]
        :param args: items and lists to be combined into a single list
        :rtype: list
    """
    x = []

    for item in args:
        if type(item) in [list, tuple]:
            temp = flatten_v2(item)
            x.extend(temp)
        else:
            x.append(item)
    return x

def merge_lists(list_one, list_two) -> []:
    if not list_one:
        return list_two
    if not list_two:
        return list_one
    result = []
    list_one.extend(list_two)
    for myDict in list_one:
        if myDict not in result:
            result.append(myDict)
    return result

def to_str(data) -> str:
    if type(data) is str:
        return data
    temp_str = ""
    for item in data:
        temp_str += "\n" + str(item)
    return temp_str

def remove_duplicates(list_in: list) -> list:
    try:
        return list(set(list_in))
    except Exception as e:
        Log.d(f"Failed to removed Dups. error=[ {e} ]")
        return list_in

