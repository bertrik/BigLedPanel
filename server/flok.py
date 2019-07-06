#!/usr/bin/python
import serial
import sys
import termios, fcntl, sys, os, select
import time
import urllib2
import json
import threading
from optparse import OptionParser
from lib.ledboard import Ledboard
from lib.font1 import font1 as font
from mpd import MPDClient, CommandError
from socket import error as SocketError


ledboard = Ledboard('/dev/ttyACM0', 9600)
_buffer = " " * 18

def set_string(what):
    global _buffer

    l = len(what)
    if l > 18:
        l = 18

    _buffer = what[0:l] + _buffer[l:18]

def thrd():
    global _buffer

    f = font()

    while True:
        try:
            print 'b', _buffer
            ledboard.drawstring(_buffer, f)
            time.sleep(90 * 10 / 9600.0)

        except Exception as e:
            print e

th = threading.Thread(target=thrd)
th.daemon = True
th.start()

i = 0
while True:
    print 'a', i
    set_string('%d' % i)
    i += 1
    time.sleep(1)

#th.join()
