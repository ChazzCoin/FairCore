from F import DICT

"""
-> Utility Functions for converting one data types into another data type.
    EX: list [] -> into -> dict {}

-> FOLLOW THE NAMING RULE PLEASE
        List [] to Dict {}
    EX: list_Of_EmbeddedDicts_To_Dict_By_KeyValue
        <Input Type> OF <List Contents> TO <Output Type> BY <How To Convert>
        REQUIRED of OPTIONAL to REQUIRED by OPTIONAL

        Dict {} to List []
    EX: dict_To_List_Of_Values
        <Input Type> TO <Output Type> OF <What Will Be Added To Output Type>
        REQUIRED of OPTIONAL to REQUIRED by OPTIONAL
"""


def list_OF_Dicts_TO_Dict_BY_KeyValue(listObj, keyStr):
    by_key_dict = {}
    for i in listObj:
        current_key_value = DICT.get(keyStr, i, False)
        if not current_key_value:
            continue
        by_key_dict = DICT.add_key_value(current_key_value, i, by_key_dict, forceListAsValue=True)
    return by_key_dict


def dict_TO_List_OF_Values(data: dict) -> list:
    """ Creates a List of Values only, ignores Keys. """
    temp_list = []
    for key in data.keys():
        temp_list.append(data[key])
    return temp_list


def dict_TO_List_OF_Keys(data: dict) -> list:
    """ Creates a List of Keys only, ignores Values. """
    temp_list = []
    for key in data.keys():
        temp_list.append(key)
    return temp_list


def list_TO_Str(data) -> str:
    if type(data) is str:
        return data
    temp_str = ""
    for item in data:
        temp_str += "\n" + str(item)
    return temp_str


def TO_bool(obj):
    strObj = str(obj)
    if strObj.lower() == "false":
        return False
    elif strObj.lower() == "true":
        return True
    else:
        return bool(obj)