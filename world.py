import settings

from vector import *
from collisions import *
from shapes import *

class World:
    """ Creates, stores, and provides access to all of the game objects. """

    def setup(self):
        self.map = Map(self, settings.map_size)
        self.sight = Sight(self, settings.sight_position)
        self.targets = [ Target(self, settings.target_position) ]

    def teardown(self):
        pass
        
    def update(self, time):
        self.map.update(time)
        self.sight.update(time)

        for target in self.targets:
            target.update(time)

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
                print 'Target hit!', self.circle.get_center()

class Target(Sprite):
    """ Represents a target that players can shoot at.  These objects will
    move autonomously in the final version. """

    def __init__(self, world, position):
        Sprite.__init__(self, position, settings.target_radius)
        self.world = world

        self.power = settings.target_power
        self.speed = settings.target_speed
        self.loopiness = settings.target_loopiness

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

