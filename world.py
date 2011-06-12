from tokens import *
from messages import game

class Universe:

    # Constructor {{{1
    def __init__(self, courier, settings):
        self.courier = courier

        self.map = None
        self.map = Map(self, settings.map_size)

        self.sight = None
        #self.sight = Sight(self, settings.sight_position)

        self.targets = []
        #self.targets = [ Target(self, settings.target_position) ]

        #self.map = Map(self, settings.map_size)
        #self.sight = Sight(self, settings.sight_position)
        #self.targets = [ Target(self, settings.target_position) ]

        self.players = {}

    # Attributes {{{1
    def get_map(self):
        return self.map

    def get_sight(self):
        return self.sight

    def get_targets(self):
        return self.targets

    def get_players(self):
        return self.players
    # }}}1

    # Game Loop {{{1
    def setup(self, addresses):
        for address in addresses:
            player = Player(address, self.sight)
            self.players[address] = player

        courier = self.courier
        courier.subscribe(game.TargetLeft, self.target_left)
        courier.subscribe(game.TargetDestroyed, self.target_destroyed)

        return self

    def still_playing(self):
        return True

    def update(self):
        pass

    # Messaging {{{1
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

    def target_destroyed(self, address, target):
        self.player_scored(address, target)

        # If we decide to implement Quidditch-style rules, this is where we
        # would check to see if the snitch had been destroyed.

    def player_scored(self, address, points):
        player = self.players[address]
        points = target.get_points()

        player.score(points)

        message = game.PlayerScored(address, points)
        for connection in self.connections.values():
            connection.send(message)
    # }}}1

class World:
    """ Creates, stores, and provides access to all of the game objects. """

    # Constructor {{{1
    def __init__(self, courier):
        self.courier = courier

        self.map = None
        self.sight = None
        self.targets = []
        self.players = {}

        self.finished = False

    # Attributes {{{1
    def get_map(self):
        return self.map

    def get_sight(self):
        return self.sight

    def get_targets(self):
        return self.targets
    # }}}1

    # Game Loop {{{1
    def setup(self, message):
        self.map = message.map
        self.sight = message.sight
        self.targets = message.targets
        self.players = message.players

        courier = self.courier
        courier.subscribe(game.PlayerScored, self.player_scored)
        courier.subscribe(game.TargetCame, self.target_came)
        courier.subscribe(game.GameOver, self.game_over)

    def still_playing(self):
        return not self.finished

    def update(self, time):
        self.map.update(time)
        self.sight.update(time)

        # Iterate through a copy of this list, so targets can be safely
        # removed.
        targets = self.targets[:]

        for target in targets:
            target.update(time)

            if target.off_map():
                self.target_left(target)
            if target.is_destroyed():
                self.target_destroyed(target)

    def teardown(self):
        pass

    # Messaging {{{1
    def target_left(self, target):
        print "Sending: TargetLeft"
        message = game.TargetLeft(target)
        self.courier.deliver(message)
        self.targets.remove(target)

    def target_came(self, target):
        print "Receiving: TargetCame"
        self.targets.append(target)

    def target_destroyed(self, target):
        print "Sending: TargetDestroyed"
        message = game.TargetDestroyed(target)
        self.courier.deliver(message)
        self.targets.remove(target)

    def player_scored(self, address, points):
        print "Receiving: PlayerScored"
        player = self.players[address]
        player.score(points)

    def game_over(self, address, points):
        print "Receiving: GameOver"
        self.finished = True
    # }}} 1

