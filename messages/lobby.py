class StartPlaying:
    def __init__(self, universe):
        self.map = universe.get_map()
        self.sights = universe.get_sights()
        self.targets = universe.get_targets()
        self.players = universe.get_players()
