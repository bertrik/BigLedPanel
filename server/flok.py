#!/usr/bin/python2
from __future__ import print_function
import serial
import sys
import termios, fcntl, sys, os, select
import time
import urllib2
import json
import socket
import threading
from optparse import OptionParser
from lib.ledboard import Ledboard
from lib.font1 import font1 as font
from socket import error as SocketError

def eprint( *args, **kwargs ):
    return print( *args, file=sys.stderr, **kwargs )

ledboard = Ledboard('/dev/ardrino', 9600)
wdth = ledboard.width()
print(wdth)
_buffer = ' ' * wdth
scroll = True
ts = None

def set_string(what_in):
    global _buffer
    global ts
    global scroll
    global wdth

    what = ''

    skip = False
    for w in what_in:
        if skip:
            if w == '$':
                skip = False

        elif w == '$':
            skip = True

        else:
            what += w

    l = len(what)

    if l < wdth:
        _buffer = what + ' ' * (wdth + 1 - l) # +1! for extra space

    else:
        _buffer = what + ' '

        scroll = True

    ts = time.time()

def thrd():
    global _buffer
    global ts
    global scroll
    global wdth

    f = font()

    while True:
        try:
            ledboard.drawstring(_buffer[0:wdth], f)

            if scroll:
                _buffer = _buffer[1:] + _buffer[0]
            else:
                _buffer = time.ctime()

            time.sleep(0.001)

            if ts and time.time() - ts >= 60:
                _buffer = ' ' * wdth
                ts = None
                scroll = False

        except Exception as e:
            sys.exit(e)

th = threading.Thread(target=thrd)
th.daemon = True
th.start()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 5001))

while True:
    try:
        data, sender_addr = sock.recvfrom(1024)
        eprint('message from %r: %r' % (sender_addr, data))
        set_string(data)

    except Exception as e:
        sys.exit(e)

#th.join()
