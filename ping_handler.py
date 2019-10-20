
import time
import threading
import platform    # For getting the operating system name
import subprocess  # For executing a shell command

recovery_interval = 5

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        print("stopping thread")
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        global working

        working = 1
        delay_counter = 0
        print("Thread running!")
        while (not self.stopped()):

            #running()

            if(delay_counter > recovery_interval):
                if (ping("google.com", "1")):
                    self.stop()
                    print("Thread stopped:", self.stopped())

                delay_counter = 0

            time.sleep(1)
            delay_counter += 1

        working = 0


counterThread = StoppableThread()
counterThread.setDaemon(True)

def ping_threading():
    if not counterThread.isAlive():
        try:
            counterThread.start()
            #threading.Thread(target=running).start()
        except Exception:
            print("Error: unable to start thread")
        return True
    else:
        print("Thread already running")
        return False


def ping(host, nr_of_packets):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, nr_of_packets, host]

    return subprocess.call(command) == 0