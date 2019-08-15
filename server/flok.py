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
_buffer = " " * 18

def set_string(what):
    global _buffer

    l = len(what)

    if l < 18:
        _buffer = what + ' ' * (19 - l) # 19! for extra space

    else:
        _buffer = what + ' '

def thrd():
    global _buffer

    f = font()

    t = 0

    while True:
        try:
            #eprint( '>%s' % _buffer )
            ledboard.drawstring(_buffer[0:18], f)
            #time.sleep(0.5)

            _buffer = _buffer[1:] + _buffer[0]

            t += 1
            if t >= 120:
                t = 0
                #time.sleep(2)

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
