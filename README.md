Wake-On-Lan-Python
==================

wol.py is A small Python 3 script to allow the sending of a WOL Magic packet so that LAN clients can be remotely switched on from another machine on the same subnet. Rather than needing to know the MAC address of the desired machine, the script allows you to specify by hostname, so long as that host is included in the configuration file.

For a quick and lazy way to create the configuration file, see [The Wake On Lan section of my router build documentation](https://www.bentasker.co.uk/documentation/linux/258-usurping-the-bthomehub-with-a-raspberry-pi-part-three-routing-remote-administration-and-utilities#WakeOnLan)


Usage GUI
-------

Windows:
Make sure pythin is installed.

    Run start.bat

Linux:

    python3 gui_main.py


Usage headless
-------

    wol.py [hostname]

or

    wol.py list



Configuration File
--------------------

    #braodcast: Broadcast address for wake on lan. Should be on same lan as units are on (ip address)
    #repeat_ping: How many times to repeat ping before giving up. Tries a ping once every 5 second (int)
    #quit_after_wol: Should the application shutdown after magic packet is sent (true/false)

    [Config]
    broadcast=192.168.0.255
    repeat_ping=20
    quit_after_wol=false

    [Test unit]
    mac=AB:CD:EF:01:23:45
    ip=192.168.0.1


    
    
License
--------

PSF v2, see [LICENSE](LICENSE)
