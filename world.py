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

    # Attributes {{{1
    def get_map(self):
        return self.map

    def get_sights(self):
        return self.sights

    def get_targets(self):
        return self.quaffles

    def get_players(self):
        return self.players
    # }}}1

    # Game Loop {{{1
    def setup(self, addresses):
        for address in addresses:
            player = Player(address)
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
    def target_left(self, sender, address, message):
        destination = sender
        players = self.players.keys()

        # Make sure the message isn't sent to the courier running on a server,
        # which will always have the first address.  This is a serious hack,
        # but the alternative is writing a full lobby.
        #
        # Actually, this doesn't work at all.  The post office doesn't know
        # the sender's address, so there's no way to avoid potentially sending
        # the message right back to the sender.
        while destination in (0, 1, sender):
            destination = random.choice(players)

        self.target_came(destination, message.target)

    def target_came(self, destination, target):
        message = game.TargetCame(target)
        self.courier.deliver(message, destination)

    def target_destroyed(self, sender, address, message):
        self.player_scored(sender, message.target.get_points())

        # If we decide to implement Quidditch-style rules, this is where we
        # would check to see if the snitch had been destroyed.
        if False:
            print "Sending: GameOver"
            message = GameOver(self)
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
        print "Receiving: GameOver"
        self.finished = True
    # }}} 1

