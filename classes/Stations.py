class Stations(object):
    """Class that hodls a station and their neighbor stations"""

    def __init__(self, name, critical=False):
        """Initialise class."""

        self.name = name
        self.critical = critical
        self.neighbors = []
