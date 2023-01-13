from F import DICT
from F.CLASS import Flass


class fict(dict, Flass):

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
    def __getattr__(self, key):
        """ Overriding dict[] bracket calling. """
        return self.find(key, default=None)

    def find(self, key, default=None):
        try:
            return DICT.get(key, self, default)
        except Exception as e:
            print(e)
            return "Failed to get Key/Value."
    def find_any(self, keys:list, default=None):
        return DICT.get_any(keys, self, default=default)

    def find_all(self, *keys):
        return DICT.get_all_keys(self, keys)


    """ Add """
    def __setattr__(self, key, value):
        """ Overriding dict[] bracket calling. """
        return self.add(key, value)

    def add(self, key, value):
        try:
            if key is None:
                return None
            if self.__contains__(key):
                return None
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


    t = fict()
    t["test"] = "poop"
    t["test2"] = "poop2"
    t["f"] = ["dfa"]
    for k,v in t.loopKeyValue():
        print(k)
        print(v)