import random
import settings

from vector import *
from collisions import *
from shapes import *
from flocking import *

class Player:

    def __init__(self, address):
        self.address = address
        self.points = 0

    def score(self, points):
        self.points += points

class Map:
    """ Stores information about the game world.  This currently includes the size
    of the map, the number of players in the game, the cumulative point value
    of all the quaffles, and the amount of friction on the map. """

    def __init__(self, size, players, points, friction):
        self.size = size
        self.friction = friction

        self.points = points
        self.players = players

    def setup(self, world):
        self.world = world

    def update(self, time):
        pass

    def place_sight(self):
        return self.size.center

    def place_target(self):
        x = random.random() * self.size.width
        y = random.random() * self.size.height
        return Vector(x, y)

    def get_size(self):
        return self.size

    def get_friction(self):
        return self.friction

    def get_points(self):
        return self.points

    def get_players(self):
        return self.players


class Sight(Sprite):
    """ Represents a player's sight.  The motion of these objects is primarily
    controlled by the player, but they will bounce off of walls. """

    def __init__(self, name, mass, force, size, power, points):
        Sprite.__init__(self)

        self.name = name

        self.mass = mass
        self.force = force
        self.direction = Vector.null()

        self.size = size
        self.power = power
        self.points = points

    def get_size(self):
        return self.size

    def setup(self, world):
        self.world = world

        position = world.get_map().place_sight()
        Sprite.setup(self, position, self.size, self.force, 0.0)

    def update(self, time):
        map = self.world.get_map()

        # Set the acceleration.
        force = self.force * self.direction
        friction = Vector.null()

        self.acceleration = force + friction
        Sprite.update(self, time)

        # Bounce the sight off the walls.
        boundary = self.world.get_map().get_size()
        Sprite.bounce(self, time, boundary)

    def accelerate(self, direction):
        self.direction = direction

    def shoot(self):
        touching = Collisions.circles_touching

        for target in self.world.targets:
            if touching(self.circle, target.circle):
                target.injure(self)

class Quaffle(Sprite):
    """ Represents a target that players can shoot at.  These objects will
    move autonomously in the final version. """

    def __init__(self, force, size, speed, health, points, chance):
        Sprite.__init__(self)

        self.force = force
        self.size = size
        self.speed = speed

        self.health = health
        self.max_health = float(health)

        self.points = points
        self.chance = chance

    def setup(self, world):
        self.world = world

        position = world.get_map().place_target()
        Sprite.setup(self, position, self.size, self.force, self.speed)

        self.behaviors = [
                Flee(self, 1.0, self.world.get_sight(0), 100),
                ]
                #Seek(self, 1.0, self.world.get_sight(0), 100)

    def update(self, time):
        # Update the physics as usual.
        Sprite.update(self, time)

    def injure(self, sight):
        self.health -= sight.power

    def off_map(self, map):
        size = map.get_size()
        return not Collisions.circle_touching_shape(self.circle, size)

    def is_destroyed(self):
        return self.health <= 0

    def get_health(self):
        return self.health / self.max_health

class Snitch(Quaffle):

    def __init__(self, force, size, speed, health, points):
        Quaffle.__init__(self, force, size, speed, health, points, 0)
