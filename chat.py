#!/usr/bin/env python

import sys
from connection import Host, Client

try:
    role = sys.argv[1]
    host = sys.argv[2]

    roles = { "host" : Host(host), "client" : Client(host) }
    connection = roles[role]

except IndexError:
    sys.exit("Usage: chat.py <host|client> <host>")

except KeyError:
    sys.exit("Usage: The first argument must be 'host' or 'client'.")


try:
    with connection:

        while True:
            message = raw_input(">>> ")
            message = message.strip()

            if message:
                connection.send(message)

            for response in connection.receive():
                print response

except IOError:
    sys.exit("Error: Unable to establish a connection.")

except KeyboardInterrupt:
    print
