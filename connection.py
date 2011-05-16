import pickle
import socket, select

class Connection(object):

    delimiter = '\0'
    format = '%d%s%s'
    ports = range(10236, 10246)

    def __init__(self, host):
        """ Save information on how to create the connection. """
        self.host = host

        self.poll = None
        self.socket = None

    def __enter__(self):
        """ Make sure that the socket has been created and prepare it for
        polling.  Polling the socket allows us to avoid the explicit use of
        threads. """

        assert self.socket

        fileno = self.socket.fileno()
        flags = select.POLLIN

        self.poll = select.poll()
        self.poll.register(fileno, flags)

        return self

    def __exit__(self, *ignore):
        """ Gracefully close the connection, no matter how the program
        terminates. """

        self.socket.close()

        self.poll = None
        self.socket = None

    # Define a pair of convenience functions.
    def enter(self): return self.__enter__()
    def exit(self, *ignore): return self.__exit__()

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

class Host(Connection):

    def __enter__(self):
        """ Listen for clients trying to connect to the given address.  Once
        this method returns, the connection will be ready for use. """

        for port in self.ports:
            try:
                address = self.host, port
                greeter = socket.socket()

                greeter.bind(address)
                greeter.listen(5)

                self.socket, ignore = greeter.accept()

                greeter.close()

                return Connection.__enter__(self)

            # If this port can't be bound, it's probably still in use.
            # Quietly continue to the next port.
            except socket.error:
                continue

        # Complain if none of the ports work.
        raise IOError()

class Client(Connection):

    def __enter__(self):
        """ Connect to the given address.  If another connection object is not
        already listening on this address, this will not work. """

        for port in self.ports:
            try:
                address = self.host, port

                self.socket = socket.socket()
                self.socket.connect(address)

                return Connection.__enter__(self)

            # If the client can't connect, the host is probably listening on a
            # different port.  
            except socket.error:
                continue

        # Complain if none of the ports work.
        raise IOError()

class Sandbox(Connection):
    """ Create an empty class that satisfies the connection interface.  This
    class can be used to play the game without going over the internet. """

    def __init__(self, host):
        self.messages = []

    def __enter__(self):
        pass

    def __exit__(self, *ignore):
        pass

    def send(self, message):
        self.messages.append(message)

    def receive(self):
        messages = self.messages
        self.messages = []
        return messages
