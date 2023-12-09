import threading, time

class setInterval:
    def __init__(self, interval: float, action):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time() + self.interval
        while not self.stopEvent.wait(nextTime - time.time()):
            nextTime += self.interval
            self.action(self)

    def cancel(self, timeout: float = 0):
        t = threading.Timer(timeout, self.stopEvent.set)
        t.start()

class setTimeout:
    def __init__(self, interval: float, action):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setTimeout)
        thread.start()

    def __setTimeout(self):
        time.sleep(self.interval)
        self.action(self)

    def cancel(self, timeout: float = 0):
        t = threading.Timer(timeout, self.stopEvent.set)
        t.start()