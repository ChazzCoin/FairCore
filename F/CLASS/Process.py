from multiprocessing import Process

class FairProcess:
    target = None
    args = ()
    process: Process = None
    isRunning = False

    def set_process(self, function, *args):
        self.process = Process(target=function, args=args)

    def start_process(self):
        self.process.start()
        self.isRunning = True

    def stop_process(self):
        self.process.terminate()
        self.isRunning = False

    def restart_process(self):
        self.stop_process()
        self.set_process(self.target, self.args)
        self.start_process()

# if __name__ == '__main__':
#     n = FairProcess(target=__test_await)
#     n.start_process()
#     time.sleep(5)
#     n.stop_process()
#     time.sleep(5)
#     n.restart_process()
