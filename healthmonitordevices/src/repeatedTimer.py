# enchanced version of: 
# https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds-in-python
from threading import Timer
import threading

class RepeatedTimer(object):
    pool_sema = threading.BoundedSemaphore(value = 1)
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = max([1, interval])
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        RepeatedTimer.pool_sema.acquire()
        self.function(*self.args, **self.kwargs)
        RepeatedTimer.pool_sema.release()

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False