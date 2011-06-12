import time
import settings

import network
from messages import lobby, maintenance

class Hub:

    def __init__(self):
        self.greeter = network.Host(settings.host, settings.port)
        self.addresses = range(settings.map.get_players() + 1)

        self.offices = {}
        self.subscriptions = {}

    def setup(self):
        self.greeter.setup()

    def listen(self, start_playing):
        while self.addresses:
            self.greet()
            time.sleep(1)

        players = [address for address in self.offices.keys()]
        universe = start_playing(players)

        message = lobby.StartPlaying(universe)
        for office in self.offices.values():
            office.send(message)

    def greet(self):
        for connection in self.greeter.accept():
            address = self.addresses.pop() + 1
            office = Office(self, address, connection)

            self.offices[address] = office

    def update(self):
        for office in self.offices.values():
            office.update()

    def subscribe(self, office, type):
        try:
            self.subscriptions[type].append(office)
        except KeyError:
            self.subscriptions[type] = [office]

    def cancel(self, office, type):
        self.subscriptions[type].remove(office)

    def deliver(self, message, address):
        key = type(message)
        subscribers = self.subscriptions[key]

        # If no address is given, deliver the message to all subscribers.
        if address == 0:
            for office in self.offices:
                office.send(message)

        # Otherwise, only deliver it to the address in question.
        else:
            office = self.offices[address]
            if office in subscribers:
                office.send(message)

class Office:
    
    def __init__(self, hub, address, connection):
        self.address = address
        self.name = None
        
        self.hub = hub
        self.connection = connection

    def send(self, message):
        self.connection.send(message)

    def update(self):
        for message in self.connection.receive():
            if isinstance(message, maintenance.Subscription):
                self.hub.subscribe(self.address, message.type)

            elif isinstance(message, maintenance.Cancellation):
                self.hub.cancel(self.address, message.type)

            elif isinstance(message, maintenance.Delivery):
                self.hub.deliver(message.message, message.address)

            else:
                raise UnrecognizedMessage()

class Courier:

    class UnrecognizedMessage(Exception):
        pass

    def __init__(self):
        self.connection = network.Client(settings.host, settings.port)
        self.callbacks = {}

    def login(self, callback):
        while True:
            for message in self.connection.receive():
                if isinstance(message, lobby.StartPlaying):
                    callback(message); return

            time.sleep(1)

    def setup(self):
        self.connection.setup()

    def deliver(self, message, address=0):
        request = maintenance.Delivery(message, address)
        self.connection.send(request)

    def subscribe(self, type, callback):
        try:
            self.callbacks[type].append(callback)

        except KeyError:
            self.callbacks[type] = [callback]

            request = maintenance.Subscription(type)
            self.connection.send(request)

    def cancel(self, type, callback):
        self.callbacks[type].remove(callback)

        if not self.callbacks[type]:
            request = maintenance.Cancellation(type)
            self.connection.send(request)

    def update(self, *ignore):
        for message in self.connection.receive():
            key = type(message)
            callbacks = self.callbacks.get(key, [])

            for callback in callbacks:
                callback(message)
                
    def teardown(self):
        self.connection.teardown()

