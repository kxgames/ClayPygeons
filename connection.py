import pickle
import socket, select

class Connection:

    delimiter = '\0'
    format = '%d%s%s'

    def __init__(self):
        self.socket = None
        self.poll = select.poll()

    def host(self, host, port):
        """ Wait for connections to the given address.  Once this method
        returns, the connection will be ready for use. """

        address = host, port
        greeter = socket.socket()

        greeter.bind(address)
        greeter.listen(5)

        self.socket, ignore = greeter.accept()

        self.finalize()

    def connect(self, host, port):
        """ Connect to the given address.  If another connection object is not
        already listening on this address, this will not work. """

        self.socket = socket.socket()
        self.socket.connect((host, port))

        self.finalize()

    def finalize(self):
        """ Prepare the socket object for reading.  By taking this extra step,
        we can avoid the use of threads. """

        fileno = self.socket.fileno()
        flags = select.POLLIN

        self.poll.register(fileno, flags)

    def send(self, message):
        """ Send a message across this connection.  The message is converted
        to a string using the pickle module, so it must be pickle-able. """

        assert self.socket

        string = pickle.dumps(message)
        size = len(string)

        packet = self.format % (size, self.delimiter, string)
        self.socket.sendall(packet)

    def receive(self):
        """ Receive all of the pending messages from the connection.  The
        messages will be reconstructed from strings using the pickle module,
        so the message classes must be defined for both clients. """

        assert self.socket

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
