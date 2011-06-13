import arguments

from tokens import *
from shapes import *

host = arguments.option("host", default='localhost')
port = arguments.option("port", default=0, cast=int) + 11249

size = Rectangle.from_size(500, 500)
map = Map(size=size, players=2, points=40, friction=50)

sights = [
        Sight("Rifle", mass=0.75, force=200, size=2, power=10, points=1),
        Sight("Shotgun", mass=0.85, force=200, size=10, power=4, points=1) ]

snitch = Snitch(chance=1, size=7, force=100, speed=60, health=50, points=40)
quaffles = [
        Quaffle(chance=3, force=100, size=15, speed=80, health=30, points=8),
        Quaffle(chance=9, force=100, size=20, speed=55, health=20, points=5),
        Quaffle(chance=14, force=100, size=10, speed=40, health=5, points=1) ]

# In the future, we will want to add more types of quaffles.  For example:
# AntiQuaffle(chance=5, size=3, speed=10, health=5, points=-10)
# HerdQuaffle(chance=50, size=4, speed=6, health=10, points=1)
