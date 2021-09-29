#!/usr/bin/env python3
#
# Based on wol.py from http://code.activestate.com/recipes/358449-wake-on-lan/
# Amended to use configuration file and hostnames
#
# Copyright (C) Fadly Tabrani, B Tasker
#
# Released under the PSF License See http://docs.python.org/2/license.html
#
#


import socket
import struct
import os
import sys
import configparser
import re


myconfig = {}
mydir = os.path.dirname(os.path.abspath(__file__))

def check_mac(macaddress):

    if (len(macaddress) == 12):
        macaddress = ':'.join(macaddress[i:i+2] for i in range(0,12,2))

    macaddress = macaddress.upper()
    # Check mac address format
    found = re.fullmatch('^([A-F0-9]{2}(([:][A-F0-9]{2}){5}|([-][A-F0-9]{2}){5})|([\s][A-F0-9]{2}){5})|([a-f0-9]{2}(([:][a-f0-9]{2}){5}|([-][a-f0-9]{2}){5}|([\s][a-f0-9]{2}){5}))$', macaddress)
    if found:
        return macaddress


def wake_on_lan(host, broadcast_ip, macaddress):
    """ Switches on remote computers using WOL. """
    global myconfig

    #We must found 1 match , or the MAC is invalid
    if check_mac(macaddress):
	#If the match is found, remove mac separator [:-\s]
        macaddress = macaddress.replace(macaddress[2], '')
    else:
        return False

    # Pad the synchronization stream.
    data = ''.join(['FFFFFFFFFFFF', macaddress * 20])
    send_data = b''

    # Split up the hex values and pack.
    for i in range(0, len(data), 2):
        send_data = b''.join([send_data,
                             struct.pack('B', int(data[i: i + 2], 16))])

    # Broadcast it to the LAN.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    sock.sendto(send_data, (broadcast_ip, 7))
    print(f"broadcasted data to {broadcast_ip}")

    return True


def loadConfig():

    """ Read in the Configuration file to get CDN specific settings
    """
    global mydir
    global myconfig
    Config = configparser.ConfigParser()
    try:
        Config.read(mydir+"/.wol_config.ini")
    except Exception as e:
        print("Duplicate entry:", e)
    sections = Config.sections()
    dict1 = {}

    for section in sections:
        options = Config.options(section)
        sectkey = section
        myconfig[sectkey] = {}

        for option in options:
            if option == "quit_after_wol":
                try:
                    myconfig[sectkey][option] = Config.getboolean(section, option)
                except ValueError:
                    myconfig[sectkey][option] = "Err"
            else:
                myconfig[sectkey][option] = Config.get(section,option)

    return myconfig # Useful for testing

def usage():
	print('Usage: wol.py [hostname]')



if __name__ == '__main__':
    #mydir = os.path.dirname(os.path.abspath(__file__))
    conf = loadConfig()
    try:
        # Use macaddresses with any seperators.
        if sys.argv[1] == 'list':
            print('Configured Hosts:')
            for i in conf:
                if i != 'Config':
                    print('\t',i)
                    print('\n')
        else:
            if not wake_on_lan(sys.argv[1]):
                print('Invalid Hostname specified')
            else:
                print('Magic packet should be winging its way')
    except:
         usage()
