# Pi-IP-Broadcast

A set of tools to allow easy identification of one or more headless Raspberry Pi computers IP addresses on a local network.

Ideal for a classroom situation where students can access their headless Raspberry Pi from their laptop via SSH over the local WiFi network.

## How it works

One or more headless Raspberry Pi computers execute a program (`broadcast.py`) that broadcasts their IP address, hostname and information over the local network.

One or more computers excute a program (`listen.py`) that listen on the local network and prints the list of computers broadcasting their IP address and information.

## Features

* Headless Raspberry Pi setup performed entirely via SD card.
* Broadcast service automatically launches at boot on the Raspberry Pi.
* Multiple Raspberry Pi computers can broadcast simultaneously.
* Multiple computers can listen simulteaneously.

## Limitations

* Only IPv4 addresses are supported.
* The Raspberry Pi and listening computer must share the same class C sub-network (i.e. their IP addresses must share the same first three digit groups groups, e.g. 192.168.1.120 & 192.168.1.204).


# Setup

## Headless Raspberry Pi

### Wireless network and SSH

Before configuring the broadcast service, follow the instruction for a [headless Raspbery Pi setup](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md) from the official Raspberry Pi documentation to configure the wireless network access and enable SSH. In the case where the Raspberry Pi is to be connected to an ethernet cable, skip the wireless network configuration but ensure so enable SSH.

### Broadcasting Python script

Once the wireless network configuration is completed and SSH is enabled, open a terminal to root of the `rootfs` partition of the SD card to configure the broadcasting service (usually mounted at `/media/user/rootfs` on most Linux system).

Download the broadcasting Python script in the `/home/pi/` folder (replace `pi` in `home/pi/` by the appropriate username if different than `pi`):

```
$ wget https://github.com/DrGFreeman/pi-ip-broadcast/raw/master/broadcast.py -O home/pi/
```

Edit the `info` string near the top of the `broadcast.py` file. This string will print next to the Raspberry Pi's IP address and hostname on the listening computer. It can be useful to distinguish one Raspberry Pi from another if multiple Raspberry Pis on the network have the same hostname.

```python
# Enter a unique computer description to help identify it among others.
info = "Computer description"
```

Also, if the Raspberry Pi is connected via its Ethernet port instead of WiFi, change the `interface` string near the top of the `broadcast.py` file from `"wlan0"` to `"eth0"`.

```python
# Network interface name.
# - Use "wlan0" for a wifi connection
# - Use "eth0" for a wired ethernet connection
interface = "wlan0"
```

### Broadcasting service

Setup the broadcasting script to run as a background service that launches automatically when the Raspberry Pi boots. Note that these steps need to be performed on a Linux or Mac computer and will not work on Windows.

Download the service unit file (`ip_broadcast.service`):

```
$ sudo wget https://github.com/DrGFreeman/pi-ip-broadcast/raw/master/ip_broadcast.service -O etc/systemd/system/ip_broadcast.service
```

Make the service unit file executable:

```
$ sudo chmod a+x etc/systemd/system/ip_broadcast.service
```

Create symbolic links to enable the service:

```
$ cd etc/systemd/system/multi-user.target.wants
$ sudo ln -s ../ip_broadcast.service ./ip_broadcast.service
```

If a different username than `pi` is used, edit the `etc/systemd/system/ip_broadcast.service` file and replace `pi` with the appropriate username in the `[Service]` section (two locations).

```
# ip_broadcast.service
[Unit]
Description=IP address broadcast service
After=network.target

[Service]
Type=simple
Restart=always
RestartSec=1
User=pi
ExecStart=/usr/bin/python3 /home/pi/broadcast.py

[Install]
WantedBy=multi-user.target
```

## Listening Computer

The listening computer can be any computer connected to the same local network at the Raspberry Pi(s).

Notes:
1. The instructions below reflect a Linux computer where Python version 3 is accessed with the `python3` command. On a system where the `python` command launches Python 3, use the `python` command where the instructions indicate `python3`.
1. If the `pip` module is not found, it may need to be installed with `sudo apt update && sudo apt install python3-pip`.

Install the *Flask* Python web server:

```
$ python3 -m pip install flask
```

Download the listening Python script (`listen.py`):

```
$ wget https://github.com/DrGFreeman/pi-ip-broadcast/raw/master/listen.py
```

# Usage

## Headless Raspberry Pi

The broadcasting script is configured to launch as a service when the Raspberry Pi boots. No action is therfore required.

## Listening Computer

Launch the listening script:

```
$ python3 listen.py
```

Wait for the Raspberry Pi(s) to broadcast their IP address. It can take up to one minute before an address is displayed.  The terminal will show all the IP addresses being broadcasted along with the respective hostnames and information strings.

```
===============================================================================
Broadcasted IPs - Last update: 2020-02-23 23:08:04
-------------------------------------------------------------------------------
2020-02-23 23:07:54: 192.168.0.120, raspberrydam, New RPi4 Damien
2020-02-23 23:08:04: 192.168.0.206, octopi, Octoprint server - Prusa i3 MK2S
-------------------------------------------------------------------------------
```

If no broadcast is received from a specific IP address in a 150 seconds interval, the IP address will be removed from the list at the next refresh.

# Remote access to the Raspberry Pi
Once the IP address of a Raspberry Pi is known, this Raspberry Pi can be accessed remotely using different protocols. Refer to the [Remote Access](https://www.raspberrypi.org/documentation/remote-access/) section of the official Raspberry Pi documentation to learn more about the different ways of accessing a Raspberry Pi remotely.

### SSH access

SSH is the recommended method to securely access the Raspberry Pi command line from another computer. If accessing a Pi remotely from a Linux or Mac computer, simply use the `ssh` command:

```
$ ssh user@ipaddress
```

For example, if the user is `pi` and the ip address is `192.168.0.120` the command would be:

```
$ ssh pi@192.168.0.120
```

To access the Pi via SSH from a windows computer, see the [SSH using Windows](https://www.raspberrypi.org/documentation/remote-access/ssh/windows.md) page of the official Raspberry Pi documentation.