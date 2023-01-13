

def getType(obj):
    return type(obj)
def is_types(obj, *types):
    if getType(obj) in types:
        return True
    return False