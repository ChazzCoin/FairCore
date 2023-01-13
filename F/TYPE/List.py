from F import LIST
from F.CLASS import Flass


class fist(list, Flass):
    index_count = -1

    """ Yielder/Iterator"""
    def loopIndexValue(self) -> (object, object):
        i = 0
        for value in self:
            yield i, value
            i += 1

    """ Get """
    def __getattr__(self, key, default=None):
        """ Overriding dict[] bracket calling. """
        return self.safe_get(key, default=default)

    def get(self, index, default=None):
        try:
            return LIST.get(index, self, default)
        except Exception as e:
            print(e)
            return None

    """ Find """
    def find(self, item) -> (int, object):
        temp_index = 0
        for i in self:
            if i == item:
                return temp_index, self[temp_index]
            temp_index += 1
        return None, None

    def find_index(self, item) -> int:
        index, value = self.find(item)
        return index

    """ Add """
    def append(self, item):
        try:
            if item is None:
                return
            self.index_count += 1
            super().append(item)
        except Exception as e:
            print(e)

    """ Delete """
    def delete_item(self, item):
        return self.remove(item)


if __name__ == '__main__':
    example = [{"_id": "1234", "title": "hey there", "date": "july 24 2022"},
               {"_id": "4321", "title": "something cool", "date": "august 02 2020"}]
    result = { "<date>": {"_id": "1234", "title": "hey there", "date": "july 24 2022"},
               "<date>": {"_id": "4321", "title": "something cool", "date": "august 02 2020"} }

    t = fist()
    t.append("poop")
    t.append("jerky")
    print(t[0])