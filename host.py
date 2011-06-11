#!/usr/bin/env python

import arguments
import world, protocol

def module(name):
    return __import__("options.%s" % name)

if __name__ == "__main__":

    systems = {}
    settings = arguments.option(
            "settings", default="basic", type=module)

    systems["world"] = world.Lead(systems,
            settings.map,
            settings.sight,
            settings.targets,
            settings.parameters)

    systems["hub"] = protocol.Hub(systems,
            settings.host,
            settings.port)

    world = systems["world"]
    hub = systems["hub"]

    clock = pygame.time.Clock()
    frequency = 40

    hub.setup()

    while world.still_playing():
        time = clock.tick(frequency) / 1000
        for system in system.values():
            system.update(time)

