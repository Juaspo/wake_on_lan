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

from ping_handler import ping
from ping_handler import ping_threading


def btn_action(id):
    global quit_after_wol_var

    host = btn[id].cget("text")
    mac = mac_labels[id].cget("text")
    ip_nr = ip_labels[id].cget("text")
    bc_ip = general_ip_entry.get()

    if(validate_ip(bc_ip)):
        if (wake_on_lan(host, macaddress=mac, broadcast_ip=bc_ip)):
            print(f"magic packet sent to {host}")
            label.config(bg="#5d5", text=host)
            ip_labels[id].config(fg="#22d")

        else:
            print(f"Failed to send packet to\nHost: {host} \nMAC: {mac}")
            label.config(bg="red", text=host)

    repeat_number=repeat_ping_entry.get()
    if(validate_ip(ip_nr) and len(repeat_number) and not repeat_number == "0"):
        try:
            ping_threading(ip_nr, host, int(repeat_number))
            repeat_ping_entry.config(fg="black")
        except ValueError:
            repeat_ping_entry.config(fg="red")


    if quit_after_wol_var.get():
        quit_func()


def debug_def():
    global quit_after_wol_var
    print("quit wol status:", quit_after_wol_var.get())

top = Tk()
top.minsize(width=250, height=150)

top.title("Wake on lan")

tabControl = ttk.Notebook(top)          # Create Tab Control
tab1 = ttk.Frame(tabControl)            # Create a tab
tabControl.add(tab1, text='WOL')      # Add the tab
tabControl.pack(expand=1, fill="both")  # Pack to make visible

#top.geometry("100x100")
main_frame0 = Frame(tab1)
main_frame0.pack()

main_frame1 = Frame(main_frame0)
main_frame1.pack()

main_frame1_1 = Frame(main_frame0, highlightbackground="black", highlightthickness=1, pady=5)
main_frame1_1.pack()

label = Label(main_frame1, pady=20, width=24, relief=RIDGE, text="WOL", wraplength=250, bg="white", fg="black", font="sans 12 bold")
label.pack()

gen_label = Label(main_frame1_1, text="Broadcast address", fg="black", width = 17)
gen_label.grid(row = 0, column = 0)
general_ip_entry = Entry(main_frame1_1, width = 15)
general_ip_entry.grid(row = 0, column = 1)

main_frame1_2 = Frame(main_frame1_1)
main_frame1_2.grid(row=1, column=0)

repeat_label = Label(main_frame1_2, text="Repeat ping", fg="black", width = 10)
repeat_label.grid(row = 0, column = 1)
repeat_ping_entry = Entry(main_frame1_2, width = 3)
repeat_ping_entry.grid(row = 0, column = 0)

quit_after_wol_var=BooleanVar()

quit_cb = Checkbutton(main_frame1_1, width = 12, text="Quit after", variable=quit_after_wol_var, onvalue=True, offvalue=False)
quit_cb.grid(row = 1, column = 1)

#test_button = Button(main_frame1_1, text="test", command=debug_def)
#test_button.grid(row=2, column=0)

frames = []
mac_labels = []
btn = []
ip_labels = []


def remove_buttons_and_labels():
    global frames
    global mac_labels
    global btn
    global ip_labels

    for i in range(len(frames)):
        frames[i].destroy()
        mac_labels[i].destroy()
        btn[i].destroy()
        ip_labels[i].destroy()


def create_buttons_and_labels(nr_to_create):
    global frames
    global mac_labels
    global btn
    global ip_labels

    for i in range(nr_to_create):
        print("create:",i)
        frames.append(Frame(main_frame0, pady=5))
        frames[-1].pack()

        mac_labels.append(Label(frames[-1], text="MAC", fg="black", font="Verdana 10 bold"))
        mac_labels[-1].grid(row = 0, column = 0)

        btn.append(Button(frames[-1], text="No host", width = 15, command=lambda n=i: btn_action(n)))
        btn[-1].grid(row = 0, column = 1)

        ip_labels.append(Label(frames[-1], text="IP", fg="black"))
        ip_labels[-1].grid(row = 1, column = 0)


############################################ Add unit Pane
########################################## TAB2

