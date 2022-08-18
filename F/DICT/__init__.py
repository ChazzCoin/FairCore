import json
import random
from F.LOG import Log

Log = Log("FCoRE.DICT")

"""
-> "dict" object extension/helper functions
"""

SORT_BY_VALUE = lambda dictObj: {k: v for k, v in sorted(dictObj.items(), key=lambda item: item[1], reverse=True)}

get_random = lambda dic: random.choice(list(dic.values()))

def yieldThis(dic:dict):
    for key in dic.keys():
        value = dic[key]
        yield key, value

""" Master Search """
def get(key: str, dic, default=False, depth=0):
    """
    Able to search embedded dict's for keys.
    Safely returns result or False.
    """
    try:
        if type(dic) is not dict:
            dic = dic.__dict__
        if dic.__contains__(key):
            return dic[key]
        for mainKey in dic.keys():
            tempValue = dic[mainKey]
            if mainKey == key:
                return tempValue
            if type(tempValue) is dict:
                result = get(key, tempValue, depth=depth+1)
                if not result and depth <= 20:
                    continue
                return result
        return default
    except Exception as e:
        Log.d(f"Failed to get key for dict error=[ {e} ]")
        return default

def get_key(value, dict, default=False):
    for key, v in dict.items():
         if value == v:
             return key
    return default

def get_from_path_keys(dic, *orderedKeys, default=False):
    count = len(orderedKeys)
    index = 1
    current_dic = dic
    for key in orderedKeys:
        if index == count:
            return get(key, current_dic, default=default)
        current_dic = get(key, dic, default=default)
        index += 1
    return False

def get_all_keys(dic, *keys, force_type=None) -> []:
    """
        Find all keys in dict
        RETURNS: List[]
    """
    if force_type is True:
        force_type = [str, list, tuple, set]
    temp_list = []
    key_list = []
    first = keys[0] if len(keys) > 0 else None
    # -> 1. Convert tuple(list) -> list
    if type(first) is list:
        for item in first:
            key_list.append(item)
    else:
        key_list = keys
    # -> 2. Loop Keys to find
    for key in key_list:
        item = get(key, dic)  # -> Deep Get ^ on dict
        itemType = type(item)
        # if null
        if item is None or item is False:
            continue
        if force_type:
            if itemType in force_type:
                temp_list.append(item)
            else:
                continue
        # if list, set, or tuple
        elif itemType in [list, set, tuple]:
            for i in item:
                temp_list.append(i)
        # if dict
        elif itemType is dict:
            list_of_items = to_value_list(item)
            for i in list_of_items:
                temp_list.append(i)
        else:
            temp_list.append(item)
    # -> 3. Post Work
    if len(temp_list) == 1:
        final_result = temp_list[0]
    else:
        final_result = temp_list
    return final_result

""" Manipulation """

def replace_key_value(dictIn, key, value):
    result = {}
    try:
        for inKey in dictIn.keys():
            if inKey == key:
                continue
            result[inKey] = dictIn[inKey]
        result[key] = value
        return result
    except Exception as e:
        Log.d(f"Could not replace key/value pair in dict. error=[ {e} ]")
        return dictIn

def replace_in_dict(input, variables):
    result = {}
    for key, value in input.iteritems():
        if isinstance(value, dict):
            result[key] = replace_in_dict(value, variables)
        else:
            result[key] = value % variables
    return result

def lazy_merge_dicts(*dict_args) -> dict:
    """
    -> LAZY MERGING
    Given any number of dictionaries, shallow copy and merge into a new dict,
    precedence goes to key-value pairs in latter dictionaries.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def tuples_to_dict(list_of_tuples: [()]) -> dict:
    """ Handles NLTK Single, Bi, Tri and Quad Terms """
    unique_list = list(set(list_of_tuples))
    temp_dict = {}
    for master_item in unique_list:
        if type(master_item[0]) is tuple:
            joined_tuple = " ".join(master_item[0])
            score = master_item[1]
            temp_dict[joined_tuple] = score
        elif type(master_item[0]) is str:
            word = master_item[0]
            score = master_item[1]
            temp_dict[word] = score
    return temp_dict

def remove_key_value(key, dic: dict) -> dict:
    try:
        del dic[key]
        return dic
    except Exception as e:
        Log.d(f"Failed to delete key value error=[ {e} ]")
        return dic

def add_key_value(key, value, dic: dict, forceListAsValue=False) -> dict:
    if dic.__contains__(key):
        temp = dic[key]
        if type(temp) in [list, tuple]:
            temp.append(value)
        elif type(temp) is str:
            temp = temp + value
        elif type(temp) is int:
            temp += value
        else:
            new = [temp, value]
            temp = new
        dic[key] = temp
    else:
        if forceListAsValue:
            dic[key] = [value]
        else:
            dic[key] = value
    return dic

""" Conversion """
def to_value_list(data: dict) -> list:
    """ Creates a list of values only. """
    temp_list = []
    for key in data.keys():
        temp_list.append(data[key])
    return temp_list

def to_key_list(data: dict) -> list:
    """ Creates a list of keys only. """
    temp_list = []
    for key in data.keys():
        temp_list.append(key)
    return temp_list

""" JSON """
def dumps(data: dict, indent=4, sort_keys=True, default=str):
    return json.dumps(data, sort_keys=sort_keys, indent=indent, default=default)

""" Export """
def to_pretty_json(data: dict, indent=4):
    obj = json.dumps(data, sort_keys=True, indent=indent, default=str)
    return obj

""" Sorting """
def order_by_value(dic: dict) -> dict:
    return SORT_BY_VALUE(dic)

""" Tiffany Specific """
# -> Takes word count dicts and add the values into one count.
def add_word_count(*dicts) -> dict:
    """ TIFFANY -> Add two dicts of word counts together """
    result = {}
    # -> Loop each dictionary
    for dictionary in dicts:
        # Loop each key
        for key in dictionary.keys():
            if result.__contains__(key):
                temp = result[key] + dictionary[key]
                result[key] = temp
            else:
                result[key] = dictionary[key]
    return result

def count_list_of_words(words):
    """ TIFFANY """
    result = {}
    for item in words:
        result = add_matched_word_to_result(item, result)
    return result

def add_matched_word_to_result(word: str, dic: dict) -> dict:
    """ TIFFANY """
    if word in dic.keys():
        dic[word] += 1
    else:
        dic[word] = 1
    return dic
