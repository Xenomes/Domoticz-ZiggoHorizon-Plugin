#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Basic Python Plugin Example
#
# Author: Xorfor
#
"""
<plugin key="xfr_ziggomediaboxxl" name="Ziggo Mediabox XL (Kodi remote)" author="Xorfor" version="1.0.0" wikilink="https://github.com/Xorfor/Domoticz-ZiggoHorizon-Plugin">
    <params>
        <param field="Address" label="IP Address" width="200px" required="true" default="127.0.0.1"/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal" default="true"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
from ziggo_mediabox_xl import ZiggoMediaboxXL


class BasePlugin:

    __HEARTBEATS2MIN = 6
    __MINUTES = 1         # or use a parameter

    __MSTAT_OFF = 0
    __MSTAT_ON = 1
    __MSTAT_PAUSED = 2
    __MSTAT_STOPPED = 3
    __MSTAT_VIDEO = 4
    __MSTAT_AUDIO = 5
    __MSTAT_PHOTO = 6
    __MSTAT_PLAYING = 7
    __MSTAT_DISCONNECTED = 8
    __MSTAT_SLEEPING = 9
    __MSTAT_UNKNOWN = 10

    # Device units
    __UNIT_STATUS = 1

    def __init__(self):
        self._runAgain = 0
        self._box = None

    def onStart(self):
        Domoticz.Debug("onStart called")
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
        else:
            Domoticz.Debugging(0)
        # Images
        # Check if images are in database
        if "xfr_ziggomediaboxxl" not in Images:
            Domoticz.Image("xfr_ziggomediaboxxl.zip").Create()
        try:
            image = Images["xfr_ziggomediaboxxl"].ID
        except:
            image = 0
        Domoticz.Debug("Image created. ID: "+str(image))
        # Validate parameters
        # Create devices
        if (len(Devices) == 0):
            Domoticz.Device( Unit=self.__UNIT_STATUS, Name="Status", Type=17, Switchtype=17, Image=image, Used=1 ).Create()
        # Log config
        DumpConfigToLog()
        # Connection
        self._box = ZiggoMediaboxXL(Parameters["Address"])

    def onStop(self):
        Domoticz.Debug("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Debug("onMessage: " + Connection.Name )

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Debug(
            "onCommand for Unit " + str(Unit) + ": Command '" + str(Command) + "', Level: " + str(Level))
        Command = Command.strip()
        action, sep, params = Command.partition(' ')
        action = action.upper()
        #
        if not self._box.turned_on():
            self._box.send_keys(["POWER"])
        #
        if action == "ON":
            self._box.send_keys(["POWER"])
        elif action == "OFF":
            self._box.send_keys(["POWER"])
        elif action == "UP":
            self._box.send_keys(["DPAD_UP"])
        elif action == "DOWN":
            self._box.send_keys(["DPAD_DOWN"])
        elif action == "LEFT":
            self._box.send_keys(["DPAD_LEFT"])
        elif action == "RIGHT":
            self._box.send_keys(["DPAD_RIGHT"])
        elif action == "INFO":
            self._box.send_keys(["INFO"])
        elif action == "SELECT":
            self._box.send_keys(["OK"])
        elif action == "BACK":
            self._box.send_keys(["BACK"])
        elif action == "CONTEXTMENU":
            self._box.send_keys(["MENU"])
        elif action == "CHANNELUP":
            self._box.send_keys(["CHAN_UP"])
        elif action == "CHANNELDOWN":
            self._box.send_keys(["CHAN_DOWN"])
        elif action == "STOP":
            self._box.send_keys(["STOP"])
        elif action == "FASTFORWARD" or action == "BIGSTEPFORWARD":
            self._box.send_keys(["FWD"])
        elif action == "REWIND" or action == "BIGSTEPBACK":
            self._box.send_keys(["CHAN_UP"])
        elif action == "PLAYPAUSE":
            self._box.send_keys(["PAUSE"])

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Debug("onNotification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(
            Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Debug( "onDisconnect: " + Connection.Name )

    def onHeartbeat(self):
        Domoticz.Debug( "onHeartbeat" )
        if self._box.turned_on():
            UpdateDevice( self.__UNIT_STATUS, self.__MSTAT_ON, "" )
        else:
            UpdateDevice( self.__UNIT_STATUS, self.__MSTAT_OFF, "" )
        # self._runAgain -= 1
        # if self._runAgain <= 0:
        #     self._runAgain = self.__HEARTBEATS2MIN * self.__MINUTES
        #     # Execute your command
        # else:
        #     Domoticz.Debug("onHeartbeat called, run again in " + str(self._runAgain) + " heartbeats.")


global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

################################################################################
# Generic helper functions
################################################################################
def DumpConfigToLog():
    # Show parameters
    Domoticz.Debug("Parameters count.....: " + str(len(Parameters)))
    for x in Parameters:
        if Parameters[x] != "":
           Domoticz.Debug("Parameter '" + x + "'...: '" + str(Parameters[x]) + "'")
    # Show settings
        Domoticz.Debug("Settings count...: " + str(len(Settings)))
    for x in Settings:
       Domoticz.Debug("Setting '" + x + "'...: '" + str(Settings[x]) + "'")
    # Show images
    Domoticz.Debug("Image count..........: " + str(len(Images)))
    for x in Images:
        Domoticz.Debug("Image '" + x + "...': '" + str(Images[x]) + "'")
    # Show devices
    Domoticz.Debug("Device count.........: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device...............: " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device Idx...........: " + str(Devices[x].ID))
        Domoticz.Debug("Device Type..........: " + str(Devices[x].Type) + " / " + str(Devices[x].SubType))
        Domoticz.Debug("Device Name..........: '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue........: " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue........: '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device Options.......: '" + str(Devices[x].Options) + "'")
        Domoticz.Debug("Device Used..........: " + str(Devices[x].Used))
        Domoticz.Debug("Device ID............: '" + str(Devices[x].DeviceID) + "'")
        Domoticz.Debug("Device LastLevel.....: " + str(Devices[x].LastLevel))
        Domoticz.Debug("Device Image.........: " + str(Devices[x].Image))

def UpdateDevice(Unit, nValue, sValue, TimedOut=0, AlwaysUpdate=False):
    if Unit in Devices:
        if Devices[Unit].nValue != nValue or Devices[Unit].sValue != sValue or Devices[Unit].TimedOut != TimedOut or AlwaysUpdate:
            Devices[Unit].Update(nValue=nValue, sValue=str(sValue), TimedOut=TimedOut)
            Domoticz.Debug("Update " + Devices[Unit].Name + ": " + str(nValue) + " - '" + str(sValue) + "'")

def UpdateDeviceOptions(Unit, Options={}):
    if Unit in Devices:
        if Devices[Unit].Options != Options:
            Devices[Unit].Update(nValue=Devices[Unit].nValue, sValue=Devices[Unit].sValue, Options=Options)
            Domoticz.Debug("Device Options update: " + Devices[Unit].Name + " = " + str(Options))

def UpdateDeviceImage(Unit, Image):
    if Unit in Devices and Image in Images:
        if Devices[Unit].Image != Images[Image].ID:
            Devices[Unit].Update(nValue=Devices[Unit].nValue, sValue=Devices[Unit].sValue, Image=Images[Image].ID)
            Domoticz.Debug("Device Image update: " + Devices[Unit].Name + " = " + str(Images[Image].ID))

def DumpHTTPResponseToLog(httpDict):
    if isinstance(httpDict, dict):
        Domoticz.Debug("HTTP Details (" + str(len(httpDict)) + "):")
        for x in httpDict:
            if isinstance(httpDict[x], dict):
                Domoticz.Debug("....'" + x + " (" + str(len(httpDict[x])) + "):")
                for y in httpDict[x]:
                    Domoticz.Debug("........'" + y + "':'" + str(httpDict[x][y]) + "'")
            else:
                Domoticz.Debug("....'" + x + "':'" + str(httpDict[x]) + "'")
