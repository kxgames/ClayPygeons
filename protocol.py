import time
import network

from messages import lobby, game

class Hub:

    class ForgotToSetup(Exception):
        pass

    class UnrecognizedMessage(Exception):
        pass

    class ForgotToQuit(Exception):
        pass

    def __init__(self, systems, host, port):
        self.greeter = network.Host(host, port)
        self.systems = systems

        self.offices = {}
        self.id = 1

        self.handler = lambda message: raise ForgotToSetup()

    def greet(self, connection):
        for connection in self.greeter.accept():
            office = Office(self, self.id, connection)
            self.offices[self.id] = office

            self.id += 1

            response = lobby.LoginResponse(self.world)
            office.send(response)

    def update(self):
        for office in self.offices.values():
            office.update()

    def broadcast(self, message):
        for office in self.offices.values():
            office.send(message)

    def deliver(self, id, message):
        self.offices[id].send(message)

    def setup(self):
        self.greeter.setup()
        self.handler = self.connecting

        world = self.systems["world"]

        while not world.ready_to_play():
            self.greet(); self.update()
            time.sleep(1)

        message = lobby.StartPlaying(world)
        self.broadcast(message)

    def connecting(self, id, message):
        if isinstance(message, lobby.LoginRequest):
            self.systems["world"].login(id, message.name)

        else:
            raise Hub.UnrecognizedMessage(message)

    def playing(self, id, message):
        world = self.systems["world"]

        if isinstance(message, game.TargetLeft):
            world.target_left(id, message.target)

        elif isinstance(message, game.TargetDestroyed):
            self.world.target_destroyed(id, message.target)
            for office in self.offices:
                office.send(message)

        else:
            raise Hub.UnrecognizedMessage(message)

    def player_scored(self, id, points):
        message = game.PlayerScored(id, points)
        self.broadcast(message)

    def target_came(self, id, target):
        message = game.TargetCame(target)
        self.deliver(message)

    def game_over(self, winner):
        message = game.GameOver(winner)

        self.broadcast(message)
        self.handler = lambda message: raise ForgotToQuit()

class Office:
    
    def __init__(self, hub, id, connection):
        self.id = id; self.hub = hub
        self.connection = connection

    def send(self):
        self.connection.send(message)

    def update(self):
        for message in self.connection.receive():
            self.hub.handler(self.id, message)

class Courier:

    class ForgotToSetup(Exception):
        pass

    class UnrecognizedMessage(Exception):
        pass

    class ForgotToQuit(Exception):
        pass
    
    def __init__(self, host, port, world):
        self.connection = network.Client(host, port)

        self.name = name
        self.world = world

        self.playing = False
        self.handler = lambda message: raise Courier.ForgotToSetup()

    def setup(self):
        message = lobby.LoginRequest(name)

        self.handler = self.connecting
        self.connection.send(message)

        while not self.playing:
            self.update()
            time.sleep(1)
                
    def update(self):
        for message in self.connection.messages():
            self.handler(message)

    def teardown(self):
        self.connection.teardown()

    def connecting(self, message):
        if isinstance(message, lobby.LoginResponse):
            self.world.login(message.description)

        elif isinstance(message, lobby.StartPlaying):
            self.world.setup(message.world)

            self.handler = self.playing
            self.playing = True

        else:
            raise Courier.UnrecognizedMessage(message)

    def playing(self, message):
        if isinstance(message, game.PlayerScored):
            self.world.player_scored(message.id, message.points)

        if isinstance(message, game.TargetCame):
            self.world.target_came(message.target)

        elif isinstance(message, game.GameOver):
            self.world.game_over(message.winner)

            self.handler = lambda message: raise Courier.ForgotToQuit()
            self.playing = False

        else:
            raise Courier.UnrecognizedMessage(message)

    def target_left(self, target):
        message = game.TargetLeft(target)
        self.connection.send(message)

    def target_destroyed(self, target):
        message = game.TargetDestroyed(target)
        self.connection.send(message)

