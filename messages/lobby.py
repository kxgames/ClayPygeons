class StartPlaying:
    def __init__(self, universe):
        self.map = universe.get_map()
        self.sight = universe.get_sight()
        self.targets = universe.get_targets()
        self.players = universe.get_players()
