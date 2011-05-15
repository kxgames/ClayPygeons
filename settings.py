from __future__ import division

from vector import *
from shapes import *

map_size = Rectangle.from_size(500, 500)

sight_position = map_size.center
target_position = map_size.center

sight_drag = 0.75
sight_power = 350

#sight_images = {
        #"normal" : pygame.image.load('images/sight-normal.png'),
        #"firing" : pygame.image.load('images/sight-firing.png') }

target_power = 200
target_speed = 200
target_radius = 10
target_loopiness = 70


