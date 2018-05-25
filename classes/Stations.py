class Stations(object):
    """ Class that hodls a station and their neighbor stations. """

    def __init__(self, name, critical=False):
        """ Initialise class."""

        self.name = name
        self.critical = critical
        self.neighbors = []


    def append_neighbor(self, name, travel_time, critical = False):
        """ Appends station to neighbor list.

        Args:
            name: A string with the name of the neighbor.
            travel_time: Integer with traveltime from origin to neighbor.
            critical: Boolean which is true if the origin or neighbor is
                  a critical station.
        """

        self.neighbors.append([name, travel_time, critical])
