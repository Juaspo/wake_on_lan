
import time
import threading
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from _thread import interrupt_main
from tkinter import messagebox



class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""


    def __init__(self, ip_address, host_name, nr_of_runs, ping):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()
        self.host_name = host_name
        self.nr_of_runs = nr_of_runs
        self.ip_address = ip_address
        self.ping = ping

    def stop(self):
        print("stopping thread")
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):

        run_nr = 0
        print("Thread running!")
        while (not self.stopped()):

            print("run nr", run_nr, "for host", self.host_name)
            if self.ping(self.ip_address):
                #messagebox.askquestion("Success", responded, )

                self.stop()
                print("Thread stopped:", self.stopped())
                if messagebox.askyesno("Success! Quit application?", f"[{self.host_name}] responded!\nDo you wish to exit application?", icon="info"):
                    print("Exit program")
                    interrupt_main()

                else:
                    print("Continue running")


            if(run_nr >= self.nr_of_runs):
                messagebox.showwarning("Failed", f"No response from [{self.host_name}]")
                self.stop()
                print("Thread stopped:", self.stopped())

            time.sleep(5)
            run_nr += 1

class PingFunctions():

    def ping(self, host):
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """

        # Option for the number of packets as a function of
        param = '-n' if platform.system().lower()=='windows' else '-c'

        # Building the command. Ex: "ping -c 1 google.com"
        command = ['ping', param, "1", host]

        return subprocess.call(command) == 0


    def ping_threading(self, ip_address, host_name="Unknown device", repeat_count=1):

        if (len(host_name) == 0): host_name="Unknown device"

        counterThread = StoppableThread(ip_address, host_name, repeat_count, self.ping)
        counterThread.setDaemon(True)

        if not counterThread.isAlive():
            try:
                counterThread.start()
            except Exception as e:
                print("Error: unable to start thread", e)
            return True
        else:
            print("Thread already running")
            return False