def save_entry(hostname, mac, ip_addr, write_to_file=True):

    entry_string = f"""
[{hostname}]
mac={mac}
"""

    if len(ip_addr):
        entry_string += f"""ip={ip_addr}
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
    ip_addr=text_entry_ip.get()
    faulty_addr=False
    mac_addr=check_mac(text_entry_mac.get())

    if mac_addr:
        text_entry_mac.config(fg="black")
    else:
        text_entry_mac.config(fg="red")
        faulty_addr=True

    print(ip_addr)
    if len(ip_addr):
        if validate_ip(ip_addr):
            text_entry_ip.config(fg="black")
        else:
            text_entry_ip.config(fg="red")
            faulty_addr=True

    if(not faulty_addr and save_entry(text_entry_host.get(), mac_addr, ip_addr)):
        text_entry_host.delete(0, END)
        text_entry_mac.delete(0, END)
        text_entry_ip.delete(0, END)

def btn5_action():
    ip_addr=text_entry_ip.get()
    bc_ip = general_ip_entry.get()
    mac_addr=check_mac(text_entry_mac.get())
    host_n=text_entry_host.get()

    if (mac_addr):
        text_entry_mac.config(fg="black")
        text_entry_mac.delete(0, END)
        text_entry_mac.insert(0, mac_addr)
        wake_on_lan(host=host_n, broadcast_ip=bc_ip, macaddress=mac_addr)
    else:
        text_entry_mac.config(fg="red")

    if validate_ip(ip_addr):
        text_entry_ip.config(fg="black")
        ping_threading(ip_address=ip_addr, host_name=host_n)
    else:
        text_entry_ip.config(fg="red")

def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

tab2 = ttk.Frame(tabControl)            # Create a tab
tabControl.add(tab2, text='Add unit')      # Add the tab
tabControl.pack(expand=1, fill="both")  # Pack to make visible

conv_frame1 = Frame(tab2)
conv_frame1.pack()


label0 = Label(conv_frame1, anchor = "w", text="Host name", fg="black", width = 15)
label0.grid(row = 0, column = 0)

label1 = Label(conv_frame1, anchor = "w", text="MAC address", fg="black", width = 15)
label1.grid(row = 1, column = 0)

label2 = Label(conv_frame1, anchor = "w", text="IP address", fg="black", width = 15)
label2.grid(row = 2, column = 0)

text_entry_host = Entry(conv_frame1, width = 18)
text_entry_host.grid(row = 0, column = 1)

text_entry_mac = Entry(conv_frame1, width = 18)
text_entry_mac.grid(row = 1, column = 1)

text_entry_ip = Entry(conv_frame1, width = 18)
text_entry_ip.grid(row = 2, column = 1)

btn4 = Button(conv_frame1, text="Save", width = 15, command = btn4_action)
btn4.grid(row = 3, column = 1)

btn5 = Button(conv_frame1, text="Test", width = 15, command = btn5_action)
btn5.grid(row = 3, column = 0)

############################################# Configurations

tab3 = ttk.Frame(tabControl)            # Create a tab
tabControl.add(tab3, text='Configure')      # Add the tab
tabControl.pack(expand=1, fill="both")  # Pack to make visible

conv_frame2 = Frame(tab3)
conv_frame2.pack()


################################## Functions


def quit_func():
    print ("good bye")
    top.destroy()


def set_btn_labels():
    config_content = loadConfig()
    number_of_items = len(config_content)
    if "Config" in config_content:
        number_of_items -= 1
    create_buttons_and_labels(number_of_items)

    n = 0;

    for devices in config_content:
        try:
            print("number:",n)
            btn[n].config(text = devices)
            mac=config_content[devices]["mac"]
            if check_mac(mac): mac_labels[n].config(text = mac)
            else: mac_labels[n].config(fg="red", text = mac)
            if "ip" in config_content[devices]:
                ip_addr=config_content[devices]["ip"]
                ip_labels[n].config(text=ip_addr)
            else:
                print("No ip address for", config_content[devices])

            n += 1
        except KeyError:
            print("Error with key")

        if n >= number_of_items:
            return

def set_configuration():
    config_content = loadConfig()
    if "Config" in config_content:
        try:
            general_ip_entry.delete(0, END)
            general_ip_entry.insert(0, config_content["Config"]["broadcast"])
            repeat_ping_entry.delete(0, END)
            repeat_ping_entry.insert(0, config_content["Config"]["repeat_ping"])

            print ("quit content:", config_content["Config"]["quit_after_wol"])

            quit_value = config_content["Config"]["quit_after_wol"]
            if not quit_value or quit_value == "Err":
                quit_cb.deselect()
            else:
                quit_cb.select()
        except Exception as e:
            print("config error:", e)
            label.config(text=f"CFG error: {e}")

    else:
        general_ip_entry.delete(0, END)
        general_ip_entry.insert(0, "Bad config")
        return False

def main(argv):
    set_btn_labels()
    set_configuration()
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
