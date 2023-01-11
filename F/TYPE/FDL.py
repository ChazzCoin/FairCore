from F.TYPE.Dict import FairDict
from F.TYPE.List import FairList


class FDL(FairDict, FairList):


    def add(self, value, keyIndex=None):
        self.append(value)
        self[keyIndex if keyIndex else self.index_count] = value

    def get(self, keyIndex):
        return self[keyIndex]







