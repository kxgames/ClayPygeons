import settings

from vector import *

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

    def __init__(self, position, velocity, acceleration):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration

    def update(self, time):
        # This is the "Velocity Verlet Algorithm".  I learned it in my
        # computational chemistry class, and it's a better way to integrate
        # Newton's equations of motions than what we were doing before.
        self.velocity += self.acceleration * (time / 2)
        self.position += self.velocity * time
        self.velocity += self.acceleration * (time / 2)

    def get_position(self):
        return self.position

    def get_velocity(self):
        return self.velocity

    def get_acceleration(self):
        return self.acceleration

class Sight(Sprite):
    """ Represents a player's sight.  The motion of these objects is primarily
    controlled by the player, but they will bounce off of walls. """

    def __init__(self, world, position):
        Sprite.__init__(self, position, Vector.null(), Vector.null())
        self.world = world

        self.drag = settings.sight_drag
        self.power = settings.sight_power

        self.direction = Vector.null()

    def update(self, time):
        position = self.position
        boundary = self.world.get_map().get_size()

        bounce = False
        vx, vy = self.velocity

        # Check for collisions against the walls.
        if position.y < boundary.top or position.y > boundary.bottom:
            bounce = True
            vy = -vy

        if position.x < boundary.left or position.x > boundary.right:
            bounce = True
            vx = -vx

        # If there is a bounce, flip the velocity and move back onto the
        # screen.
        if bounce:
            self.velocity = Vector(vx, vy)
            self.position += self.velocity * time

        # Set the acceleration.
        force = self.power * self.direction
        drag = -self.drag * self.velocity

        self.acceleration = force + drag

        # Update the physics as usual.
        Sprite.update(self, time)

    def accelerate(self, direction):
        self.direction = direction

class Target(Sprite):
    """ Represents a target that players can shoot at.  These objects will
    move autonomously in the final version. """

    def __init__(self, world, position):
        """ These variable names are a little bit obfuscated right now.  I
        plan to change them once I get a better understanding of how they
        affect the movement of the target.  
        
        Until then, range is the size of the imaginary circle drawn around the
        target.  Step is the maximum size of the displacement attempted each
        update cycle. """

        Sprite.__init__(self, position, Vector.null(), Vector.null())
        self.world = world

        self.power = settings.target_power
        self.speed = settings.target_speed
        self.radius = settings.target_radius
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

        # If the acceleration is too fast, then truncate it.  I don't really
        # think this will ever occur.
        if self.acceleration.magnitude > self.power:
            self.acceleration = self.power * self.acceleration.normal

        # Update the physics as usual.
        Sprite.update(self, time)

    def reposition(self, map):
        x, y = self.position

        x = x % map.size.width
        y = y % map.size.height

        self.position = Vector(x, y)

