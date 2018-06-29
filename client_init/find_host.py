#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2018, KazPostBot"
__version__ = "1.0.1"
__maintainer__ = "Bauyrzhan Ospan"
__email__ = "bospan@cleverest.tech"
__status__ = "Development"


import nmap
import socket

# Get IP as string of the host machine
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def nmap_host():
    nm = nmap.PortScanner()
    # Vendor list for MAC address
    ip_raw = get_ip().split(".")
    ip = ip_raw[0] + "." + ip_raw[1] + "." + ip_raw[2] + ".*"
    nm.scan(ip, arguments='-sn')
    mac = "24:0A:64:43:77:DF"
    for h in nm.all_hosts():
        # print(nm[h]['addresses'])
        try:

            if mac in nm[h]['addresses']['mac']:
                mac_ip = nm[h]['addresses']['ipv4']
                return mac_ip
        except:
            pass


if __name__ == "__main__":
    print("---------------")
    print(nmap_host())

