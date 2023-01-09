

class OrderedDict(dict):
    def __init__(self, data=None, **kwargs):
        self._keys = self.keys(data, kwargs.get("keys"))
        self._default_factory = kwargs.get("default_factory")
        if data is None:
            dict.__init__(self)
        else:
            dict.__init__(self, data)

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self._keys.remove(key)

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __iter__(self):
        return (key for key in self.keys())

    def __missing__(self, key):
        if not self._default_factory and key not in self._keys:
            raise KeyError()
        return self._default_factory()

    def __setitem__(self, key, item):
        dict.__setitem__(self, key, item)
        if key not in self._keys:
            self._keys.append(key)

    def clear(self):
        dict.clear(self)
        self._keys.clear()

    def copy(self):
        d = dict.copy(self)
        d._keys = self._keys
        return d

    def items(self):
        # returns iterator under python 3 and list under python 2
        return zip(self.keys(), self.values())

    def keys(self, data=None, keys=None):
        if data:
            if keys:
                assert isinstance(keys, list)
                assert len(data) == len(keys)
                return keys
            else:
                assert (
                    isinstance(data, dict)
                    or isinstance(data, OrderedDict)
                    or isinstance(data, list)
                )
                if isinstance(data, dict) or isinstance(data, OrderedDict):
                    return data.keys()
                elif isinstance(data, list):
                    return [key for (key, value) in data]
        elif "_keys" in self.__dict__:
            return self._keys
        else:
            return []

    def popitem(self):
        if not self._keys:
            raise KeyError()

        key = self._keys.pop()
        value = self[key]
        del self[key]
        return (key, value)

    def setdefault(self, key, failobj=None):
        dict.setdefault(self, key, failobj)
        if key not in self._keys:
            self._keys.append(key)

    def update(self, data):
        dict.update(self, data)
        for key in self.keys(data):
            if key not in self._keys:
                self._keys.append(key)

    def values(self):
        # returns iterator under python 3
        return map(self.get, self._keys)