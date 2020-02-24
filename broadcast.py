#!/usr/bin/python3

import json
import os
import re
import subprocess
from threading import Thread
import time
import urllib.request

# Enter a unique computer description to help identify it among others.
info = "Computer description"

# Network interface name.
# - Use "wlan0" for a wifi connection
# - Use "eth0" for a wired ethernet connection
interface = "wlan0"

# This port number must match the one in listen.py on the listening server.
port = 5000


def local_ip(interface):

    try:
        ifconfig = (
            subprocess.check_output(["ifconfig", interface])
            .decode()
            .split("\n")
        )
        ip = re.search(r"(?<=inet )(\d{1,3}\.){3}\d{1,3}", ifconfig[1]).group()
        return ip

    except Exception:
        pass


def subnet(ip):
    return ".".join(ip.split(".")[:-1])


def hostname():
    return os.uname().nodename


def post_ip(target_ip, local_ip, port=port):
    url = "http://" + target_ip + ":" + str(port) + "/ip_listen"
    json_bytes = json.dumps(
        dict(ip=local_ip, hostname=hostname(), info=info)
    ).encode("utf-8")

    req = urllib.request.Request(url)
    req.add_header("Content-Type", "application/json; charset=utf-8")
    req.add_header("Content-length", len(json_bytes))

    try:
        resp = urllib.request.urlopen(req, json_bytes, timeout=2)
        print("Successfully posted to " + target_ip)
        return resp

    except Exception as e:
        pass


def post_to_all(interface):
    ip = local_ip(interface)

    threads = list()
    for i in range(256):
        target_ip = subnet(ip) + "." + str(i)
        t = Thread(target=post_ip, args=(target_ip, ip))
        threads.append(t)
        t.start()


if __name__ == "__main__":

    while True:
        post_to_all(interface)
        time.sleep(60)
