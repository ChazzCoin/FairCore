# from .Function import FairFunction
from .Queue import FairQueue
from F import DICT

class FairCallbackChannel:
    subscriptions = FairQueue()

    def subscribe(self, function):
        self.subscriptions.add(function)

    def looper(self):
        for i in range(self.subscriptions.size()):
            yield self.subscriptions.mainQueue.queue[i]

    @classmethod
    def getGlobalCallback(cls):
        newCls = cls()
        return newCls.get_callback

    def send_subscribed_callbacks(self, result):
        looper = self.looper()
        for i in range(self.subscriptions.size()):
            callback = next(looper)
            callback(result)

    def get_callback(self, msg):
        result = DICT.get("result", msg, default=False)
        if result or msg:
            self.send_subscribed_callbacks(result=msg)
        return result if result else msg

    def subscribeThisFunction(self, func):
        print("--WRAPPED AWAIT FUNCTION--")
        self.subscribe(func)
        def wrapper(args):
            return func(args)
        return wrapper