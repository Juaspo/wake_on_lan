
import time
import threading


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        print("stopping thread...")
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        global working

        working = 1
        delay_counter = 0
        print("Thread running!")
        while (not self.stopped()):

            running()

            if(delay_counter > recovery_interval):
                recovery_stamp_time()
                delay_counter = 0

            time.sleep(1)
            delay_counter += 1

        working = 0


counterThread = StoppableThread()
counterThread.setDaemon(True)