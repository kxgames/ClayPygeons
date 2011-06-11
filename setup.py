from tokens import *

map = MediumMap()
sight = BasicSight()

targets = [
        ( 10, BasicQuaffle(size=5, speed=10, health=30, points=6) ),
        ( 15, BasicQuaffle(size=3, speed=7, health=20, points=5) ),

        ( 5,  AntiQuaffle(
            size=3, speed=10, health=5, annoying=15, points=-10) ),

        ( 50, FlockQuaffle(
            size=4, speed=6, health=10, flocking=10, points=1) ),

        ( 1,  Snitch(size=2, speed=12, health=50, points=50) ) ]

settings = {
        "number of players" : 2,
        "targets per player" : 10 }

