class StartPlaying(object):
    def __init__(self, universe, address):
        self.map = universe.get_map()
        self.sights = universe.get_sights()
        self.targets = universe.get_targets(address)
        self.players = universe.get_players()
