#! /usr/bin/python

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto('leven is pijn', ('10.208.42.176', 5001))
