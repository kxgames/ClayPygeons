from __future__ import division

from vector import *
from shapes import *

map_size = Rectangle.from_size(500, 500)

sight_position = map_size.center
target_position = map_size.center

sight_drag = 0.75
sight_power = 450
sight_radius = 24

shot_power = 20

#sight_images = {
        #"normal" : pygame.image.load('images/sight-normal.png'),
        #"firing" : pygame.image.load('images/sight-firing.png') }

target_power = 200
target_speed = 100
target_radius = 10
target_loopiness = 50
target_hitpoints = 100

hitpoints_bar_height = 2


