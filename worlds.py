import random
import settings

from vector import *
from collisions import *
from shapes import *

class Lead:

    class UnrecognizedMessage(Exception):
        pass

    def __init__(self, settings):
        self.greeter = network.Host(settings.host, settings.port)
        self.connections = []

        self.map = settings.map
        self.sight = settings.sight
        self.targets = settings.targets
        self.parameters = settings.parameters

        self.id = 1
        self.players = {}

    def __str__(self):
        return self.parameters["description"]

    def ready_to_play(self):
        return len(self.players) == self.parameters["number of players"]

    def still_playing(self):
        return True

    def setup(self):
        self.greeter.setup()

        while not self.ready_to_play():

            for connection in self.greeter.accept():
                self.follows[self.id] = connection
                self.id += 1

                response = lobby.LoginResponse(self)
                office.send(response)

            for id, connection in self.follows.pairs():
                for message in connection.recieve():
                    if isinstance(message, lobby.LoginRequest):
                        self.players[id] = message.name

            time.sleep(1)

        message = lobby.StartPlaying(self)
        for connection in self.follows.values():
            connection.send(message)

    def update(self, time):

        messages = [ (id, message)
                for message in connection.recieve()
                for id, connection in self.follows.pairs() ]

        for id, message in messages:
            if isinstance(message, game.TargetLeft):
                self.target_left(id, message.target)

            elif isinstance(message, game.TargetDestroyed):
                self.world.target_destroyed(id, message.target)

            else:
                raise Lead.UnrecognizedMessage(message)

    def target_left(self, origin, target):
        destination = origin
        players = self.players.keys()

        while destination == origin:
            destination = random.choice(players)

        self.target_came(destination, target)

    def target_came(self, destination, target):
        connection = self.follows[destination]
        message = game.TargetCame(target)

        connection.send(message)

    def target_destroyed(self, id, target):
        self.player_scored(id, target)

        # If we end up implementing the Quidditch idea, this would be the
        # place to check to see whether or not the game is over.

    def player_scored(self, id, points):
        player = self.players[id]
        points = target.get_points()

        player.score(points)

        message = game.PlayerScored(id, points)
        for connection in self.connections.values():
            connection.send(message)

class Follow(World):

    def __init__(self, host, port):
        self.connection = network.Client(host, port)

        self.map = None
        self.sight = None
        self.targets = []

        self.players = {}

    def still_playing(self):
        return True

    def setup(self):
        message = lobby.LoginRequest(name)
        connection = self.connection

        connection.send(message)

        while not self.playing:

            for message in connection.receive():
                if isinstance(message, lobby.LoginResponse):
                    print message.description

                elif isinstance(message, lobby.StartPlaying):
                    self.map = message.map
                    self.sight = message.sight
                    self.targets = message.targets
                    self.players = message.players

                    for target in self.targets:
                        position = self.map.get_random_position(target.radius)
                        target.set_position(position)

                    self.playing = True

                else:
                    raise Courier.UnrecognizedMessage(message)

            time.sleep(1)
                
    def update(self, time):
        self.map.update(time)
        self.sight.update(time)

        alive = []
        for target in self.targets:
            target.update(time)
            if target.hitpoints > 0:
                alive.append(target)
        self.targets = alive

        for message in self.connection.receive():
            if isinstance(message, game.PlayerScored):
                self.player_scored(message.id, message.points)

            if isinstance(message, game.TargetCame):
                self.target_came(message.target)

            elif isinstance(message, game.GameOver):
                self.game_over(message.winner)

            else:
                raise Courier.UnrecognizedMessage(message)

    def teardown(self):
        self.connection.teardown()

    def target_left(self, target):
        message = game.TargetLeft(target)
        self.connection.send(message)

    def target_came(self, target):
        self.targets.add(target)

    def target_destroyed(self, target):
        message = game.TargetDestroyed(target)
        self.connection.send(message)

    def player_scored(self, id, points):
        player = self.players[id]
        player.score(points)

    def game_over(self, id, points):
        self.playing = False

