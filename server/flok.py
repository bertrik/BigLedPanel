#!/usr/bin/python
import serial
import sys
import termios, fcntl, sys, os, select
import time
import urllib2
import json
from optparse import OptionParser
from lib.ledboard import Ledboard
from lib.font1 import font1 as font
from mpd import MPDClient, CommandError
from socket import error as SocketError


ledboard = Ledboard('/dev/ttyACM0', 115200)
_buffer = " " * 18

while True:
    ledboard.drawstring('piemels zijn vies', font())
    time.sleep(.1)
