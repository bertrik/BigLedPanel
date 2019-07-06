#! /usr/bin/python

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto('je moeder zuigt', ('127.0.0.1', 5001))
