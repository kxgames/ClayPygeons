#!/usr/bin/env python

import arguments
import worlds

def main(settings):
    world = worlds.Lead(settings)
    world.setup()

    clock = pygame.time.Clock()
    frequency = 40

    while world.still_playing():
        world.update()
        clock.tick(frequency)

if __name__ == "__main__":

    def module(name):
        return __import__("settings.%s" % name)

    settings = arguments.option(
            "settings", default="basic", type=module)

    main(settings)
