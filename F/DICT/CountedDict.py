

class CountedDict(dict):
    count = 0

    def __init__(self, data=None):
        if data is None:
            dict.__init__(self)
        else:
            dict.__init__(self, data)

    def add(self, item):
        self.count += 1
        dict.__setitem__(self, self.count, item)