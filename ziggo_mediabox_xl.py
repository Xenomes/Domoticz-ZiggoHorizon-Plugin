#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Based on https://github.com/b10m/ziggo_mediabox_xl/blob/master/ziggo_mediabox_xl.py
#
# Above python script had a lot of errors in the key definitions!
# They are updated here
#
# Upload and display of channels not supported yet

import socket
#import requests


class ZiggoMediaboxXL(object):

    def __init__(self, ip):
        self._ip = ip
        self._port = {"state": 62137, "cmd": 5900}
        self._version = ""
        # self._channels_url = 'https://restapi.ziggo.nl/1.0/channels-overview'
        # self._fetch_channels()
        self._keys = {
            "POWER":            "E0 00",    # Toggle power of device
            "OK":               "E0 01",    # Confirm, exact meaning depends on context
            "BACK":             "E0 02",    # Go back, exact meaning depends on context
            "CHAN_UP":          "E0 06",    # Select next channel
            "CHAN_DOWN":        "E0 07",    # Select previous channel
            "HELP":             "E0 09",    # The F1 key for your set-top box
            "MENU":             "E0 0A",    # Toggle the main menu
            "GUIDE":            "E0 0B",    # Show TV guide
            "INFO":             "E0 0E",    # Toggle info for TV show of current channel
            "TEXT":             "E0 0F",    # Toggle teletext
            "MENU1":            "E0 11",    # Toggle the main menu
            "MENU2":            "E0 15",    # Toggle the main menu
            "DPAD_UP":          "E1 00",    # Navigate up
            "DPAD_DOWN":        "E1 01",    # Navigate down
            "DPAD_LEFT":        "E1 02",    # Navigate left
            "DPAD_RIGHT":       "E1 03",    # Navigate right
            "PAUSE":            "E4 00",    # Pause media
            "STOP":             "E4 02",    # Stop pausing
            "RECORD":           "E4 03",    # Record media
            "FWD":              "E4 05",    # Fast forwards
            "RWD":              "E4 07",    # Fast backwards
            "MENU3":            "EF 00",    # Meaning unknown
            "TIMESHIFT_INFO":   "EF 06",    # Meaning unknown
            "POWER2":           "EF 15",    # Meaning unknown
            "ID":               "EF 16",    # Show Radio Frequency menu
            "RC_PAIR":          "EF 17",    # Meaning unknown
            "TIMINGS":          "EF 19",    # Meaning unknown
            "ONDEMAND":         "EF 28",    # Open OnDemand menu
            "DVR":              "EF 29",    # Open DVR menu
            "TV":               "EF 2A"     # Close all menus and go back to TV show or go to previous channel
        }
        # And de NUM_00 ... NUM_09 keys
        for i in range(10):
            self._keys["NUM_{}".format(i)] = "E3 {:02d}".format(i)

    # def _fetch_channels(self):
    #   # Retrieve Ziggo channel information.
    #   json = requests.get(self._channels_url).json()
    #   self._channels = {c['channel']['code']: c['channel']['name']
    #   for c in json['channels']}

    # def channels(self):
    #     return self._channels

    def test_connection(self):
        # Make sure we can reach the given IP address.
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if sock.connect_ex((self._ip, self._port["cmd"])) == 0:
                return True
            else:
                return False
        except socket.error:
            raise

    def turned_on(self):
        # Update and return switched on state.
        self.update_state()
        return self.state

    def update_state(self):
        # Find out whether the media box is turned on/off.
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if sock.connect_ex((self._ip, self._port["state"])) == 0:
                self.state = True
            else:
                self.state = False
            sock.close()
        except socket.error:
            raise

    def send_keys(self, keys):
        # Send keys to the device.
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self._ip, self._port["cmd"]))
            # mandatory dance
            # Read the version of the set-top box...
            version_info = sock.recv(15)
            # ... and write it back. Why? I've no idea!
            sock.send(version_info)
            # The media box returns with 2 bytes (01 01). I've no idea what they mean
            sock.recv(2)
            # The following write and reads are used to authenticate
            sock.send(bytes.fromhex("01"))
            sock.recv(4)
            sock.recv(24)
            # send our keys now!
            for key in keys:
                if key in self._keys:
                    sock.send(bytes.fromhex("04 01 00 00 00 00 " + self._keys[key]))
                    sock.send(bytes.fromhex("04 00 00 00 00 00 " + self._keys[key]))
            sock.close()
        except socket.error:
            raise
