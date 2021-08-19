#!/usr/bin/python
import sys
import socket
import argparse

__author__ = "Alexey Alexashin (alexashin.a.n@yandex.ru)"
__copyright__ = "Copyright (c) 2021 Alexey Alexashin"
__license__ = "GPL"

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-p", help="listen port")
parser.add_argument("-t", help="tcp", action='store_true')
parser.add_argument("-u", help="udp", action='store_true')

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

args = parser.parse_args()
if args.p is None:
    parser.print_help(sys.stderr)
    sys.exit(1)

if args.u:
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.bind(("", int(args.p)))
    print("UDP server listen on {} port".format(args.p))
    while(True):
        message, client_addr = client.recvfrom(1460)
        print("Bytes from {}: {}".format(client_addr, message))
        client.sendto(str(client_addr), client_addr)
elif args.t:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.bind(("", int(args.p)))
    client.listen(5)
    print("TCP server listen on {} port".format(args.p))
    conn, client_addr = client.accept()
    while(True):
        message = conn.recv(1460)
        print("Bytes from {}: {}".format(client_addr, message))
        conn.sendall(str(client_addr))

