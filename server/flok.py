#!/usr/bin/python2

from __future__ import print_function
from datetime import datetime
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

ledboard = Ledboard('/dev/ardrino', 115200)
wdth = ledboard.width()
print(wdth)
_buffer = ' ' * wdth
scroll = False
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

    _buffer = what + ' ' * wdth

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
            if scroll:
                ledboard.drawstring(_buffer[0:wdth], f)

                _buffer = _buffer[1:] + _buffer[0]

            time.sleep(0.1)

            if ts and time.time() - ts >= 60:
                print('end')
                _buffer = ' ' * wdth
                ts = None
                scroll = False

        except Exception as e:
            break

    print('text thread end')

def pf():
    global scroll

    sockpf = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockpf.bind(('0.0.0.0', 5003))

    framebuffer = bytearray([0x00] * 90)

    while True:
        try:
            data, sender_addr = sockpf.recvfrom(9000)

            if scroll == False:
                msgs = data.split('\n')

                for m in msgs:
                    parts = m.split(' ')

                    if parts[0] == 'PX':
                        x = int(parts[1])
                        y = int(parts[2])

                        r = int(parts[3][0:2], 16)
                        g = int(parts[3][2:4], 16)
                        b = int(parts[3][4:6], 16)
                        gray = (r + g + b) / 3
                        p = gray >= 128

                        if x < 90 and y < 7:
                            if p:
                                framebuffer[x] |= 1 << y
                            else:
                                framebuffer[x] &= ~(1 << y)

                ledboard.drawpixels(framebuffer)

        except Exception as e:
            print('exception', e)
            break

    print('pixelflut thread end')

th = threading.Thread(target=thrd)
th.daemon = True
th.start()

th2 = threading.Thread(target=pf)
th2.daemon = True
th2.start()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 5001))

while True:
    try:
        data, sender_addr = sock.recvfrom(1024)
        eprint('message from %r: %r' % (sender_addr, data))
        set_string(data)

    except Exception as e:
        break

sys.exit(1)

#th2.join()
#th.join()
