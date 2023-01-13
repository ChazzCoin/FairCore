from F.TYPE.Dict import fict
from F.TYPE.List import fist


class FDL(fict, fist):


    def add(self, value, keyIndex=None):
        self.append(value)
        self[keyIndex if keyIndex else self.index_count] = value

    def get(self, keyIndex):
        return self[keyIndex]







