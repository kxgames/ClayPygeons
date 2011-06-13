import arguments

from tokens import *
from shapes import *

host = arguments.option("host", default='localhost')
port = arguments.option("port", default=0, cast=int) + 11249

size = Rectangle.from_size(500, 500)
map = Map(size=size, players=1, points=50, friction=100)

sights = [
        Sight("Rifle", mass=20, force=100, size=2, power=10, points=1),
        Sight("Shotgun", mass=50, force=100, size=10, power=4, points=1) ]

snitch = Snitch(size=5, force=75, speed=12, health=50, points=50)
quaffles = [
        Quaffle(chance=10, force=100, size=25, speed=10, health=30, points=6),
        Quaffle(chance=15, force=100, size=15, speed=7, health=20, points=5) ]

# In the future, we will want to add more types of quaffles.  For example:
# AntiQuaffle(chance=5, size=3, speed=10, health=5, points=-10)
# HerdQuaffle(chance=50, size=4, speed=6, health=10, points=1)
