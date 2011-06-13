#!/usr/bin/env python

from __future__ import division

import pickle
import socket, select

# The assert statements at the top of the accept, send, and receive connection
# are nice, because they do help catch bugs.  But the assertion messages would
# be utterly cryptic for anyone other than myself.  I should thrown nicer
# exceptions with nicer messages instead.

class Connection(object):

    delimiter = '\0'
    format = '%d%s%s'

    def __init__(self, host, port):
        """ Save information on how to create the connection. """
        self.host = host
        self.port = port

        self.poll = None
        self.socket = None

    # Define a pair of convenience operators.
    def __enter__(self): return self.setup()
    def __exit__(self, *ignore): return self.teardown()

    def setup(self):
        """ Make sure that the socket has been created and prepare it for
        polling.  Polling the socket allows us to avoid the explicit use of
        threads. """

        assert self.socket

        fileno = self.socket.fileno()
        flags = select.POLLIN

        self.poll = select.poll()
        self.poll.register(fileno, flags)

        return self

    def teardown(self, *ignore):
        """ Gracefully close the connection and prevent this object from being
        used before the connection is explicitly reestablished. """

        #self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

        self.poll = None
        self.socket = None

class Host(Connection):

    def setup(self):
        """ Create a socket that is listening to the address given previously.
        The host can only listen on a single port at a time. """

        self.socket = socket.socket()
        address = self.host, self.port

        self.socket.bind(address)
        self.socket.listen(5)

        return Connection.setup(self)
        
    def accept(self):
        """ If a client is trying to connect, accept the connection and return
        an object that can be used to communicate with it.  If no clients are
        trying to connect, return immediately. """

        assert self.poll and self.socket

        events = True
        connections = []

        while events:
            events = self.poll.poll(0)

            for fileno, event in events:

                # Quietly ignore events that don't have to do with our socket.
                if not fileno == self.socket.fileno():
                    continue
                if not event & select.POLLIN:
                    continue

                # Accept any incoming connections.
                client, address = self.socket.accept()

                # Construct an object that can communicate with this client.
                connection = Client(*address)
                connection.setup(client)

                connections.append(connection)

        return connections

class Client(Connection):

    def setup(self, client=None):
        """ Connect to the given address.  If a host connection object is not
        already listening on this address, this will not work. """

        if client is None:
            address = self.host, self.port

            self.socket = socket.socket()
            self.socket.connect(address)

        else:
            self.socket = client

        return Connection.setup(self)

    def send(self, message):
        """ Send a message across this connection.  The message is converted
        to a string using the pickle module, so it must be pickle-able. """

        assert self.poll and self.socket

        string = pickle.dumps(message)
        size = len(string)

        packet = self.format % (size, self.delimiter, string)
        self.socket.sendall(packet)

    def receive(self):
        """ Receive all of the pending messages from the connection.  The
        messages will be reconstructed from strings using the pickle module,
        so the message classes must be defined for both clients. """

        assert self.poll and self.socket

        packet = ""
        messages = []

        socket = self.socket
        delimiter = Connection.delimiter

        for fileno, event in self.poll.poll(0):

            # Ignore events that don't have to do with our socket.
            if not fileno == self.socket.fileno():
                continue
            if not event & select.POLLIN:
                continue

            more_messages = True

            # There might be a few messages queued up, and they all have to be
            # dealt with.
            while more_messages:

                # Make sure enough of the packet has arrived to begin parsing.
                while delimiter not in packet:
                    packet += socket.recv(4096)

                size, packet = packet.split(delimiter, 1)
                size = int(size)

                # Receive the rest of the packet, then recreate the original
                # message.
                while size > len(packet):
                    packet += socket.recv(4096)

                string, packet = packet[:size], packet[size:]
                message = pickle.loads(string)

                messages.append(message)
                more_messages = bool(packet)

        return messages

class Sandbox(Client):
    """ Create an empty class that satisfies the connection interface.  This
    class can be used to test network logic without having to send packets over
    the internet. """

    def __init__(self, *ignore):
        self.messages = []

    def setup(self, *ignore):
        pass

    def teardown(self, *ignore):
        pass

    def send(self, message):
        self.messages.append(message)

    def receive(self):
        messages = self.messages
        self.messages = []
        return messages
