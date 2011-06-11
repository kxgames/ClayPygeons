import random
import settings

from vector import *
from collisions import *
from shapes import *

class World:
    """ Creates, stores, and provides access to all of the game objects. """

    def setup(self):
        pass

    def teardown(self):
        pass
        
    def update(self, time):
        self.map.update(time)
        self.sight.update(time)

        alive = []
        for target in self.targets:
            target.update(time)
            if target.hitpoints > 0:
                alive.append(target)
        self.targets = alive

    def get_map(self):
        return self.map

    def get_sight(self):
        return self.sight

    def get_targets(self):
        return self.targets

    def add_target(self, target):
        self.targets.append(target)

    def remove_target(self, target):
        self.targets.remove(target)

    def is_playing(self):
        return True

class Lead:

    def __init__(self, systems, map, sight, targets, parameters):
        # Contains references to the core game systems.
        self.systems = systems

        self.map = map
        self.sight = sight
        self.targets = targets
        self.parameters = parameters

        self.players = {}

    def __str__(self):
        return "Clay Pygeons"

    def setup(self):
        self.hub = self.systems["hub"]

    def login(self, id, name):
        if not self.ready_to_play():
            self.players[id] = Player(name, self.sight)
        else:
            raise AssertionError()

        if self.ready_to_play():
            self.hub.start_playing()

    def update(self, time):
        pass

    def ready_to_play(self):
        return len(self.players) == self.parameters["number of players"]

    def still_playing(self):
        return True

    def target_left(self, origin, target):
        destination = origin
        players = self.players.keys()

        while destination == origin:
            destination = random.choice(players)

        self.hub.target_came(destination, target)

    def target_destroyed(self, id, target):
        player = self.players[id]
        points = target.get_points()

        # Check to see if the game is over.
        
        player.score(points)
        self.hub.player_scored(id, points)

class Follow(World):

    def __init__(self, systems):
        self.systems = systems

    def update(self, time):
        pass

    def setup(self):
        self.courier = self.systems["courier"]

    def player_scored(self, id, points):
        pass

    def target_came(self, id, points):
        pass

    def game_over(self, id, points):
        pass

class Player:

    def __init__(self, name, sight):
        self.name = name
        self.sight = sight

        self.points = 0

    def score(self, points):
        self.points += points

class Map:
    """ Stores information about the game world.  This is just the size of the
    map right now, but it might eventually include information about how
    targets spawn. """

    def __init__(self, world, size):
        self.size = size

    def update(self, time):
        pass

    def get_size(self):
        return self.size

class Sprite:
    """ A parent class for every game object that can move.  This class stores
    position data and handles basic physics, but it is not meant to be
    directly instantiated. """

    def __init__(self, position, radius):
        self.circle = Circle(position, radius)
        self.velocity = Vector.null()
        self.acceleration = Vector.null()

    def update(self, time):
        # This is the "Velocity Verlet Algorithm".  I learned it in my
        # computational chemistry class, and it's a better way to integrate
        # Newton's equations of motions than what we were doing before.
        self.velocity += self.acceleration * (time / 2)
        self.circle = Circle.move(self.circle, self.velocity * time)
        self.velocity += self.acceleration * (time / 2)

    def bounce(self, time, boundary):
        x, y = self.circle.center
        vx, vy = self.velocity

        bounce = False

        # Check for collisions against the walls.
        if y < boundary.top or y > boundary.bottom:
            bounce = True
            vy = -vy

        if x < boundary.left or x > boundary.right:
            bounce = True
            vx = -vx

        # If there is a bounce, flip the velocity and move back onto the
        # screen.
        if bounce:
            self.velocity = Vector(vx, vy)
            self.circle = Circle.move(self.circle, self.velocity * time)

    def wrap_around(self, boundary):
        x, y = self.circle.center

        x = x % boundary.width
        y = y % boundary.height

        position = Vector(x, y)
        self.circle = Circle(position, self.circle.radius)

    def get_position(self):
        return self.circle.center

    def get_velocity(self):
        return self.velocity

    def get_acceleration(self):
        return self.acceleration

    def get_radius(self):
        return self.circle.radius

    def get_circle(self):
        return self.circle

class Sight(Sprite):
    """ Represents a player's sight.  The motion of these objects is primarily
    controlled by the player, but they will bounce off of walls. """

    def __init__(self, world, position):
        Sprite.__init__(self, position, settings.sight_radius)
        self.world = world

        self.drag = settings.sight_drag
        self.power = settings.sight_power

        self.direction = Vector.null()

    def update(self, time):
        # Set the acceleration.
        force = self.power * self.direction
        drag = -self.drag * self.velocity

        self.acceleration = force + drag
        Sprite.update(self, time)

        # Bounce the sight off the walls.
        boundary = self.world.get_map().get_size()
        Sprite.bounce(self, time, boundary)

    def accelerate(self, direction):
        self.direction = direction

    def shoot(self):
        for target in self.world.targets:
            if Collisions.circles_touching(self.circle, target.circle):
                target.hit()

class Target(Sprite):
    """ Represents a target that players can shoot at.  These objects will
    move autonomously in the final version. """

    def __init__(self, world, position):
        Sprite.__init__(self, position, settings.target_radius)
        self.world = world

        self.power = settings.target_power
        self.speed = settings.target_speed
        self.loopiness = settings.target_loopiness
        self.hitpoints = settings.target_hitpoints

        self.goal = self.speed * Vector.random()

    def update(self, time):
        offset = self.loopiness * Vector.random()

        self.goal = self.goal + offset
        self.goal = self.speed * self.goal.normal

        # The goal is what the velocity should ideally be.  The acceleration
        # can be computed by finding the difference between the current
        # velocity and the goal.
        self.acceleration = self.goal - self.velocity

        # If the acceleration is too fast, then truncate it.
        if self.acceleration.magnitude > self.power:
            self.acceleration = self.power * self.acceleration.normal

        # Update the physics as usual.
        Sprite.update(self, time)

    def hit(self):
        self.hitpoints -= settings.shot_power
        print 'Target hit!', self.hitpoints

    def get_hitpoints(self):
        return self.hitpoints
