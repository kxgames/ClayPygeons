import settings

from vector import *
from shapes import *



class Sprite:
    """ A parent class for every game object that can move.  This class stores
    position data and handles basic physics, but it is not meant to be
    directly instantiated. """
    # Constructor {{{1

    def __init__(self):
        self.circle = None
        self.behaviors = []

        self.velocity = Vector.null()
        self.acceleration = Vector.null()

    def setup(self, position, radius, force, speed):
        self.circle = Circle(position, radius)
        self.force = force
        self.speed = speed

    # Updates {{{1
    def update(self, time):
        # Calculate change to acceleration. Accounts for the weight and
        # prioritization of each behavior. For these purposes, force and
        # acceleration are basically the same in name.
        remaining_force = self.force
        for behavior in self.behaviors:
            ideal_force, weight = behavior.update()
            force = ideal_force * weight
            if force.magnitude <= remaining_force:
                remaining_force -= force.magnitude
                self.acceleration += force
            elif remaining_force > 0:
                final_force = force.normal * remaining_force
                self.acceleration += final_force
                break
            else:
                break

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

    # Attributes {{{1
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
    
    def get_speed(self):
        return self.speed
    # }}}1

class Seek:
    # Seek {{{1
    def __init__ (self, sprite, weight, target, los=0.0):
        self.sprite = sprite
        self.weight = weight
        self.target = target
        self.los = los
    def update (self):
        desired_direction = self.target.get_position() - self.sprite.get_position()
        if 0.0 == self.los or desired_direction.magnitude <= self.los:
            desired_normal = desired_direction.normal
            desired_velocity = desired_normal * self.sprite.get_speed()
            force = desired_velocity - self.sprite.get_velocity()
        else:
            force = Vector.null()

        # Returns a force, not velocity. Velocities are used in these
        # calculations to find delta_velocity. delta_velocity = acceleration *
        # time. The time step will be dealt with later and, for our purposes,
        # acceleration is basically the same as force. 
        return force, self.weight
    # }}}1

class Flee:
    # Flee {{{1
    def __init__ (self, sprite, weight, target, los=0.0):
        self.sprite = sprite
        self.weight = weight
        self.target = target
        self.los = los
    def update (self):
        desired_direction = self.sprite.get_position() - self.target.get_position()
        if 0.0 == self.los or desired_direction.magnitude <= self.los:
            desired_normal = desired_direction.normal
            desired_velocity = desired_normal * self.sprite.get_speed()
            force = desired_velocity - self.sprite.get_velocity()
        else:
            force = Vector.null()

        # Returns a force, not velocity. Velocities are used in these
        # calculations to find delta_velocity. delta_velocity = acceleration *
        # time. The time step will be dealt with later and, for our purposes,
        # acceleration is basically the same as force. 
        return force, self.weight
    # }}}1

class Lazy:
    def __init__(self, sprite, weight):
        self.sprite = sprite
        self.weight = weight
    def update(self):
        sprite_velocity = self.sprite.get_velocity()
        print sprite_velocity
        if sprite_velocity.magnitude > 0:
            force = -1.0 * sprite_velocity
        else:
            force = Vector.null()
        return force
