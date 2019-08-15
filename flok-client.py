#! /usr/bin/python3

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.sendto(b'leven is pijn', ('10.208.42.176', 5001))
sock.sendto(b'leven is pijn', ('127.0.0.1', 5001))
