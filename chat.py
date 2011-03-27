#!/usr/bin/env python

import sys
from connection import *

try:
    role = sys.argv[1]
    host = sys.argv[2]
    port = int(sys.argv[3])
    
except IndexError:
    sys.exit("Usage: chat.py <host|client> <host> <port>")

connection = Connection()

if role == "host":     
    connection.host(host, port)
elif role == "client": 
    connection.connect(host, port)
else:
    assert False

while True:
    message = raw_input(">>> ")
    connection.send(message)

    for response in connection.receive():
        print response
