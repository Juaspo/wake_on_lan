'''
Created on 23 nov. 2018

@author: ezasaju
'''
import getopt

import os

from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from wol import wake_on_lan
from wol import loadConfig
from wol import check_mac

import platform    # For getting the operating system name
import subprocess  # For executing a shell command


def btn_action(id):
    host = btn[id].cget("text")
    mac = mac_labels[id].cget("text")
    if (wake_on_lan(host, mac)):
        print(f"magic packet sent to {host}")
        label.config(bg="#5d5", text=host)
        ip_labels[id].config(fg="#22d")

        ping(ip_labels[id].cget("text"))
    else:
        print(f"Failed to send packet to\nHost: {host} \nMAC: {mac}")
        label.config(bg="red", text=host)

def goto_sleep():
    print ("going to sleep mode... Good night!")
    label.config(text = "Sleep")
    cc.put_to_sleep()


top = Tk()
top.minsize(width=250, height=150)

top.title("Wake on lan")

tabControl = ttk.Notebook(top)          # Create Tab Control
tab1 = ttk.Frame(tabControl)            # Create a tab
tabControl.add(tab1, text='wol')      # Add the tab
tabControl.pack(expand=1, fill="both")  # Pack to make visible

#top.geometry("100x100")
main_frame0 = Frame(tab1)
main_frame0.pack()

main_frame1 = Frame(main_frame0)
main_frame1.pack()

#main_frame2 = Frame(main_frame0)
#main_frame2.pack()


label = Label(main_frame1, text="WOL", fg="black", font="Verdana 30 bold")
label.pack()

frames = []
mac_labels = []
btn = []
ip_labels = []



for i in range(5):
    frames.append(Frame(main_frame0))
    frames[i].pack()


    mac_labels.append(Label(frames[i], text="xx:xx:xx:xx:xx:xx", fg="black", font="Verdana 10 bold"))
    mac_labels[i].grid(row = 0, column = 0)

    btn.append(Button(frames[i], text="No host", width = 15, command=lambda n=i: btn_action(n)))
    btn[i].grid(row = 0, column = 1)

    ip_labels.append(Label(frames[i], text="192.255.255.255", fg="black"))
    ip_labels[i].grid(row = 1, column = 0)


############################################ Add unit Pane
########################################## TAB2

def save_entry(hostname, mac, write_to_file = True):
    mac_length = len(mac)
    print("mac length:", mac_length)
    if (mac_length == 12):
        mac = ':'.join(mac[i:i+2] for i in range(0,12,2))
        print("Modified mac:", mac)

    if(not check_mac(mac)):
        print("wrong mac format!")
        return False

    entry_string = f"""
[{hostname}]
mac={mac}
"""

    print(entry_string)
    if (write_to_file):
        mydir = os.path.dirname(os.path.abspath(__file__))
        inifile = mydir+"/.wol_config.ini"
        write_data_to_file(inifile, "a", entry_string)
    return mac

def write_data_to_file(file_name, mode, s):
    # Open a file
    fo = open(file_name, mode)
    fo.write(s)
    fo.close()

def btn4_action():
    if(save_entry(text_entry_host.get(), text_entry_mac.get())):
        text_entry_host.delete(0, END)
        text_entry_mac.delete(0, END)

def btn5_action():
    mac = save_entry(text_entry_host.get(), text_entry_mac.get(), False)
    if (mac):
        text_entry_mac.config(fg="black")
        text_entry_mac.delete(0, END)
        text_entry_mac.insert(0, mac)
        wake_on_lan(text_entry_host.get(), mac)
    else:
        text_entry_mac.config(fg="red")
        return False


tab2 = ttk.Frame(tabControl)            # Create a tab
tabControl.add(tab2, text='Add unit')      # Add the tab
tabControl.pack(expand=1, fill="both")  # Pack to make visible

conv_frame1 = Frame(tab2)
conv_frame1.pack()


label0 = Label(conv_frame1, anchor = "w", text="Host name", fg="black", width = 15)
label0.grid(row = 0, column = 0)

label1 = Label(conv_frame1, anchor = "w", text="Mac address", fg="black", width = 15)
label1.grid(row = 1, column = 0)

text_entry_host = Entry(conv_frame1, width = 15)
text_entry_host.grid(row = 0, column = 1)

text_entry_mac = Entry(conv_frame1, width = 15)
text_entry_mac.grid(row = 1, column = 1)

btn4 = Button(conv_frame1, text="Save", width = 15, command = btn4_action)
btn4.grid(row = 2, column = 1)

btn5 = Button(conv_frame1, text="Test", width = 15, command = btn5_action)
btn5.grid(row = 2, column = 0)

############################################# Configurations

tab3 = ttk.Frame(tabControl)            # Create a tab
tabControl.add(tab3, text='Configure')      # Add the tab
tabControl.pack(expand=1, fill="both")  # Pack to make visible

conv_frame2 = Frame(tab3)
conv_frame2.pack()


################################## Functions


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0

def quit_func():
    if (mp.is_working()):
        MsgBox = messagebox.askyesno("Exit Application","Are you sure you want to exit the application", icon = "warning")
        if (MsgBox):
            mp.end_clocking(4, "user")
            top.destroy()
        else:
            print("Exit aborted")
    else:
        print ("good bye")
        top.destroy()

    #msg = messagebox.showinfo("Hi", "Hello World!")


def shutdown_pc():
    global shutdown_sequence

    if (shutdown_sequence):
        print ("Shutdown Aborted!")
        label.config(text = "Aborted!")
        os.system("shutdown /a")
        shutdown_sequence = False
        btn1["text"] = "Shutdown PC"
        check_if_runnung()

    else:
        print ("Shutting down PC Good bye!")
        label.config(text = "Shutdown!", bg="#d00", fg="#000")

        if (mp.is_working()):
            mp.end_clocking(4, "user")

        try:
            int(shutdown_delay_text_entry.get())
            shutdown_time = shutdown_delay_text_entry.get()
        except ValueError:
            shutdown_time = "40"
            print("Shutdown time not a number! Default 40s set")


        print (shutdown_time, "secs to shutdown")
        sequence = "shutdown /s /t " + shutdown_time + " /c \"Time counter shutdown\" /f /d p:0:0"
        print("seq", sequence)
        #os.system("shutdown /s /t 40 /c \"Time counter shutdown\" /f /d p:0:0")
        os.system(sequence)

        shutdown_sequence = True
        btn1["text"] = "Abort Shutdown"


def main(argv):
    config_content = loadConfig()
    n = 0;
    for devices in config_content:
        try:
            btn[n].config(text = devices)
            mac=list(config_content[devices].values())[0]
            if check_mac(mac): mac_labels[n].config(text = mac)
            else: mac_labels[n].config(fg="red", text = mac)
            n += 1
        except KeyError:
            print("Error with key")

    try:
        opts, args = getopt.getopt(argv, "hs:t:", ["help"])
    except getopt.GetoptError:
        print("Wrong input try -h for help")
        sys.exit(2)

    for opt, arg in opts:
        print("arg:", arg)
        if opt in ("-h", "--help"):
            print("\nTimeCounter help screen\n")
            print("-h\tfor this help text\n-s\tfor auto start\n-t\tfor timestamp")
            sys.exit()
        elif opt == "-t":
            timestamp(arg)
            take_timestamp = True
        elif opt == "-s":
            run_end_clocking(arg)
            autostart = True

        print ("auto start:", autostart, "timestamp:", take_timestamp, "argv:", argv, "opts:", opts)

if __name__ == '__main__':
    main(sys.argv[1:])

#btn.place(x=50, y=50)
top.mainloop()
