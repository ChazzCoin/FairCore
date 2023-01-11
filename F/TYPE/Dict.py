from F import DICT, CONVERT
from F.CLASS import FairClass


class FairDict(dict, FairClass):
    key_list = []
    value_list = []

    """ List Getters """
    def get_list_of_keys(self):
        return self.keys()

    def get_list_of_values(self):
        return self.values()

    """ Yielder/Iterator"""
    def loopKeyValue(self) -> (object, object):
        for key in self.keys():
            value = self[key]
            yield key, value

    """ Get """
    def __getattr__(self, key, default=None):
        """ Overriding dict[] bracket calling. """
        return self.safe_get(key, default=default)

    def safe_get(self, key, default=None):
        try:
            return DICT.get(key, self, default)
        except Exception as e:
            print(e)
            return "Failed to get Key/Value."

    """ Add """
    def __setattr__(self, key, value):
        """ Overriding dict[] bracket calling. """
        return self.safe_add(key, value)

    def safe_add(self, key, value):
        try:
            if key is None:
                return None
            if self.__contains__(key):
                return None
            self.key_list.append(key)
            self.value_list.append(value)
            super().__setitem__(key, value)
        except Exception as e:
            print(e)
            return None

    """ Delete """
    def delete_key(self, key):
        return super().pop(key, None)




if __name__ == '__main__':
    example = [{"_id": "1234", "title": "hey there", "date": "july 24 2022"},
               {"_id": "4321", "title": "something cool", "date": "august 02 2020"}]
    result = { "<date>": {"_id": "1234", "title": "hey there", "date": "july 24 2022"},
               "<date>": {"_id": "4321", "title": "something cool", "date": "august 02 2020"} }


    t = FairDict()
    t["test"] = "poop"
    t["test2"] = "poop2"
    t["f"] = ["dfa"]
    for k,v in t.loopKeyValue():
        print(k)
        print(v)