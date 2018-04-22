# -*- coding: UTF-8 -*-
from __future__ import print_function, division
import os
import nmap
import json
import requests

def get_all_components():
    """Returns a list of dictionaries with hosts running the tempmon API infrastructure.

    Explanation
    -------------

    Tempmon components all run a REST API on port 80, and respond to /whoami.

    This allows tempmon to operate in a network without static IPs.
    
    Returns
    -----------
    
    
    A list of dictionaries with the host ips, types and ids."""

    # scanner = nmap.PortScanner()
    #TODO: Figure out a different way to get the current domain IP prefix.
    # scanner.scan(hosts="192.168.1.0/24", arguments="-sn")
    # hosts = [(x, scanner[x]["hostnames"][0]["name"]) for x in scanner.all_hosts()]
    hosts = [
                ("192.168.1.106", "nodemcu1"), 
                ("192.168.1.107", "nodemcu2"), 
                ("192.168.1.108", "nodemcu3"),
                ("192.168.1.109", "nodemcu4"),
                ("192.168.1.110", "nodemcu5")
        ]
    # After identifying all hosts on network, identify valid ones.
    tempmon_hosts = []
    for host in hosts:
        ip = host[0]
        hostname = host[1]
        try:
            who_request = requests.get("http://{}/whoami".format(ip))
            # check if response is valid.
            # If it is, then read the response and identify the host.
            if who_request.status_code == 200:
                response = who_request.json()
                host_type = response["type"]
                host_id = response["id"]
                tempmon_hosts.append({"ip": ip, "type": host_type, "id": host_id})
            else:
                print("{} : {}".format(ip, who_request.status_code))
                print("{} : {}".format(ip, who_request.reason))
                print("{} : {}".format(ip, who_request.text))
                
        except requests.exceptions.RequestException:
            pass
    return tempmon_hosts

if __name__ == "__main__":
    print(get_all_components())
