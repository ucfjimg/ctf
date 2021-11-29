#!/usr/bin/env python3

import socket
import sys

server = 'ctfgatewayinterface.hackable.software'
port = 8888


def line(s):
    data = []
    while True:
        d = s.recv(1)
        if not d:
            s.close()
            return None
        data.append(d)
        if d == b'\n':
            break
    return str(b''.join(data).strip(), 'ascii')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((server, port))


    get = '/cgi-bin/session_b9b29257dd8339fa512b180c65f3e8b7dc2c3cdc'


    b = bytes(f'GET {get} HTTP/1.1\r\n\r\n', 'latin1')
    s.sendall(b)

    l = line(s)
    print(l)
    version, status, message = l.split(' ')
    print(version, status, message)

    content_length = None
    while True:
        header_line = line(s)
        if not header_line:
            break

        header, value = header_line.split(':', 1)
        header = header.strip().lower()
        value = value.strip()

        if header == 'content-length':
            try:
                content_length = int(value)
            except ValueError:
                pass
    
    if content_length == None:
        sys.exit(0)

    body = s.recv(content_length)
    print(body)

