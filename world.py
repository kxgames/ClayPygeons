from __future__ import division

import copy
import settings

from tokens import *
from messages import game

# Make an address class to wrap integer address numbers.  It wouldn't be much
# more to pickle, but it would give some extra safety.

class Universe:

    # Constructor {{{1
    def __init__(self, courier):
        self.courier = courier

        self.map = settings.map
        self.sights = settings.sights

        self.snitch = settings.snitch
        self.quaffles = settings.quaffles

        self.players = {}
        self.targets = {}

        self.finished = False

    # Attributes {{{1
    def get_map(self):
        return self.map

    def get_sights(self):
        return self.sights

    def get_targets(self, address):
        return self.targets[address]

    def get_players(self):
        return self.players
    # }}}1

    # Game Loop {{{1
    def setup(self, addresses):

        self.points = 0

        # Associate each of the addresses with players.
        for address in addresses:
            player = Player(address)
            self.players[address] = player

        # Assign quaffles to each player.
        normalization = 0
        for quaffle in self.quaffles:
            normalization += quaffle.get_chance()

        for address in addresses:
            points = 0
            self.targets[address] = []

            # Skip the degenerate server-side player.
            if address == 1:
                continue

            while points < self.map.get_points() / 2:

                threshold = random.random() * normalization
                target = random.choice(self.quaffles)

                if target.get_chance() > threshold:
                    target = copy.copy(target)
                    self.targets[address].append(target)

                    points += target.get_points()
                    self.points += target.get_points()

        # Prepare to receive messages.
        courier = self.courier
        courier.subscribe(game.TargetLeft, self.target_left)
        courier.subscribe(game.TargetDestroyed, self.target_destroyed)

        return self

    def still_playing(self):
        return not self.finished

    def update(self):
        pass

    # Messaging {{{1
    def target_left(self, sender, address, message):
        destination = sender
        players = self.players.keys()

        # Make sure the message isn't sent to the courier running on a server,
        # which will always have the first address.  This is a serious hack,
        # but the alternative is writing a full lobby.
        while destination in (0, 1, sender):
            destination = random.choice(players)

        self.target_came(destination, message.target)

    def target_came(self, destination, target):
        message = game.TargetCame(target)
        self.courier.deliver(message, destination)

    def target_destroyed(self, sender, address, message):
        destroyed = message.target
        points = destroyed.get_points()

        self.player_scored(sender, destroyed.get_points())
        self.points -= points

        print "Receiving: TargetDestroyed."
        print "    points = %d / %d" % (self.points, self.map.get_points())

        normalization = 0
        for target in self.quaffles + [self.snitch]:
            normalization += target.get_chance()

        # Create a new target once enough targets have been destroyed.
        while self.points < self.map.get_points():
            threshold = random.random() * normalization
            next = random.choice(self.quaffles + [self.snitch])

            if next.get_chance() > threshold:
                addresses = self.players.keys()[:]
                addresses.remove(1)

                address = random.choice(addresses)

                self.points += next.get_points()
                self.target_came(address, next)

                message = "Snitch!" if isinstance(next, Snitch) else "Quaffle."

                print "Sending: New %s" % message
                print "    points = %d / %d" % (self.points, self.map.get_points())

        # The game ends once the Snitch is destroyed.
        if isinstance(destroyed, Snitch):
            print "Sending: GameOver"

            points = 0
            winner = None

            # Figure out which player has more points.
            for player in self.players.values():
                if points < player.get_points():
                    winner = player
                    points = player.get_points()

            message = game.GameOver(winner)
            self.courier.deliver(message)

    def player_scored(self, sender, points):
        player = self.players[sender]
        player.score(points)

        message = game.PlayerScored(sender, points)
        self.courier.deliver(message)

    # }}}1

class World:
    """ Creates, stores, and provides access to all of the game objects. """

    # Constructor {{{1
    def __init__(self, courier):
        self.courier = courier

        self.map = None
        self.sights = []
        self.targets = []
        self.players = {}

        self.finished = False

    # This method is a hack to prevent the world from ever getting pickled.
    # This is necessary because most of the game objects contain a reference
    # to the world, so when they get pickled this also gets pickled.
    def __getstate__(self):
        return {}

    # Attributes {{{1
    def get_map(self):
        return self.map

    def get_sight(self, index):
        return self.sights[index]

    def get_sights(self):
        return self.sights

    def get_targets(self):
        return self.targets
    # }}}1

    # Game Loop {{{1
    def setup(self, message):
        self.map = message.map
        self.map.setup(self)

        self.sights = message.sights
        self.targets = message.targets
        self.players = message.players

        for sight in self.sights:
            sight.setup(self)
        for target in self.targets:
            target.setup(self)

        courier = self.courier
        courier.subscribe(game.PlayerScored, self.player_scored)
        courier.subscribe(game.TargetCame, self.target_came)
        courier.subscribe(game.GameOver, self.game_over)

    def still_playing(self):
        return not self.finished

    def update(self, time):
        self.map.update(time)

        for sight in self.sights:
            sight.update(time)

        # Iterate through a copy of this list, so targets can be safely
        # removed.
        for target in self.targets[:]:
            target.update(time)

            if target.off_map(self.map):
                self.target_left(target)
            if target.is_destroyed():
                self.target_destroyed(target, self.get_sight(0))

    def teardown(self):
        pass

    # Messaging {{{1
    def target_left(self, target):
        message = game.TargetLeft(target)
        self.courier.deliver(message)
        self.targets.remove(target)

    def target_came(self, sender, address, message):
        target = message.target
        boundary = self.map.get_size()

        # Another hack: Since any newly created targets won't have been set up
        # yet and any existing targets will have the wrong world class, I have
        # to call the setup function again. 
        target.setup(self)

        position = self.map.place_sight()
        target.set_position(position)

        self.targets.append(target)

    def target_destroyed(self, target, sight):
        message = game.TargetDestroyed(target, sight)
        self.courier.deliver(message)
        self.targets.remove(target)

    def player_scored(self, sender, address, message):
        player = self.players[sender]
        player.score(message.points)

    def game_over(self, sender, address, message):
        print "Game over.  Player #%D won." % message.winner
        self.finished = True
    # }}} 1

