

def yieldThis(dic:dict):
    for key in dic.keys():
        value = dic[key]
        yield key, value
