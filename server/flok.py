#!/usr/bin/python
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

ledboard = Ledboard('/dev/ttyACM0', 9600)
_buffer = " " * 18

def set_string(what):
    global _buffer

    l = len(what)

    if l < 18:
        _buffer = what + ' ' * (18 - l)

    else:
        _buffer = what

def thrd():
    global _buffer

    f = font()

    while True:
        try:
            print '>%s' % _buffer
            ledboard.drawstring(_buffer[0:18], f)
            time.sleep(0.5)

            _buffer = _buffer[1:] + _buffer[0]

        except Exception as e:
            print e

th = threading.Thread(target=thrd)
th.daemon = True
th.start()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 5001))

while True:
    try:
        data, sender_addr = sock.recvfrom(1024)
        print 'message from ', sender_addr
        set_string(str(data))

    except Exception as e:
        print e

#th.join()
