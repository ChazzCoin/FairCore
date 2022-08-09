from queue import Queue
import F


class FairQueue:
    maxSize = 0
    noDuplicates = True
    mainQueue: Queue

    def __init__(self, maxSize=0, noDuplicates=True):
        self.maxSize = maxSize
        self.noDuplicates = noDuplicates
        self.mainQueue = Queue(self.maxSize)

    def add(self, obj):
        if self.mainQueue.full():
            return False
        else:
            self.safe_put(obj)

    def get(self):
        temp = self.mainQueue.get()
        return temp

    def isDup(self, obj):
        if obj in self.mainQueue.queue:
            print(f"{obj} is already in queue!")
            return True
        for item in self.mainQueue.queue:
            if str(item) == str(obj):
                return True
            if F.is_function(item) and F.is_function(obj):
                objName = F.get_function_name(obj)
                itemName = F.get_function_name(item)
                if str(objName) == str(itemName):
                    return True
        return False

    def safe_put(self, obj):
        if self.noDuplicates:
            if not self.isDup(obj=obj):
                self.mainQueue.put(obj)
                print(f"{obj} added to queue!")
                return True
            else:
                return False
        else:
            self.mainQueue.put(obj)
            print(f"{obj} added to queue!")
            return True

    def clear_all(self):
        self.mainQueue = Queue(1)

    def size(self):
        try:
            return self.mainQueue.qsize()
        except Exception as e:
            print("Failed to get Size.", e)
            return 0

    def isEmpty(self):
        try:
            return self.mainQueue.empty()
        except Exception as e:
            print("Failed to see if queue is empty.", e)
            return 0

    def isFull(self):
        try:
            return self.mainQueue.full()
        except Exception as e:
            print("Failed to see if queue is full.", e)
            return 0